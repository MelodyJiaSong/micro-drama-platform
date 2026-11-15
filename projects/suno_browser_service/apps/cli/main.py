import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from projects.suno_browser_service.libs.application.commands.agent__command import AgentCommand
from projects.suno_browser_service.libs.application.queries.agent__query import AgentQuery
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import GenerationRequest
from pydantic import ValidationError


def main() -> int:
    parser = argparse.ArgumentParser(description="Suno JSON CLI for Kimi Code, Codex and shell programs. Token stays in local storage.")
    subs = parser.add_subparsers(dest="action", required=True)
    for action in ("capabilities", "schema", "list"):
        subs.add_parser(action)
    for action in ("plan", "create"):
        command = subs.add_parser(action)
        command.add_argument("--file", required=True, help="UTF-8 request JSON; '-' reads stdin")
        if action == "create":
            command.add_argument("--key", required=True, help="Stable idempotency key; reuse after network timeout")
    upload = subs.add_parser("upload")
    upload.add_argument("--file", required=True)
    upload.add_argument("--rights-confirmed", action="store_true")
    for action in ("get", "wait", "resume", "cancel", "download"):
        command = subs.add_parser(action)
        command.add_argument("--job", required=True)
        if action == "wait":
            command.add_argument("--seconds", type=int, default=45)
        if action == "resume":
            command.add_argument("--file", required=True, help="JSON object with song_urls or recollect=true; never regenerates uncertain jobs")
        if action == "download":
            command.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.action == "schema":
            result = GenerationRequest.model_json_schema()
        else:
            agent = AgentQuery() if args.action in {"capabilities", "plan", "get", "list", "wait"} else AgentCommand()
            if args.action in {"plan", "create", "resume"}:
                data = json.loads(sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8-sig"))
            match args.action:
                case "capabilities": result = agent.capabilities()
                case "list": result = agent.list()
                case "plan": result = agent.plan(GenerationRequest.model_validate(data))
                case "create": result = agent.create(GenerationRequest.model_validate(data), args.key)
                case "upload": result = agent.upload(args.file, args.rights_confirmed)
                case "get": result = agent.get(args.job)
                case "wait": result = agent.wait(args.job, args.seconds)
                case "resume": result = agent.resume(args.job, data.get("song_urls", []), bool(data.get("recollect", False)))
                case "cancel": result = agent.cancel(args.job)
                case "download": result = agent.download(args.job, args.output)
        print(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
        return 0
    except (ServiceError, ValidationError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": {"code": getattr(exc, "code", "invalid_input"), "message": str(exc)}}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
