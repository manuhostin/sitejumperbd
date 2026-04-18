from django.contrib import admin
from .models import Game, Like, Comment, View

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'created_at', 'updated_at')
    search_fields = ('game_id',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('game', 'user_id', 'created_at')
    search_fields = ('game__game_id', 'user_id')
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('game', 'user_id', 'created_at')
    search_fields = ('game__game_id', 'text', 'user_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user_id', 'ip_address', 'created_at')
    search_fields = ('game__game_id', 'user_id', 'ip_address')
    readonly_fields = ('created_at',)
