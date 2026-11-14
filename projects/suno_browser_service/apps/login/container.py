from dependency_injector import containers, providers

from projects.suno_browser_service.libs.application.commands.session__command import SessionCommand
from projects.suno_browser_service.libs.common.settings import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings.from_env)
    session = providers.Singleton(SessionCommand, settings)
