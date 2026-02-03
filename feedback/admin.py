from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'feedback_type', 'rating', 'submitted_at']
    list_filter = ['feedback_type', 'rating', 'submitted_at']
    search_fields = ['user__email', 'user__name', 'comment', 'title']
    readonly_fields = ['submitted_at', 'created_at', 'updated_at', 'content_type', 'object_id']
    fieldsets = (
        ('User & Type', {
            'fields': ('user', 'feedback_type', 'content_type', 'object_id')
        }),
        ('Feedback Content', {
            'fields': ('title', 'comment', 'rating')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
