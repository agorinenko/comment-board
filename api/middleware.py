import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPError


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except HTTPError as ex:
        details = ex.body.decode() if ex.body is not None else str(ex)
        try:
            details = json.loads(details)
        except json.decoder.JSONDecodeError:
            pass

        data = {
            "details": details
        }
        return web.json_response(data, status=ex.status)
