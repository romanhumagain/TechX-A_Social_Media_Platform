from django.db.models.signals import post_save , post_delete
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
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
    
    
# ==== To automatically send the welcome message to new users ===== #
@receiver(post_save , sender = User)

def send_email_to_user(sender , instance , created , **kwargs):
  if created:
    subjects =" You're In! Discover what's next on TechBlog-A Blogging Platform."
    from_email = settings.EMAIL_HOST_USER
    to = [instance.email]
    message = (
      f"<p>Hello <strong>{instance.username}</strong>,</p>"
      "<br>"
      "Warm greetings from <strong>Tech Blog Team</strong>! We're delighted to welcome you to our community of tech enthusiasts, writers, and readers. "
      "From the latest in AI to breakthroughs in cybersecurity, get ready to explore a world of innovation and insights."
      "<br><br>"
      "If you ever have questions or ideas, our virtual door is always open."
      "<br><br>"
      "Happy reading and writing!"
      "<br>"
      "Warmly,<br>"
      "The <strong> Tech Blog </strong> Team"
  )
    email = EmailMultiAlternatives(
      subject=subjects, body=message, from_email=from_email, to=to
    )
    email.content_subtype = 'html'
    email.send()
    

  

    
