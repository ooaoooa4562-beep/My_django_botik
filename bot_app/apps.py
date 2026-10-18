import os
import threading
from django.apps import AppConfig


class BotAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot_app"

    def ready(self):
        # 1. ЗАПУСК TELEGRAM-БОТА
        # Запускаем только в основном процессе (чтобы не было дублей)
        if os.environ.get("RUN_MAIN") == "true" or "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
            from .bot import run_bot
            threading.Thread(target=run_bot, daemon=True).start()

        # 2. АВТО-СОЗДАНИЕ АДМИНОВ
        # Запускаем только на сервере (на Render)
        if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                
                # СПИСОК АДМИНОВ
                admins = [
                    {
                        "username": "admin", 
                        "email": "admin@example.com", 
                        "password": "Rostiktostik129876!"
                    },
                    {
                        "username": "Anzor", 
                        "email": "teacher@example.com", 
                        "password": "Anxoradmin3467!"
                    },
                ]
                
                for a in admins:
                    if not User.objects.filter(username=a["username"]).exists():
                        User.objects.create_superuser(
                            username=a["username"], 
                            email=a["email"], 
                            password=a["password"]
                        )
                        print(f"✅ Админ {a['username']} успешно создан!")
                    else:
                        print(f"ℹ️ Админ {a['username']} уже существует.")
                        
            except Exception as e:
                print(f"⚠️ Ошибка при создании админов: {e}")
