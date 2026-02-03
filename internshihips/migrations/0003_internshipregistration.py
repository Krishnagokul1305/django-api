# Generated migration for InternshipRegistration

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('internshihips', '0002_rename_status_internship_is_active'),
        ('users', '0004_remove_user_role_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(choices=[('high_school', 'High School'), ('bachelors', "Bachelor's Degree"), ('masters', "Master's Degree"), ('phd', 'PhD'), ('diploma', 'Diploma'), ('other', 'Other')], max_length=50)),
                ('current_institution', models.CharField(blank=True, max_length=255, null=True)),
                ('major_or_field', models.CharField(blank=True, max_length=255, null=True)),
                ('resume_link', models.URLField(help_text='URL to hosted resume (e.g., S3, Google Drive)')),
                ('portfolio_link', models.URLField(blank=True, help_text='Portfolio or GitHub link', null=True)),
                ('skill_tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, help_text="JSON array of skills (e.g., ['Python', 'Django', 'REST API'])")),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewing', 'Under Review'), ('shortlisted', 'Shortlisted'), ('interviewing', 'Interviewing'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('status_updated_at', models.DateTimeField(auto_now=True)),
                ('cover_letter', models.TextField(blank=True, null=True)),
                ('expected_start_date', models.DateField(blank=True, null=True)),
                ('available_hours_per_week', models.IntegerField(blank=True, help_text='Hours available per week', null=True)),
                ('interviewer_notes', models.TextField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='internshihips.internship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_registrations', to='users.user')),
            ],
            options={
                'ordering': ['-applied_at'],
                'unique_together': {('internship', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='internshipregistration',
            index=models.Index(fields=['status', '-applied_at'], name='internshihi_status_a1b2c3_idx'),
        ),
        migrations.AddIndex(
            model_name='internshipregistration',
            index=models.Index(fields=['user', 'status'], name='internshihi_user_id_d4e5f6_idx'),
        ),
    ]
