class ScriptReader:
    def read(self, path: str | None) -> str:
        if path is None:
            return ""
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
