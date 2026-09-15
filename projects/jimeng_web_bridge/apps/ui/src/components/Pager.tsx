interface PagerProps {
  page: number;
  pageSize: number;
  total: number;
  onPage: (page: number) => void;
}

export function Pager({ page, pageSize, total, onPage }: PagerProps) {
  const pages = Math.max(1, Math.ceil(total / Math.max(1, pageSize)));
  if (pages <= 1) return null;
  return (
    <nav aria-label="分页" className="toolbar">
      <button type="button" aria-disabled={page <= 1} onClick={() => page > 1 && onPage(page - 1)}>
        上一页
      </button>
      <span>
        第 {page} / {pages} 页（共 {total} 条）
      </span>
      <button type="button" aria-disabled={page >= pages} onClick={() => page < pages && onPage(page + 1)}>
        下一页
      </button>
    </nav>
  );
}
