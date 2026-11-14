from dependency_injector import containers, providers

from libs.application.commands.clip__command import ClipCommand
from libs.application.commands.session__command import SessionCommand
from libs.application.commands.source__command import SourceCommand
from libs.application.mappers.clip__mapper import ClipMapper
from libs.application.mappers.source__mapper import SourceMapper
from libs.application.queries.source__query import SourceQuery
from libs.common.options import DEFAULT_LIBRARY
from libs.infrastructure.clients.chrome__client import ChromeClient
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.clients.ytdlp__client import YtdlpClient
from libs.infrastructure.readers.source__reader import SourceReader
from libs.infrastructure.readers.subtitle__reader import SubtitleReader
from libs.infrastructure.readers.youtube__reader import YoutubeReader
from libs.infrastructure.writers.clip__writer import ClipWriter
from libs.infrastructure.writers.cookie__writer import CookieWriter
from libs.infrastructure.writers.source__writer import SourceWriter


class LibraryContainer(containers.DeclarativeContainer):
    library = providers.Object(DEFAULT_LIBRARY)
    process = providers.Singleton(ProcessClient)
    ytdlp = providers.Singleton(YtdlpClient, process)
    ffmpeg = providers.Singleton(FfmpegClient, process)
    youtube = providers.Singleton(YoutubeReader, ytdlp)
    sources = providers.Singleton(SourceReader, library)
    subtitles = providers.Singleton(SubtitleReader)
    source_writer = providers.Singleton(SourceWriter, library, ytdlp)
    clip_writer = providers.Singleton(ClipWriter, library, ffmpeg)
    source_mapper = providers.Singleton(SourceMapper)
    clip_mapper = providers.Singleton(ClipMapper)
    source_query = providers.Factory(SourceQuery, youtube, sources, subtitles, source_mapper)
    source_command = providers.Factory(SourceCommand, youtube, sources, source_writer, source_mapper)
    clip_command = providers.Factory(ClipCommand, sources, subtitles, clip_writer, source_mapper, clip_mapper)
    chrome = providers.Singleton(ChromeClient)
    cookie_writer = providers.Singleton(CookieWriter)
    session_command = providers.Factory(SessionCommand, chrome, cookie_writer)
