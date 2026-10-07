import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { QuestionWizard, type InterviewQuestion } from "../src/components/QuestionWizard";
import { WritersRoomPage } from "../src/components/WritersRoomPage";

const questions: InterviewQuestion[] = [1, 2, 3].map(i => ({
  id: `q${i}`, title: `问题${i}`, dimension: "行为", multiple: false,
  options: [{value: "A", label: "观察"}, {value: "B", label: "行动"}, {value: "C", label: "求助"}],
}));
const answer = {choice: "A", note: "已保存"};
const deferred = <T,>() => {
  let resolve!: (value: T) => void;
  let reject!: (error: Error) => void;
  const promise = new Promise<T>((ok, fail) => {resolve = ok; reject = fail;});
  return {promise, resolve, reject};
};
afterEach(() => {cleanup(); vi.unstubAllGlobals();});

describe("逐题访谈契约", () => {
  it("保存成功才跳题，等待期间点击和键盘仅提交一次", async () => {
    const pending = deferred<void>();
    const save = vi.fn(() => pending.promise);
    render(<QuestionWizard questions={questions} answers={{}} onSave={save} />);
    fireEvent.click(screen.getByRole("button", {name: "A 观察"}));
    fireEvent.click(screen.getByRole("button", {name: "B 行动"}));
    fireEvent.keyDown(document.body, {key: "C"});
    expect(save).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("heading", {name: "问题1"})).toBeInTheDocument();
    await act(async () => pending.resolve());
    expect(screen.getByRole("heading", {name: "问题2"})).toHaveFocus();
  });

  it("保存失败保留当前题和输入，可重试", async () => {
    const save = vi.fn().mockRejectedValueOnce(new Error("磁盘失败")).mockResolvedValue(undefined);
    render(<QuestionWizard questions={questions} answers={{}} onSave={save} />);
    fireEvent.change(screen.getByRole("textbox"), {target: {value: "补充经历"}});
    fireEvent.click(screen.getByRole("button", {name: "A 观察"}));
    expect(await screen.findByRole("alert")).toHaveTextContent("磁盘失败");
    expect(screen.getByRole("heading", {name: "问题1"})).toBeInTheDocument();
    expect(screen.getByRole("textbox")).toHaveValue("补充经历");
    fireEvent.click(screen.getByRole("button", {name: "B 行动"}));
    await screen.findByRole("heading", {name: "问题2"});
    expect(save).toHaveBeenLastCalledWith("q1", {choice: "B", note: "补充经历"});
  });

  it("按住字母键的 repeat 事件不会回答下一题", async () => {
    const save = vi.fn().mockResolvedValue(undefined);
    render(<QuestionWizard questions={questions} answers={{}} onSave={save} />);
    fireEvent.keyDown(document.body, {key: "a"});
    await screen.findByRole("heading", {name: "问题2"});
    fireEvent.keyDown(document.body, {key: "a", repeat: true});
    await act(async () => {});
    expect(save).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("heading", {name: "问题2"})).toBeInTheDocument();
  });

  it("在文本框、编辑区域或组合键输入时不抢快捷键", () => {
    const save = vi.fn().mockResolvedValue(undefined);
    render(<QuestionWizard questions={questions} answers={{}} onSave={save} />);
    fireEvent.keyDown(screen.getByRole("textbox"), {key: "A"});
    fireEvent.keyDown(document.body, {key: "B", ctrlKey: true});
    const editable = document.createElement("div"); editable.contentEditable = "true";
    editable.setAttribute("contenteditable", "true"); document.body.appendChild(editable);
    fireEvent.keyDown(editable, {key: "C"}); editable.remove();
    expect(save).not.toHaveBeenCalled();
  });

  it("自己填写答案不能为空，保存后才能继续", async () => {
    const save = vi.fn().mockResolvedValue(undefined);
    render(<QuestionWizard questions={questions} answers={{}} onSave={save} />);
    fireEvent.click(screen.getByRole("button", {name: "✎ 写自己的答案"}));
    expect(screen.getByRole("button", {name: "保存并继续 →"})).toBeDisabled();
    fireEvent.change(screen.getByRole("textbox"), {target: {value: "  先护住朋友  "}});
    fireEvent.keyDown(document.body, {key: "A"});
    expect(save).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", {name: "保存并继续 →"}));
    await screen.findByRole("heading", {name: "问题2"});
    expect(save).toHaveBeenCalledWith("q1", {choice: "custom", note: "先护住朋友"});
  });

  it("恢复到首个未答题，并能回退修改已有答案", async () => {
    const save = vi.fn().mockResolvedValue(undefined);
    render(<QuestionWizard questions={questions} answers={{q1: answer, q3: answer}} onSave={save} />);
    expect(screen.getByRole("heading", {name: "问题2"})).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", {name: "← 上一题"}));
    expect(screen.getByRole("textbox")).toHaveValue("已保存");
    fireEvent.click(screen.getByRole("button", {name: "B 行动"}));
    await screen.findByRole("heading", {name: "问题2"});
    expect(save).toHaveBeenCalledWith("q1", {choice: "B", note: "已保存"});
  });
});

