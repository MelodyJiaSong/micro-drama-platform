import asyncio
import uvicorn

from projects.suno_browser_service.apps.api.app_factory import create_app


async def serve() -> None:
    app = create_app()
    container = app.state.container
    settings = container.settings()
    runtime = container.runtime()
    config = uvicorn.Config(app, host="127.0.0.1", port=settings.port, workers=1, ws="none")
    socket = config.bind_socket()
    server = uvicorn.Server(config)

    async def watch() -> None:
        while not server.should_exit:
            if server.started and runtime.shutdown_requested():
                runtime.stop_event.set()
                while runtime.thread and runtime.thread.is_alive():
                    await asyncio.sleep(0.25)
                server.should_exit = True
                return
            await asyncio.sleep(0.5)

    watcher = asyncio.create_task(watch())
    try:
        await server.serve(sockets=[socket])
    finally:
        watcher.cancel()
        socket.close()


if __name__ == "__main__":
    asyncio.run(serve())
