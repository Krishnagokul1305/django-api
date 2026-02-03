# Generated migration for Feedback model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0004_remove_user_role_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('feedback_type', models.CharField(choices=[('webinar', 'Webinar'), ('internship', 'Internship'), ('membership', 'Membership'), ('event', 'Event'), ('general', 'General')], max_length=20)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], help_text='Rating from 1-5')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.TextField(help_text='Feedback comment/review')),
                ('is_approved', models.BooleanField(default=False, help_text='Admin approval status')),
                ('is_anonymous', models.BooleanField(default=False, help_text='Show user anonymously')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='users.user')),
            ],
            options={
                'ordering': ['-submitted_at'],
                'unique_together': {('user', 'content_type', 'object_id')},
            },
        ),
        migrations.AddIndex(
            model_name='feedback',
            index=models.Index(fields=['feedback_type', '-submitted_at'], name='feedback_fe_feedb_idx'),
        ),
        migrations.AddIndex(
            model_name='feedback',
            index=models.Index(fields=['user', 'feedback_type'], name='feedback_fe_user_id_idx'),
        ),
        migrations.AddIndex(
            model_name='feedback',
            index=models.Index(fields=['rating'], name='feedback_fe_rating_idx'),
        ),
    ]
