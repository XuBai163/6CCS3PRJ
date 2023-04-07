from django.contrib import admin
from .models import Message, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email',
    ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for posts."""

    list_display = [
        'user', 'text', 'is_user_message',
    ]
