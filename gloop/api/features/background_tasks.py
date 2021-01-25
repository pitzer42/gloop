import asyncio

__KEY__ = __name__


def install(app):
    app[__KEY__] = []
    app.on_cleanup.append(cancel_background_tasks)


def create_background_task(app, coroutine):
    task = asyncio.create_task(coroutine)
    app[__KEY__].append(task)


async def cancel_background_tasks(app):
    for task in app[__KEY__]:
        task.cancel()
        await task
