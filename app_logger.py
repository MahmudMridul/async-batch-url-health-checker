import json
import logging
import logging.config
from pathlib import Path

class AppLogger:
    def __init__(self, config_path: str = "logging_config.json", logger_name : str = __name__):
        self._ensure_log_directory(config_path)
        self._load_config(config_path)
        self.logger = logging.getLogger(logger_name)

    def _ensure_log_directory(self, config_path: str) -> None:
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.load(file)
            log_file = config["handlers"]["file"]["filename"]
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        except FileNotFoundError as e:
            raise
        except OSError as e:
            raise 

    def _load_config(self, config_path : str) -> None:
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.load(file)
            logging.config.dictConfig(config)
        except FileNotFoundError as e:
            raise
        except OSError as e:
            raise 

    def get_logger(self) -> logging.Logger: 
        return self.logger
        