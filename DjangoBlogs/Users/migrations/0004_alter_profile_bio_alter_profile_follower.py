# Generated by Django 4.2.1 on 2023-08-12 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follower',
            field=models.IntegerField(default=False, null=True),
        ),
    ]
