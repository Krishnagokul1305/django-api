from django.db import models
from users.models import User

class Webinar(models.Model):
    image = models.ImageField(upload_to='webinars/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class WebinarRegistration(models.Model):
    """User registration for webinars with attendance tracking"""
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webinar_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False, help_text="Whether user attended the webinar")
    attendance_marked_at = models.DateTimeField(null=True, blank=True)
    
    reason = models.TextField(blank=True, null=True, help_text="User's reason for registering/interest in webinar")
    
    # Rejection/Cancellation
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for cancellation/rejection")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('webinar', 'user')  # One registration per user per webinar

    def __str__(self):
        return f"{self.user.email} - {self.webinar.title}"
