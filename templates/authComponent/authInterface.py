from abc import ABC, abstractmethod
from flask import Request, Response

class AuthInterface(ABC):

    @abstractmethod
    def register(self, request: Request) -> Response:
        pass

    @abstractmethod
    def login(self, request: Request) -> Response:
        pass

    @abstractmethod
    def logout(self) -> Response:
        pass