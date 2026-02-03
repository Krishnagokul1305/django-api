# Generated migration for MembershipRegistration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
        ('users', '0004_remove_user_role_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('renewal_count', models.IntegerField(default=0)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registrations', to='memberships.membership')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_registrations', to='users.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
