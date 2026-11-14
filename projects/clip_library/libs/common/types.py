from dataclasses import dataclass


@dataclass(frozen=True)
class Auth:
    browser: str = ""
    cookies: str = ""

    def arguments(self) -> list[str]:
        if self.cookies:
            return ["--cookies", self.cookies]
        if self.browser:
            return ["--cookies-from-browser", self.browser]
        return []
