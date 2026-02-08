# Generated migration to remove rating and comment from Feedback
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_remove_feedback_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='comment',
        ),
    ]
