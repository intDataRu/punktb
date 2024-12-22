from flask import Flask, jsonify
from flask_cors import CORS
import logging
import time
from threading import Thread
from .config import Config
from .domain import Manager as DomainManager
from .service import Manager as ServiceManager
from .controller import LoginController, ManagerController, ClientController
from .database import Database

class Server:
    def __init__(self, config: Config):
        self.http_cfg = config.http
        self.app = Flask(__name__)
        CORS(self.app)

        self.db = Database(config.postgresql)
        self.manager_service = ServiceManager(DomainManager(self.db))
        self.login_controller = LoginController(self.manager_service)
        self.manager_controller = ManagerController(self.manager_service)
        self.client_controller = ClientController(self.manager_service)

        self.login_cache = {}
        self.cache_thread = Thread(target=self.fill_login_cache)
        self.cache_thread.start()

    def run(self):
        if self.http_cfg.is_https:
            logging.info("HTTPS mode is on")
            self.app.run(host='0.0.0.0', port=8443, ssl_context=(self.http_cfg.server_cert_path, self.http_cfg.private_key_path))
        else:
            logging.info("Server started")
            self.app.run(host='0.0.0.0', port=8080)

    def fill_login_cache(self):
        while True:
            time.sleep(5)
            try:
                managers = self.manager_service.get_all_managers()
                self.login_cache = {manager.login: manager for manager in managers}
            except Exception as e:
                logging.debug("fill_login_cache error: %s", e)

# Пример конфигурации
class Config:
    class HTTP:
        is_https = False
        server_cert_path = "path/to/cert.pem"
        private_key_path = "path/to/key.pem"

    class PostgreSQL:
        username = "user"
        password = "password"
        host = "localhost"
        port = "5432"
        database = "dbname"

# Пример запуска сервера
if __name__ == "__main__":
    config = Config()
    server = Server(config)
    server.run()
