# Generated by Django 4.2.1 on 2023-08-10 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_blogpost_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='slug',
        ),
    ]
