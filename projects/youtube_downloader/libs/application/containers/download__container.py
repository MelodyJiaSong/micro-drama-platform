from dependency_injector import containers, providers

from libs.application.commands.download__command import DownloadCommand
from libs.application.mappers.download__mapper import DownloadMapper
from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.writers.download__writer import DownloadWriter


class DownloadContainer(containers.DeclarativeContainer):
    client = providers.Factory(ProcessClient)
    writer = providers.Factory(DownloadWriter, client=client)
    mapper = providers.Factory(DownloadMapper)
    command = providers.Factory(DownloadCommand, writer=writer, mapper=mapper)
