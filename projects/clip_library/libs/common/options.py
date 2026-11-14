from enum import StrEnum
import os
from pathlib import Path


class LicenseKind(StrEnum):
    CC_BY = "cc_by"
    PERMISSION = "permission"
    PUBLIC_DOMAIN = "public_domain"
    QUOTE = "quote"


LICENSE_LABELS: dict[LicenseKind, str] = {
    LicenseKind.CC_BY: "CC BY 授权",
    LicenseKind.PERMISSION: "已获作者许可",
    LicenseKind.PUBLIC_DOMAIN: "公有领域",
    LicenseKind.QUOTE: "引用（未授权）",
}
EVIDENCE_REQUIRED: frozenset[LicenseKind] = frozenset({LicenseKind.PERMISSION, LicenseKind.PUBLIC_DOMAIN})
QUOTE_MAX_SECONDS = 10.0
CC_MARKER = "Creative Commons"

LIBRARY_ENV = "CLIP_LIBRARY_DIR"
DEFAULT_LIBRARY = Path(__file__).resolve().parents[2] / "library"
SOURCES_DIR = "sources"
CLIPS_DIR = "clips"
SOURCE_RECORD = "source.json"
INFO_FILE = "info.json"
CLIP_LEDGER = "clips.jsonl"
VIDEO_STEM = "video"

SUB_LANGS = "en,zh-Hans,zh-Hant,zh"
MAX_HEIGHT = 1080
BROWSERS = ("edge", "firefox", "chrome", "brave")
DURATIONS: dict[str, int] = {"any": 0, "short": 1, "long": 2, "medium": 3}
ORDERS: dict[str, int] = {"relevance": 0, "date": 2, "views": 3}
BATCH_SLEEP = (3, 8)

SESSION_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "clip_library"
CHROME_PROFILE = SESSION_DIR / "chrome_profile"
COOKIES_FILE = SESSION_DIR / "cookies.txt"
CHROME_PATHS = (Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
                Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))
LOGIN_URL = "https://accounts.google.com/ServiceLogin?service=youtube&continue=https%3A%2F%2Fwww.youtube.com%2F"
COOKIE_DOMAINS = ("youtube.com", "google.com")
LOGIN_COOKIES = frozenset({"SAPISID", "__Secure-3PSID", "LOGIN_INFO"})

FONT_FILES = (Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf"))
VERTICAL_SIZE = (1080, 1920)
