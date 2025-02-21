from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'owner')
    search_fields = ('email', 'full_name')
    list_filter = ('owner',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner')
    search_fields = ('subject', 'body')
    list_filter = ('owner',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'start_time', 'end_time', 'status', 'owner')
    list_filter = ('status', 'owner')
    filter_horizontal = ('clients',)
    search_fields = ('message__subject',)
    date_hierarchy = 'start_time'

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'status', 'mailing')
    list_filter = ('status', 'datetime')
    search_fields = ('server_response',)
    date_hierarchy = 'datetime' 