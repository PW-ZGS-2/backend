from abc import abstractmethod, ABC

from pydantic import BaseModel


class RestResponse(BaseModel, ABC):
    pass

class RestRequest(BaseModel, ABC):
    pass

class DefaultHandler(ABC):
    @abstractmethod
    def run(self, request: RestResponse) -> RestResponse:
        pass
