from django.contrib import admin
from .models import Comment, ContactLog, StatusHistory


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['application', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['application__reference_number', 'application__email', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ContactLog)
class ContactLogAdmin(admin.ModelAdmin):
    list_display = ['application', 'recruiter', 'contact_type', 'contacted_at']
    list_filter = ['contact_type', 'contacted_at']
    search_fields = ['application__reference_number', 'application__email']
    readonly_fields = ['contacted_at']


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['application', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['application__reference_number', 'application__email']
    readonly_fields = ['changed_at']
