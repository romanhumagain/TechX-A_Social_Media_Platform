# Generated by Django 4.2.1 on 2023-09-05 15:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0017_like_timestamp_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user',
            new_name='receiver',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='like',
        ),
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Blog.blogpost'),
        ),
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 9, 5, 15, 40, 54, 541374, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('comment', 'comment'), ('like', 'like'), ('follow', 'follow')], default=datetime.datetime(2023, 9, 5, 15, 41, 1, 600819, tzinfo=datetime.timezone.utc), max_length=10),
            preserve_default=False,
        ),
    ]