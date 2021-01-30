"""
    Execute background tasks along with your aiohttp web app. New tasks are 
    created with create_background_task and all background tasks created this
    way are properly canceled during the appliction clean up.
"""

import asyncio
from aiohttp.web import Application

__KEY__ = __name__


def install(app: Application):
    """
        Install background_tasks plugin on the aiohttp web app
    """
    app[__KEY__] = []
    app.on_cleanup.append(cancel_background_tasks)


def create_background_task(app: Application, coroutine):
    """
        Create a background task from the given coroutine. This task will be
        automatically canceled during the Application Clean-up.
    """
    task = asyncio.create_task(coroutine)
    app[__KEY__].append(task)


async def cancel_background_tasks(app: Application):
    """
        Cancel all the background tasks created with create_background_task function
    """
    for task in app[__KEY__]:
        task.cancel()
        await task
