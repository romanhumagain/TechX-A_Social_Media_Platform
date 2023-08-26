# Generated by Django 4.2.1 on 2023-08-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_alter_profile_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='Users.Follow', to='Users.profile'),
        ),
    ]