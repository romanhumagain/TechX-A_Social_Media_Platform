# Generated by Django 4.2.1 on 2023-09-17 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('two_factor_authentication', '0008_remove_twofactortoken_failed_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='twofactortoken',
            name='failed_attempts',
            field=models.IntegerField(default=0),
        ),
    ]
