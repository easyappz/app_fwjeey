from django.contrib import admin
from .models import Member, AuthToken, Message


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'display_name', 'created_at']
    search_fields = ['username', 'display_name']
    readonly_fields = ['created_at']


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'member', 'created_at']
    search_fields = ['key', 'member__username']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'author__username']
    readonly_fields = ['created_at']
