import { useRef } from "react";
import { Modal } from "./Modal";

interface ConflictDialogProps {
  location: string;
  onReload: () => void;
  onKeepEditing: () => void;
}

export function ConflictDialog({ location, onReload, onKeepEditing }: ConflictDialogProps) {
  const keepRef = useRef<HTMLButtonElement>(null);
  return (
    <Modal
      role="dialog"
      title="文件已在别处被修改"
      description={
        <p>
          <code>{location}</code> 在你读取之后被改动过，这次保存没有写入。可以重新加载最新内容（会丢弃你未保存的修改），或者继续编辑、稍后再处理。
        </p>
      }
      initialFocusRef={keepRef}
      onDismiss={onKeepEditing}
    >
      <div className="modal-actions">
        <button type="button" ref={keepRef} onClick={onKeepEditing}>
          继续编辑
        </button>
        <button type="button" onClick={onReload}>
          重新加载（放弃我的修改）
        </button>
      </div>
    </Modal>
  );
}
