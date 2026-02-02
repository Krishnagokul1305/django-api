from django.db import models

class Webinar(models.Model):
    image = models.ImageField(upload_to='webinars/', null=True, blank=True)
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
