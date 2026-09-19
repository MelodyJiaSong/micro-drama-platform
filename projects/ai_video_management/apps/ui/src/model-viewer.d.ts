/** JSX typing for the <model-viewer> custom element (@google/model-viewer).

Custom elements are invisible to tsc, so the one attribute set we actually use is
declared here rather than falling back to `any` on the whole element.
*/
import type { DetailedHTMLProps, HTMLAttributes } from "react";

interface ModelViewerAttributes
  extends DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement> {
  src?: string;
  alt?: string;
  "camera-controls"?: boolean;
  "touch-action"?: string;
  "shadow-intensity"?: string;
  exposure?: string;
  "environment-image"?: string;
  "ar-status"?: string;
  /** "eager" | "lazy" | "auto" — lazy keeps a card full of meshes from fetching
   *  every MB before the user scrolls to it. */
  loading?: string;
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "model-viewer": ModelViewerAttributes;
    }
  }
}
