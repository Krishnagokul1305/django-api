from django.contrib import admin
from .models import Internship, InternshipRegistration

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InternshipRegistration)
class InternshipRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'internship_title', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__email', 'user__name', 'internship__title']
    readonly_fields = ['applied_at', 'status_updated_at', 'created_at', 'updated_at']
    fieldsets = (
        ('Application', {
            'fields': ('internship', 'user', 'resume_link', 'applied_at', 'status', 'status_updated_at')
        }),
        ('Review & Feedback', {
            'fields': ('rejection_reason',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def internship_title(self, obj):
        return obj.internship.title
    internship_title.short_description = 'Internship'

