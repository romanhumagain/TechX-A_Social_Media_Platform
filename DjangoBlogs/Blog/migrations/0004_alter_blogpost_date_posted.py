# Generated by Django 4.2.1 on 2023-08-11 05:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_remove_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
