from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User


class Feedback(models.Model):
    """Generic feedback model for webinars, internships, and other entities"""
    
    FEEDBACK_TYPE_CHOICES = [
        ('webinar', 'Webinar'),
        ('internship', 'Internship'),
        ('membership', 'Membership'),
        ('event', 'Event'),
        ('general', 'General'),
    ]

    # User providing feedback
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')

    # Generic relation to any object (webinar, internship, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Feedback type
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)

    # Feedback content (rating and comment removed)

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('user', 'content_type', 'object_id')  # One feedback per user per object
        indexes = [
            models.Index(fields=['feedback_type', '-submitted_at']),
            models.Index(fields=['user', 'feedback_type']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.feedback_type}"
