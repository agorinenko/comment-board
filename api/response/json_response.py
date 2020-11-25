from typing import Any

from aiohttp import web
from aiohttp.web_response import Response

from api.response.base_response import BaseResponse


class JsonResponse(BaseResponse):
    """
    Json response
    """

    def get_response(self, data: Any, *args, **kwargs) -> Response:
        dump = self.schema.dump(data)

        if len(kwargs) > 0:
            dump = {
                "results": dump
            }

            dump = {**kwargs, **dump}

        return web.json_response(dump)
