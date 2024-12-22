from typing import List, Protocol, Optional
from .domain import Client as DomainClient
from .dto import Client as DTOClient

class Client(Protocol):
    def get_clients(self, id: int, is_admin: bool) -> List[DTOClient]:
        ...

    def set_client_checked(self, id: int) -> None:
        ...

    def set_client_archive(self, id: int) -> None:
        ...

    def add_result(self, client: DTOClient) -> None:
        ...

    def get_result_client(self, id: int) -> Optional[DTOClient]:
        ...

class ClientService:
    def __init__(self, dm: DomainClient) -> None:
        self.dm = dm

    def get_clients(self, id: int, is_admin: bool) -> List[DTOClient]:
        clients = self.dm.get_clients(id, is_admin)
        return clients

    def set_client_checked(self, id: int) -> None:
        self.dm.set_client_checked(id)

    def set_client_archive(self, id: int) -> None:
        self.dm.set_client_archive(id)

    def add_result(self, client: DTOClient) -> None:
        self.dm.add_result(client)

    def get_result_client(self, id: int) -> Optional[DTOClient]:
        client = self.dm.get_result_client(id)
        return client
