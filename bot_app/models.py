from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=50, unique=True)
    referred_by = models.BigIntegerField(blank=True, null=True, verbose_name="Кто пригласил")
    referrals_count = models.IntegerField(default=0, verbose_name="Приглашено друзей")
    is_banned = models.BooleanField(default=False, verbose_name="Забанен")
    course_code = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Код курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
