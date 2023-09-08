from django.db.models.signals import post_save , post_delete
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from Blog.models import BlogPost

# ===== To create a profile when the user is created =====
@receiver(post_save, sender = User)
def create_profile(sender , instance , created , **kwargs):
  if created:
    Profile.objects.create(user = instance)
    
    
@receiver(post_save , sender = User)
def save_profile(sender , instance , **kwargs):
  instance.profile.save()
  
# ==== To get the user last_logged_in details =====
@receiver(user_logged_out , sender = User)
def update_previous_login(sender , request , user , **kwargs):
  profile = user.profile
  if user.last_login:
    profile.previous_logged_in_date = user.last_login
    profile.save()
    

  

    
