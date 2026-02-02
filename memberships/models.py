from django.db import models
from django.contrib.postgres.fields import ArrayField

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
