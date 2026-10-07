"""Static declarations only: no imports, evaluation, environment reads or tool calls."""
from __future__ import annotations

import ast
from typing import Any

from libs.common.config_redaction import redact_config, redact_text


def declaration(value: ast.expr) -> Any:
    try:
        return ast.literal_eval(value)
    except (ValueError, TypeError):
        return {"expression": redact_text(ast.unparse(value))}


def project_defaults(text: str) -> dict[str, Any]:
    module = ast.parse(text)
    values: dict[str, Any] = {}
    if description := ast.get_docstring(module):
        values["SOURCE_GUIDANCE"] = description
    defaults: dict[str, Any] = {}
    cli: list[dict[str, Any]] = []
    environment: set[str] = set()
    for node in ast.walk(module):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id.isupper() and node.value is not None:
                    values[target.id] = declaration(node.value)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            pairs = list(zip([*node.args.posonlyargs, *node.args.args][-len(node.args.defaults):], node.args.defaults)) if node.args.defaults else []
            pairs.extend((arg, value) for arg, value in zip(node.args.kwonlyargs, node.args.kw_defaults) if value is not None)
            if pairs:
                defaults[f"{node.name}@{node.lineno}"] = {arg.arg: declaration(value) for arg, value in pairs}
        if isinstance(node, ast.Call):
            call = ast.unparse(node.func)
            if call.endswith(".add_argument"):
                options = [arg.value for arg in node.args if isinstance(arg, ast.Constant) and isinstance(arg.value, str)]
                for keyword in node.keywords:
                    if keyword.arg == "default":
                        cli.append({"options": options, "default": redact_config(declaration(keyword.value), " ".join(options))})
            if call in {"os.getenv", "os.environ.get", "getenv"} and node.args:
                argument = node.args[0]
                environment.add(argument.value if isinstance(argument, ast.Constant) and isinstance(argument.value, str) else ast.unparse(argument))
    values["FUNCTION_DEFAULTS"] = defaults
    values["CLI_DEFAULTS"] = cli
    values["ENVIRONMENT_NAMES"] = sorted(environment)
    return redact_config(values)
