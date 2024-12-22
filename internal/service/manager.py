from typing import List, Optional

# Определяем класс DTO для менеджера
class ManagerDTO:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

# Интерфейс для доменного менеджера
class DomainManager:
    def get_user_data(self, login: str, password: str) -> Optional[ManagerDTO]:
        raise NotImplementedError

    def change_manager_data(self, manager: ManagerDTO) -> None:
        raise NotImplementedError

    def get_all_managers(self) -> List[ManagerDTO]:
        raise NotImplementedError

    def add_manager(self, manager: ManagerDTO) -> None:
        raise NotImplementedError

    def change_active(self, id: int) -> None:
        raise NotImplementedError

    def change_full_access(self, id: int) -> None:
        raise NotImplementedError

# Реализация менеджера
class Manager:
    def __init__(self, domain_manager: DomainManager):
        self.dm = domain_manager

    def change_full_access(self, id: int) -> None:
        self.dm.change_full_access(id)

    def change_active(self, id: int) -> None:
        self.dm.change_active(id)

    def add_manager(self, manager: ManagerDTO) -> None:
        self.dm.add_manager(manager)

    def get_all_managers(self) -> List[ManagerDTO]:
        return self.dm.get_all_managers()

    def get_user_data(self, login: str, password: str) -> Optional[ManagerDTO]:
        return self.dm.get_user_data(login, password)

    def change_manager_data(self, manager: ManagerDTO) -> None:
        self.dm.change_manager_data(manager)

# Пример реализации доменного менеджера
class MockDomainManager(DomainManager):
    def __init__(self):
        self.managers = []

    def get_user_data(self, login: str, password: str) -> Optional[ManagerDTO]:
        for manager in self.managers:
            if manager.name == login:  # Упрощенная проверка
                return manager
        return None

    def change_manager_data(self, manager: ManagerDTO) -> None:
        for idx, m in enumerate(self.managers):
            if m.id == manager.id:
                self.managers[idx] = manager

    def get_all_managers(self) -> List[ManagerDTO]:
        return self.managers

    def add_manager(self, manager: ManagerDTO) -> None:
        self.managers.append(manager)

    def change_active(self, id: int) -> None:
        print(f"Manager with ID {id} is now active.")

    def change_full_access(self, id: int) -> None:
        print(f"Manager with ID {id} now has full access.")

# Пример использования
if __name__ == "__main__":
    domain_manager_instance = MockDomainManager()
    domain_manager_instance.add_manager(ManagerDTO(1, "Alice"))
    domain_manager_instance.add_manager(ManagerDTO(2, "Bob"))

    manager = Manager(domain_manager_instance)

    # Получаем данные пользователя
    user_data = manager.get_user_data("Alice", "password")
    if user_data:
        print(f"User found: ID: {user_data.id}, Name: {user_data.name}")
    else:
        print("User not found.")

    # Изменяем данные менеджера
    manager.change_manager_data(ManagerDTO(1, "Alice Updated"))

    # Проверяем изменения
    updated_user_data = manager.get_user_data("Alice Updated", "password")
    print(f"Updated User: ID: {updated_user_data.id}, Name: {updated_user_data.name}")

    # Изменяем доступ
    manager.change_full_access(1)
    manager.change_active(2)
