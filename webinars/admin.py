from django.contrib import admin
from .models import Webinar, WebinarRegistration

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WebinarRegistration)
class WebinarRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'webinar_title', 'registered_at', 'attended', 'rating', 'feedback_status']
    list_filter = ['attended', 'rating', 'registered_at', 'feedback_given_at']
    search_fields = ['user__email', 'user__name', 'webinar__title']
    readonly_fields = ['registered_at', 'attendance_marked_at', 'feedback_given_at', 'created_at', 'updated_at']
    fieldsets = (
        ('Registration', {
            'fields': ('webinar', 'user', 'registered_at')
        }),
        ('Attendance', {
            'fields': ('attended', 'attendance_marked_at')
        }),
        ('Feedback', {
            'fields': ('rating', 'feedback', 'feedback_given_at')
        }),
        ('Rejection', {
            'fields': ('rejection_reason',)
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def webinar_title(self, obj):
        return obj.webinar.title
    webinar_title.short_description = 'Webinar'

    def feedback_status(self, obj):
        return 'Yes' if obj.feedback_given_at else 'No'
    feedback_status.short_description = 'Feedback Given'