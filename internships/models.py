from django.db import models
from users.models import User
from django.utils.text import slugify
import uuid
import os

def resume_upload_path(instance, filename):
    """Generate unique filename using UUID"""
    ext = os.path.splitext(filename)[1]  # Get file extension
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('resumes', filename)

class Internship(models.Model):
    image = models.ImageField(upload_to='internships/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class InternshipRegistration(models.Model):
    """User application/registration for internships"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internship_registrations')
    
    resume = models.FileField(upload_to=resume_upload_path, help_text="Upload your resume (PDF, DOC, DOCX)")
    
    reason = models.TextField(blank=True, null=True, help_text="User's reason for applying/interest in internship")
    
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

