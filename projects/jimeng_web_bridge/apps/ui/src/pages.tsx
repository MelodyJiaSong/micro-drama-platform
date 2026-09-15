import type { ComponentType } from "react";

export interface PageDef {
  path: string;
  title: string;
  Component: ComponentType;
}

function placeholder(title: string): ComponentType {
  return function PlaceholderPage() {
    return (
      <section>
        <h1 tabIndex={-1}>{title}</h1>
        <p>页面开发中。</p>
      </section>
    );
  };
}

export const PAGES: PageDef[] = [
  { path: "/", title: "会话", Component: placeholder("会话") },
  { path: "/dramas", title: "剧 config", Component: placeholder("剧 config") },
  { path: "/batches/:batchId", title: "批次确认", Component: placeholder("批次确认") },
  { path: "/queue", title: "队列看板", Component: placeholder("队列看板") },
  { path: "/history", title: "历史与积分", Component: placeholder("历史与积分") },
  { path: "/entities", title: "主体对账", Component: placeholder("主体对账") },
  { path: "/settings", title: "全局设置", Component: placeholder("全局设置") },
];
