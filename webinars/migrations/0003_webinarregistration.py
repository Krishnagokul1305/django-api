# Generated migration for WebinarRegistration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinars', '0002_rename_status_webinar_is_active'),
        ('users', '0004_remove_user_role_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebinarRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('attended', models.BooleanField(default=False, help_text='Whether user attended the webinar')),
                ('attendance_marked_at', models.DateTimeField(blank=True, null=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], help_text='Rating from 1-5', null=True)),
                ('feedback', models.TextField(blank=True, help_text='Feedback from attendee', null=True)),
                ('feedback_given_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, help_text='Reason for cancellation/rejection', null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webinar_registrations', to='users.user')),
                ('webinar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='webinars.webinar')),
            ],
            options={
                'ordering': ['-registered_at'],
                'unique_together': {('webinar', 'user')},
            },
        ),
    ]
