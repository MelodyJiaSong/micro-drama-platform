/** ZoomableImage: an <img> that opens a fullscreen zoom viewer on click.
 *
 * Viewer: wheel zooms around the cursor, drag pans, double-click toggles
 * fit ↔ 100% (actual pixels), keys `+` / `-` / `0` zoom / reset, Esc closes.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

export interface ZoomableImageProps {
  src: string;
  alt: string;
  className?: string;
  loading?: "lazy" | "eager";
}

const MIN_SCALE = 0.1;
const MAX_SCALE = 20;
const WHEEL_STEP = 1.15;

interface View {
  scale: number;
  x: number;
  y: number;
}

export function ZoomableImage({ src, alt, className, loading }: ZoomableImageProps): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  return (
    <>
      <img
        src={src}
        alt={alt}
        className={["zoomable-img", className].filter(Boolean).join(" ")}
        loading={loading}
        onClick={(e) => {
          e.stopPropagation();
          setOpen(true);
        }}
        title="点击放大"
      />
      {open ? <ZoomViewer src={src} alt={alt} onClose={() => setOpen(false)} /> : null}
    </>
  );
}

function ZoomViewer({ src, alt, onClose }: { src: string; alt: string; onClose: () => void }): JSX.Element {
  const stageRef = useRef<HTMLDivElement>(null);
  const [natural, setNatural] = useState<{ w: number; h: number } | null>(null);
  const [view, setView] = useState<View>({ scale: 1, x: 0, y: 0 });
  const drag = useRef<{ px: number; py: number; x: number; y: number; moved: boolean; backdrop: boolean } | null>(null);

  const fitView = useCallback((): View | null => {
    const stage = stageRef.current;
    if (!stage || !natural) return null;
    const scale = Math.min(stage.clientWidth / natural.w, stage.clientHeight / natural.h, 1);
    return {
      scale,
      x: (stage.clientWidth - natural.w * scale) / 2,
      y: (stage.clientHeight - natural.h * scale) / 2,
    };
  }, [natural]);

  const zoomAt = useCallback((factor: number, cx: number, cy: number): void => {
    setView((v) => {
      const scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, v.scale * factor));
      const k = scale / v.scale;
      return { scale, x: cx - (cx - v.x) * k, y: cy - (cy - v.y) * k };
    });
  }, []);

  const zoomCenter = useCallback((factor: number): void => {
    const stage = stageRef.current;
    if (!stage) return;
    zoomAt(factor, stage.clientWidth / 2, stage.clientHeight / 2);
  }, [zoomAt]);

  const reset = useCallback((): void => {
    const fit = fitView();
    if (fit) setView(fit);
  }, [fitView]);

  useEffect(() => {
    reset();
  }, [reset]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent): void => {
      if (e.key === "Escape") onClose();
      else if (e.key === "+" || e.key === "=") zoomCenter(WHEEL_STEP);
      else if (e.key === "-") zoomCenter(1 / WHEEL_STEP);
      else if (e.key === "0") reset();
      else return;
      e.preventDefault();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose, zoomCenter, reset]);

  // React's onWheel is passive, so preventDefault needs a native listener.
  useEffect(() => {
    const stage = stageRef.current;
    if (!stage) return;
    const onWheel = (e: WheelEvent): void => {
      e.preventDefault();
      const r = stage.getBoundingClientRect();
      zoomAt(e.deltaY < 0 ? WHEEL_STEP : 1 / WHEEL_STEP, e.clientX - r.left, e.clientY - r.top);
    };
    stage.addEventListener("wheel", onWheel, { passive: false });
    return () => stage.removeEventListener("wheel", onWheel);
  }, [zoomAt]);

  const onPointerDown = (e: React.PointerEvent<HTMLDivElement>): void => {
    if (e.button !== 0) return;
    const backdrop = e.target === e.currentTarget;
    e.currentTarget.setPointerCapture(e.pointerId);
    drag.current = { px: e.clientX, py: e.clientY, x: view.x, y: view.y, moved: false, backdrop };
  };
  const onPointerMove = (e: React.PointerEvent<HTMLDivElement>): void => {
    const d = drag.current;
    if (!d) return;
    const dx = e.clientX - d.px;
    const dy = e.clientY - d.py;
    if (Math.abs(dx) + Math.abs(dy) > 3) d.moved = true;
    setView((v) => ({ ...v, x: d.x + dx, y: d.y + dy }));
  };
  const onPointerUp = (): void => {
    const d = drag.current;
    drag.current = null;
    // A plain click on the backdrop (not the image, no drag) closes the viewer.
    if (d && !d.moved && d.backdrop) onClose();
  };
  const onDoubleClick = (e: React.MouseEvent<HTMLDivElement>): void => {
    const fit = fitView();
    if (!fit) return;
    if (Math.abs(view.scale - fit.scale) > 1e-3) {
      setView(fit);
    } else {
      const r = e.currentTarget.getBoundingClientRect();
      zoomAt(Math.max(1, fit.scale * 2) / view.scale, e.clientX - r.left, e.clientY - r.top);
    }
  };

  return createPortal(
    <div className="zoom-viewer" role="dialog" aria-modal="true" aria-label={`${alt} 放大查看`}>
      <div
        ref={stageRef}
        className="zoom-viewer-stage"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onDoubleClick={onDoubleClick}
      >
        <img
          src={src}
          alt={alt}
          draggable={false}
          onLoad={(e) => setNatural({ w: e.currentTarget.naturalWidth, h: e.currentTarget.naturalHeight })}
          style={{
            width: natural ? natural.w * view.scale : undefined,
            height: natural ? natural.h * view.scale : undefined,
            transform: `translate(${view.x}px, ${view.y}px)`,
            visibility: natural ? "visible" : "hidden",
          }}
        />
      </div>
      <div className="zoom-viewer-toolbar">
        <button type="button" onClick={() => zoomCenter(1 / WHEEL_STEP)} aria-label="缩小">−</button>
        <span className="zoom-viewer-pct">{Math.round(view.scale * 100)}%</span>
        <button type="button" onClick={() => zoomCenter(WHEEL_STEP)} aria-label="放大">+</button>
        <button type="button" onClick={reset}>适应</button>
        <button type="button" onClick={() => natural && zoomCenter(1 / view.scale)}>1:1</button>
        <button type="button" onClick={onClose} aria-label="关闭">✕</button>
      </div>
    </div>,
    document.body,
  );
}
