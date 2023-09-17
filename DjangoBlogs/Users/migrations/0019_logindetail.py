# Generated by Django 4.2.1 on 2023-09-15 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0018_rename_followed_people_follow_followed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=100)),
                ('browser', models.CharField(max_length=100)),
                ('os', models.CharField(max_length=100)),
                ('node_device_name', models.CharField(default=None, max_length=200, null=True)),
                ('processor', models.CharField(default=None, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]