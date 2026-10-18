import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_backend.settings")
django.setup()

# Теперь, когда Django загружен, импортируем бота
from bot_app.bot import run_bot

if __name__ == "__main__":
    run_bot()
