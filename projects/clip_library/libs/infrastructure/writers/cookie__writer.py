from pathlib import Path

from libs.common.options import COOKIES_FILE
from libs.infrastructure.daos.cookie__dao import CookieDao


class CookieWriter:
    def write(self, cookies: list[CookieDao]) -> Path:
        rows = ["# Netscape HTTP Cookie File"]
        for c in cookies:
            rows.append("\t".join([c.domain, "TRUE" if c.domain.startswith(".") else "FALSE", c.path,
                                   "TRUE" if c.secure else "FALSE", str(c.expires), c.name, c.value]))
        COOKIES_FILE.parent.mkdir(parents=True, exist_ok=True)
        COOKIES_FILE.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return COOKIES_FILE
