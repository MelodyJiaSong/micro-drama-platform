import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "../src/App";
import { ErrorBoundary } from "../src/components/ErrorBoundary";
import { parseErrorBody } from "../src/api";

function Boom(): never {
  throw new Error("解析失败");
}

describe("app shell", () => {
  it("renders all seven pages in the navigation", () => {
    render(
      <MemoryRouter initialEntries={["/queue"]}>
        <App />
      </MemoryRouter>,
    );
    for (const title of ["会话", "剧 config", "批次确认", "队列看板", "历史与积分", "主体对账", "全局设置"]) {
      expect(screen.getByRole("link", { name: title })).toBeInTheDocument();
    }
    expect(screen.getByRole("heading", { name: "队列看板" })).toBeInTheDocument();
  });

  it("shows an accessible error with retry instead of a blank page when a page throws", async () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => undefined);
    render(
      <ErrorBoundary pageTitle="队列看板">
        <Boom />
      </ErrorBoundary>,
    );
    expect(screen.getByRole("alert")).toHaveTextContent("解析失败");
    await userEvent.click(screen.getByRole("button", { name: "重试" }));
    spy.mockRestore();
  });
});

describe("parseErrorBody", () => {
  it("keeps the business error envelope", () => {
    expect(parseErrorBody(409, { error_code: "config_conflict", message: "文件已被修改", hint: "重新加载", config_key: null })).toEqual({
      error_code: "config_conflict",
      message: "文件已被修改",
      hint: "重新加载",
      config_key: null,
    });
  });

  it("falls back for non-envelope bodies", () => {
    expect(parseErrorBody(502, "<html>")).toEqual({ error_code: "http_502", message: "请求失败（HTTP 502）", hint: null, config_key: null });
  });
});
