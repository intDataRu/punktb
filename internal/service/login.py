from typing import Protocol, Optional
from .domain import Login as DomainLogin
from .dto import Manager

class Login(Protocol):
    def login(self, login: str, password: str) -> Optional[Manager]:
        ...

class LoginService:
    def __init__(self, dm: DomainLogin) -> None:
        self.dm = dm

    def login(self, login: str, password: str) -> Optional[Manager]:
        manager = self.dm.login(login, password)
        return manager
