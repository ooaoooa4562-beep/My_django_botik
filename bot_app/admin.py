from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "first_name", "username", "referrals_count", "is_banned", "created_at")
    search_fields = ("telegram_id", "username", "first_name", "referral_code", "course_code")
    list_filter = ("is_banned", "created_at")
    list_editable = ("is_banned",)
    readonly_fields = ("created_at",)
