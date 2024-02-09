from django.contrib import admin

from .models import Room, Message, ChatMessage,ChatSession


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(ChatMessage)
admin.site.register(ChatSession)
