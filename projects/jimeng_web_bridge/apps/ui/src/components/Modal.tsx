import { type KeyboardEvent, type ReactNode, type RefObject, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";

const FOCUSABLE = 'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

export interface ModalProps {
  role: "dialog" | "alertdialog";
  title: string;
  description?: ReactNode;
  children?: ReactNode;
  initialFocusRef: RefObject<HTMLElement>;
  onDismiss: () => void;
  returnFocus?: () => HTMLElement | null;
}

export function Modal({ role, title, description, children, initialFocusRef, onDismiss, returnFocus }: ModalProps) {
  const titleId = useId();
  const descriptionId = useId();
  const [host] = useState(() => document.createElement("div"));
  const [opener] = useState(() => (document.activeElement instanceof HTMLElement ? document.activeElement : null));

  useEffect(() => {
    document.body.appendChild(host);
    const siblings = Array.from(document.body.children).filter((node) => node !== host && !node.hasAttribute("inert"));
    siblings.forEach((node) => node.setAttribute("inert", ""));
    initialFocusRef.current?.focus();
    return () => {
      siblings.forEach((node) => node.removeAttribute("inert"));
      host.remove();
      const target = opener?.isConnected ? opener : returnFocus?.() ?? null;
      target?.focus();
    };
  }, []);

  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      onDismiss();
      return;
    }
    if (event.key !== "Tab") return;
    const focusables = Array.from(event.currentTarget.querySelectorAll<HTMLElement>(FOCUSABLE));
    if (focusables.length === 0) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  return createPortal(
    <div className="modal-backdrop">
      <div
        role={role}
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={description ? descriptionId : undefined}
        className={`modal modal-${role}`}
        onKeyDown={onKeyDown}
      >
        <h2 id={titleId}>{title}</h2>
        {description ? (
          <div id={descriptionId} className="modal-description">
            {description}
          </div>
        ) : null}
        {children}
      </div>
    </div>,
    host,
  );
}
