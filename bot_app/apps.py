import os
from django.apps import AppConfig

class BotAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot_app"

    def ready(self):
        # ЗАПУСК БОТА ОТСЮДА УБИРАЕМ
        
        # АВТО-СОЗДАНИЕ АДМИНОВ (оставляем)
        if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                admins = [
                    {"username": "admin", "email": "admin@example.com", "password": "AdminPass123!"},
                    {"username": "Anzor", "email": "anzor@example.com", "password": "AnzorPass123!"},
                ]
                for a in admins:
                    if not User.objects.filter(username=a["username"]).exists():
                        User.objects.create_superuser(a["username"], a["email"], a["password"])
                        print(f"✅ Админ {a['username']} успешно создан!")
            except Exception as e:
                print(f"Ошибка создания админов: {e}")
