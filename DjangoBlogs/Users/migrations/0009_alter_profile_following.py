# Generated by Django 4.2.1 on 2023-08-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_profile_previous_logged_in_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(through='Users.Follow', to='Users.profile'),
        ),
    ]