const seed = (slug: string) => ({slug, characters: [{id: "a", name: "甲"}, {id: "b", name: "乙"}]});
const detail = (slug: string, revision = 2) => ({seed: seed(slug), questions, answers: {revision, characters: {a: {q1: answer}, b: {q1: answer, q2: answer}}}});
const response = (data: unknown, ok = true) => ({ok, status: ok ? 200 : 409, json: async () => data});

describe("编剧室访谈保存", () => {
  it("切换人物及刷新从各自未答题恢复，PUT 带当前 revision", async () => {
    let persisted = detail("alpha");
    const fetcher = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const next = {revision: 3, characters: {a: {q1: answer, q2: answer}, b: {q1: answer, q2: answer}}};
        persisted = {...persisted, answers: next};
        return response(next);
      }
      return response(url === "/api/writers-room" ? [seed("alpha")] : persisted);
    });
    vi.stubGlobal("fetch", fetcher);
    const view = render(<WritersRoomPage />);
    await screen.findByRole("heading", {name: "问题2"});
    fireEvent.change(screen.getByRole("combobox", {name: "人物"}), {target: {value: "b"}});
    expect(screen.getByRole("heading", {name: "问题3"})).toBeInTheDocument();
    fireEvent.change(screen.getByRole("combobox", {name: "人物"}), {target: {value: "a"}});
    fireEvent.click(screen.getByRole("button", {name: "C 求助"}));
    await screen.findByRole("heading", {name: "问题3"});
    const put = fetcher.mock.calls.find(call => call[1]?.method === "PUT")!;
    expect(JSON.parse(put[1]!.body as string)).toEqual({character: "a", question_id: "q2", choice: "C", note: "", expected_revision: 2});
    view.unmount(); render(<WritersRoomPage />);
    await screen.findByRole("heading", {name: "问题3"});
  });

  it("revision 冲突显示错误且留在当前题", async () => {
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => response(
      init?.method === "PUT" ? {detail: {message: "答案已在另一窗口更新"}} : url === "/api/writers-room" ? [seed("alpha")] : detail("alpha"), init?.method !== "PUT",
    )));
    render(<WritersRoomPage />); await screen.findByRole("heading", {name: "问题2"});
    fireEvent.click(screen.getByRole("button", {name: "A 观察"}));
    expect(await screen.findByRole("alert")).toHaveTextContent("另一窗口更新");
    expect(screen.getByRole("heading", {name: "问题2"})).toBeInTheDocument();
  });

  it("保存期间换剧，迟到的响应不覆盖新剧答案和 revision", async () => {
    const pending = deferred<ReturnType<typeof response>>();
    const fetcher = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "PUT" && url.includes("alpha")) return pending.promise;
      if (init?.method === "PUT") return response({revision: 8, characters: {a: {q1: answer, q2: answer}}});
      return response(url === "/api/writers-room" ? [seed("alpha"), seed("beta")] : detail(url.endsWith("beta") ? "beta" : "alpha", url.endsWith("beta") ? 7 : 2));
    });
    vi.stubGlobal("fetch", fetcher);
    render(<WritersRoomPage />); await screen.findByRole("heading", {name: "问题2"});
    fireEvent.click(screen.getByRole("button", {name: "A 观察"}));
    fireEvent.change(screen.getByRole("combobox", {name: "剧目"}), {target: {value: "beta"}});
    await waitFor(() => expect(screen.getByRole("combobox", {name: "人物"})).toBeInTheDocument());
    await act(async () => pending.resolve(response({revision: 3, characters: {a: {q1: answer, q2: answer}}})));
    fireEvent.click(screen.getByRole("button", {name: "C 求助"}));
    await waitFor(() => expect(fetcher.mock.calls.filter(call => call[1]?.method === "PUT")).toHaveLength(2));
    const last = fetcher.mock.calls.at(-1)!;
    expect(last[0]).toBe("/api/writers-room/beta/answers");
    expect(JSON.parse(last[1]!.body as string).expected_revision).toBe(7);
  });
});
