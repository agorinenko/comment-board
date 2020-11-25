from abc import ABC, abstractmethod
from typing import Any

from aiohttp.web_response import Response

from api.schemas.base_schema import BaseSchema


class BaseResponse(ABC):
    """
    Base abstract response
    """

    def __init__(self, schema: BaseSchema):
        if schema is None:
            raise ValueError("Schema is required")
        self.schema = schema

    @abstractmethod
    def get_response(self, data: Any, *args, **kwargs) -> Response:
        """
         Get aiohttp response object
        :param data: The object to serialize.
        :param args:
        :param kwargs:
        :return: A response of serialized data
        """
        raise NotImplementedError()
