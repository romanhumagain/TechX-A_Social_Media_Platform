# Generated by Django 4.2.1 on 2023-09-17 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('two_factor_authentication', '0009_twofactortoken_failed_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twofactortoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='two_factor_auth_token', to=settings.AUTH_USER_MODEL),
        ),
    ]
