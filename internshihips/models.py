from django.db import models
from users.models import User

class Internship(models.Model):
    image = models.ImageField(upload_to='internships/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class InternshipRegistration(models.Model):
    """User application/registration for internships"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internship_registrations')
    
    # Resume
    resume_link = models.URLField(help_text="URL to hosted resume (e.g., S3, Google Drive)")
    
    reason = models.TextField(blank=True, null=True, help_text="User's reason for applying/interest in internship")
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    status_updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ('internship', 'user')  # One application per user per internship
        indexes = [
            models.Index(fields=['status', '-applied_at']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.internship.title} ({self.status})"

