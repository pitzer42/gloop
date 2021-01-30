""" This module contains features that can be pluged in an aiohttp Web Application. Features may be defined in one of the following ways:

    HTTP Handlers
        Classic HTTP Handler functions or Class based views that are executed in a route

    Plugins
        Functions that extends a aiohttp Web App life-cycle. By convention a plugin module has a install function that receives an aiohttp web app.

"""