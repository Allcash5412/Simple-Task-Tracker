import logging.config
from pathlib import Path
from typing import Dict

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

default_config: Dict = SettingsConfigDict(env_file=BASE_DIR / '.env', extra='ignore')

class DefaultModelConfig:
    model_config: Dict = default_config


class GlobalSettings(BaseSettings):
    model_config = default_config
    start_setting: str = Field(alias='START_SETTING')
    logger_config: Dict = {}

    @field_validator('logger_config')
    def get_logger_config(cls, v, info: FieldValidationInfo):
        logger_config = cls.get_logger_config_by_setting(info.data['start_setting'])
        return logger_config

    @classmethod
    def get_logger_config_by_setting(cls, start_setting: str) -> Dict:
        if start_setting == 'PRODUCTION':
            LOGGER_CONFIG = {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "simple": {
                        "format": "%(levelname)s: %(message)s"
                    },
                    "detailed": {
                        "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
                    }
                },
                "handlers": {
                    'console': {
                        'level': 'WARNING',
                        'class': 'logging.StreamHandler',
                        'formatter': 'verbose'
                    },
                    'file': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'filename': 'app.log',
                        'when': 'W0',
                        'utc': True,
                        'formatter': 'verbose',
                    },
                },
                "loggers": {
                    "root": {
                        # "level": "INFO",
                        "handlers": [
                            "console",
                            # "file"
                        ]
                    }
                }
            }
        else:
            LOGGER_CONFIG = {
                "version": 1,
                "disable_existing_loggers": True,
                "formatters": {
                    "detailed": {
                        "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "DEBUG",
                        "formatter": "detailed",
                        "stream": "ext://sys.stderr"
                    },
                    # "file": {
                    #     "class": "logging.handlers.RotatingFileHandler",
                    #     "level": "WARNING",
                    #     "formatter": "detailed",
                    #     "filename": "logs/my_app.log",
                    #     "maxBytes": 10000,
                    #     "backupCount": 3
                    # }
                },
                "loggers": {
                    "app": {
                        "level": "DEBUG",
                        "handlers": [
                            "console",
                            # "file"
                        ]
                    }
                }
            }

        return LOGGER_CONFIG


class SqliteSettings(BaseSettings):
    model_config = default_config
    db_name: str = Field(alias='DB_NAME')
    url: str = ''

    @field_validator('url')
    def get_database_url(cls, v, info: FieldValidationInfo):
        return f'sqlite+aiosqlite:///{info.data['db_name']}'


class Settings(BaseSettings):
    global_settings: GlobalSettings = GlobalSettings()
    sqlite_settings: SqliteSettings = SqliteSettings()


settings = Settings()
logging.config.dictConfig(settings.global_settings.logger_config)
