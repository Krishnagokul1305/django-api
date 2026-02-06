from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User

class Membership(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    benefits = ArrayField(
        base_field=models.CharField(max_length=200),
        blank=True,
        default=list
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MembershipRegistration(models.Model):
    """User membership registration and subscription tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_registrations')
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT, related_name='registrations')
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment Fields
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    reason = models.TextField(blank=True, null=True, help_text="User's reason for joining/interest in membership")
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for rejection")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.membership.name} (since {self.start_date.date()})"
