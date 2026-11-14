import argparse
import os
from pathlib import Path
import sys

from dependency_injector import providers

from apps.cli.container import Container
from libs.common.options import BROWSERS, COOKIES_FILE, DEFAULT_LIBRARY, DURATIONS, LIBRARY_ENV, ORDERS, SUB_LANGS, LicenseKind
from libs.common.types import Auth


def _clock(seconds: float) -> str:
    whole = int(seconds)
    return f"{whole // 3600}:{whole // 60 % 60:02}:{whole % 60:02}.{int(seconds * 1000) % 1000:03}"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YouTube 素材库：按授权搜索、下载、字幕检索、截取片段")
    parser.add_argument("--library", default=os.environ.get(LIBRARY_ENV, str(DEFAULT_LIBRARY)))
    parser.add_argument("--browser", choices=BROWSERS, default="", help="用本机浏览器登录（YouTube 要求验证时）")
    parser.add_argument("--cookies", default="", help="Netscape 格式 cookies 文件（默认用 login 导出的）")
    sub = parser.add_subparsers(dest="action", required=True)

    def search_options(target: argparse.ArgumentParser) -> None:
        target.add_argument("--limit", type=int, default=20)
        target.add_argument("--duration", choices=list(DURATIONS), default="any")
        target.add_argument("--order", choices=list(ORDERS), default="relevance")
        target.add_argument("--all-licenses", action="store_true", help="不限 CC 授权")

    search = sub.add_parser("search", help="搜索 YouTube，默认只看 CC 授权")
    search.add_argument("query")
    search_options(search)
    download = sub.add_parser("download", help="下载到素材库（视频 + 字幕 + 授权记录）")
    download.add_argument("urls", nargs="*")
    download.add_argument("--file", default="", help="每行一个链接")
    download.add_argument("--search", default="", help="直接下载搜索结果")
    search_options(download)
    download.add_argument("--license", choices=[kind.value for kind in LicenseKind], default="",
                          help="不填则自动：平台标 CC 记 cc_by，否则记 quote")
    download.add_argument("--note", default="", help="授权依据；permission / public_domain 必填")
    download.add_argument("--sub-langs", default=SUB_LANGS)
    sub.add_parser("login", help="开独立 Chrome 登录 YouTube，关窗后导出登录状态")
    sub.add_parser("list", help="列出素材库")
    find = sub.add_parser("find", help="在字幕里找原话")
    find.add_argument("keyword")
    find.add_argument("--source", default="")
    find.add_argument("--limit", type=int, default=50)
    cut = sub.add_parser("cut", help="截取片段，默认 9:16 + 出处卡")
    cut.add_argument("source")
    cut.add_argument("start")
    cut.add_argument("end")
    cut.add_argument("--horizontal", action="store_true")
    return parser


def _run(args: argparse.Namespace, container: Container) -> int:
    cookies = args.cookies or (str(COOKIES_FILE) if not args.browser and COOKIES_FILE.is_file() else "")
    auth = Auth(args.browser, cookies)
    if args.action == "login":
        session = container.session_command().login(print)
        print(f"已导出 {session.cookie_count} 条登录 cookies：")
        print(session.cookies_file)
    elif args.action == "search":
        for hit in container.source_query().search(args.query, args.limit, args.duration, args.order,
                                                   not args.all_licenses, auth):
            print(f"{hit.url}  {_clock(hit.duration)}  {hit.view_count:>10,}  {hit.channel} | {hit.title}")
    elif args.action == "download":
        claimed = LicenseKind(args.license) if args.license else None
        command = container.source_command()
        if args.search:
            result = command.download_search(args.search, args.limit, args.duration, args.order,
                                             not args.all_licenses, claimed, args.note, args.sub_langs, auth, print)
        else:
            urls = list(args.urls)
            if args.file:
                urls += [line.strip() for line in Path(args.file).read_text(encoding="utf-8").splitlines()
                         if line.strip() and not line.startswith("#")]
            result = command.download(urls, claimed, args.note, args.sub_langs, auth, print)
        failed = [item for item in result.items if item.status == "失败"]
        print(f"\n共 {len(result.items)} 条，失败 {len(failed)} 条")
        for item in failed:
            print(f"✗ {item.url}\n  {item.message}")
        return 1 if failed else 0
    elif args.action == "list":
        for row in container.source_query().library():
            print(f"{row.video_id}  {_clock(row.duration)}  {row.license_label}  字幕:{','.join(row.subtitle_languages) or '无'}"
                  f"  {row.channel} | {row.title}\n    {row.folder}")
    elif args.action == "find":
        for hit in container.source_query().find(args.keyword, args.source, args.limit):
            print(f"{hit.source_id}  {_clock(hit.start)} → {_clock(hit.end)}  [{hit.language}]  {hit.text}")
    else:
        result = container.clip_command().cut(args.source, args.start, args.end, not args.horizontal)
        print(f"{result.seconds:.1f}s · {result.license_label}\n{result.file}", *result.subtitles, sep="\n")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = _parser().parse_args()
    container = Container()
    container.library.override(providers.Object(Path(args.library)))
    container.wire(modules=[__name__])
    try:
        return _run(args, container)
    except Exception as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
