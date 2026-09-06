import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { Rich } from "../src/components/ResearchText";

const html = (text: string): string => renderToStaticMarkup(<Rich text={text} />);

describe("Rich", () => {
  it("renders **bold** as <strong> instead of literal asterisks", () => {
    const out = html("回报好 **两项都要过** 才算");
    expect(out).toContain("<strong>两项都要过</strong>");
    expect(out).not.toContain("**");
  });

  it("renders `code` spans", () => {
    expect(html("见 `verifier_ip_flag` 字段")).toContain("<code>verifier_ip_flag</code>");
  });

  it("leaves plain prose untouched", () => {
    expect(html("没有任何标记")).toContain("没有任何标记");
  });

  it("handles several markers in one string", () => {
    const out = html("**A** 与 **B** 都要看 `c`");
    expect(out).toContain("<strong>A</strong>");
    expect(out).toContain("<strong>B</strong>");
    expect(out).toContain("<code>c</code>");
  });

  it("does not treat a lone asterisk or hash as markup", () => {
    const out = html("成本 3*5 小时 # 备注");
    expect(out).toContain("3*5");
    expect(out).toContain("# 备注");
  });
});
