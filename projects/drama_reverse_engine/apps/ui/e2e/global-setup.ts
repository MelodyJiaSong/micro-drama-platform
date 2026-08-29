import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const WS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../.e2e_ws");

function write(rel: string, content: string) {
  const full = path.join(WS, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, "utf-8");
}

export default function globalSetup() {
  fs.rmSync(WS, { recursive: true, force: true });
  write("seed1/drama.json", JSON.stringify({
    drama_id: "seed1", title: "种子剧", gate_a_enabled: false, gate_b_enabled: false,
  }));
  write("seed1/authorization_stub.json", JSON.stringify({
    declaration_version: "v1", declared_by: "e2e", ts: "2026-07-15T00:00:00Z", sha256: "seed",
  }));
  write("seed1/ep01/pipeline_state.json", JSON.stringify({
    stage: "done", failed_reason: null, gate_hold: false, needs_recompose: false,
  }));
  write("seed1/ep01/script.md", "# 剧本（逐字忠实原片）\n\n> 裴远：「你还敢回来？」\n");
  write("seed1/ep01/dialogue.md", "# 台词表\n\n- [镜01] 裴远：「你还敢回来？」\n");
  write("seed1/ep01/novel.md", "# 第一章\n\n他回来了。\n");
  write("seed1/ep01/all_shot_prompts.md", "# 全镜 prompt 汇总\n\n## shot01\n\n```text\n情节: 测试\n```\n");
  write("seed1/ep01/compose_manifest.json", JSON.stringify({
    shot_files: ["seed1/ep01/shots/shot01/shot01.md"], novel_rel_path: "seed1/ep01/novel.md", degradations: [],
  }));
  write("seed1/ep01/shots/shot01/shot01.md", "---\nshot: 1\n---\n\n# shot01\n\n## 视频 prompt\n\n```text\n情节: 测试\n```\n");
}
