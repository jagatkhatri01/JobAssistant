# Generated by Django 5.1.4 on 2025-04-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_customuser_managers_alter_customuser_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
