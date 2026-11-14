from dependency_injector import containers, providers

from projects.suno_browser_service.libs.application.commands.job__command import JobCommand
from projects.suno_browser_service.libs.application.commands.runtime__command import RuntimeCommand
from projects.suno_browser_service.libs.application.queries.auth__query import AuthQuery
from projects.suno_browser_service.libs.application.queries.job__query import JobQuery
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.application.queries.capability__query import CapabilityQuery
from projects.suno_browser_service.libs.application.commands.asset__command import AssetCommand


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings.from_env)
    auth = providers.Singleton(AuthQuery, settings)
    query = providers.Singleton(JobQuery, settings)
    command = providers.Singleton(JobCommand, settings)
    runtime = providers.Singleton(RuntimeCommand, settings)
    capabilities = providers.Singleton(CapabilityQuery, settings)
    assets = providers.Singleton(AssetCommand, settings)
