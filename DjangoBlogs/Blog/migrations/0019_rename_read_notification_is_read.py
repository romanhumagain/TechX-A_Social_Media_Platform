# Generated by Django 4.2.1 on 2023-09-05 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0018_rename_user_notification_receiver_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='is_read',
        ),
    ]