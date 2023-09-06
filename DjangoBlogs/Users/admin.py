from django.contrib import admin
from Users.models import Profile , Follow

class ProfileAdmin(admin.ModelAdmin):
  readonly_fields = ['user','previous_logged_in_date', 'slug', 'profile_pic', 'bio',  'following' , 'following_count', 'follower_count']

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow)