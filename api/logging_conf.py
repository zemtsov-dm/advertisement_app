from logging.config import dictConfig
from config import settings
import telebot
from logging import Handler, LogRecord

class TelegramBotHandler(Handler):
    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: LogRecord):
        bot = telebot.TeleBot(self.token)
        bot.send_message(self.chat_id, self.format(record))

def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8,
                    "default_value": "-",
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                },
                "telegram": {
                    "class": "api.logging_conf.TelegramBotHandler",
                    "chat_id": f"{settings.CHAT_ID}",
                    "token": f"{settings.BOT_TOKEN}",
                    "formatter": "console",
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "api": {"handlers": ["default","telegram"], "level": "DEBUG", "propagate": False},
                "uvicorn": {"handlers": ["default"], "level": "INFO"},
                "databases": {"handlers": ["default"], "level": "WARNING"},
            },
        }
    )

