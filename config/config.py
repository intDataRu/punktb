import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

@dataclass
class HTTP:
    is_https: bool
    server_cert_path: str
    private_key_path: str

@dataclass
class DBConfig:
    port: str
    host: str
    username: str
    database: str
    password: str

@dataclass
class Config:
    log_level: str = os.getenv("LOG_LEVEL", "debug")
    http: HTTP = HTTP(
        is_https=bool(os.getenv("IS_HTTPS")),
        server_cert_path=os.getenv("SERVER_CERT_PATH"),
        private_key_path=os.getenv("PRIVATE_KEY_PATH"),
    )
    postgresql: DBConfig = DBConfig(
        port=os.getenv("PSQL_PORT"),
        host=os.getenv("PSQL_HOST"),
        username=os.getenv("PSQL_USERNAME"),
        database=os.getenv("PSQL_DATABASE"),
        password=os.getenv("PSQL_PASSWORD"),
    )

# Глобальная переменная для хранения экземпляра конфигурации
_config_instance = None

def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
        # Проверка обязательных полей
        if not _config_instance.http.server_cert_path or not _config_instance.http.private_key_path:
            raise ValueError("SERVER_CERT_PATH and PRIVATE_KEY_PATH are required.")
        if not all([_config_instance.postgresql.port, _config_instance.postgresql.host,
                    _config_instance.postgresql.username, _config_instance.postgresql.database,
                    _config_instance.postgresql.password]):
            raise ValueError("All PostgreSQL configuration fields are required.")
    return _config_instance
