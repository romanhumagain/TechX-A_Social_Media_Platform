# Generated by Django 4.2.1 on 2023-09-18 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0027_rename_count_notification_unread_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='unread_count',
        ),
    ]