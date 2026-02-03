from django.contrib import admin
from .models import Membership, MembershipRegistration

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MembershipRegistration)
class MembershipRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'membership_name', 'start_date', 'expiry_date', 'payment_status', 'is_active']
    list_filter = ['payment_status', 'is_active', 'start_date']
    search_fields = ['user__email', 'user__name', 'membership__name']
    readonly_fields = ['start_date', 'created_at', 'updated_at']
    fieldsets = (
        ('Registration', {
            'fields': ('user', 'membership', 'start_date', 'expiry_date')
        }),
        ('Payment & Status', {
            'fields': ('payment_status', 'is_active', 'payment_amount', 'payment_method', 'transaction_id', 'payment_date', 'renewal_count', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def membership_name(self, obj):
        return obj.membership.name
    membership_name.short_description = 'Membership'
