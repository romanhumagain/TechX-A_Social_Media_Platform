# Generated by Django 4.2.1 on 2023-08-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0013_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='reply',
            field=models.CharField(default=False, max_length=100, null=True),
        ),
    ]