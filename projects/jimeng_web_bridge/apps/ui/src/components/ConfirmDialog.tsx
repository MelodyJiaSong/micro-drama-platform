import { type ReactNode, useRef } from "react";
import { Modal } from "./Modal";

interface ConfirmDialogProps {
  title: string;
  description: ReactNode;
  confirmLabel: string;
  cancelLabel: string;
  onConfirm: () => void;
  onCancel: () => void;
  returnFocus?: () => HTMLElement | null;
}

/** Two-step confirmation for credit-spending / site-changing / file-moving actions: focus starts on the safe option, Escape = safe. */
export function ConfirmDialog({ title, description, confirmLabel, cancelLabel, onConfirm, onCancel, returnFocus }: ConfirmDialogProps) {
  const safeRef = useRef<HTMLButtonElement>(null);
  return (
    <Modal role="alertdialog" title={title} description={description} initialFocusRef={safeRef} onDismiss={onCancel} returnFocus={returnFocus}>
      <div className="modal-actions">
        <button type="button" ref={safeRef} onClick={onCancel}>
          {cancelLabel}
        </button>
        <button type="button" className="danger" onClick={onConfirm}>
          {confirmLabel}
        </button>
      </div>
    </Modal>
  );
}
