import os
import threading
from django.apps import AppConfig

class BotAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot_app"

    def ready(self):
        # Запуск бота, если это не процесс миграций и не дев-сервер
        if os.environ.get("RUN_MAIN") == "true" or "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
            from .bot import run_bot
            threading.Thread(target=run_bot, daemon=True).start()
