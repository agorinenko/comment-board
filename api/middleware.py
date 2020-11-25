import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPError

from api.views.base_api_view import BaseApiView


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except HTTPError as ex:
        logger = BaseApiView.logger(request)
        logger.info(ex)

        details = ex.body.decode() if ex.body is not None else str(ex)
        try:
            details = json.loads(details)
        except json.decoder.JSONDecodeError:
            pass

        data = {
            "details": details
        }
        return web.json_response(data, status=ex.status)
    except Exception as ex:
        logger = BaseApiView.logger(request)
        logger.exception(ex)

        data = {
            "details": "Unexpected error"
        }
        return web.json_response(data, status=500)
