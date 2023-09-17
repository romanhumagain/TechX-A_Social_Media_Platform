from django.db.models.signals import post_save , post_delete
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.dispatch import receiver
from .models import Profile
from Blog.models import BlogPost
import platform
from Users.models import LoginDetail
from Users.utils import send_email
from django.utils import timezone

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
    to = instance.email
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
    send_email(subject=subjects, message=message, to=to) 
  
    
# === to store the login details when the user login from the new devices === #
@receiver(user_logged_in, sender = User)
def get_login_details(sender, request, user, **kwargs):
  
  if request.user_agent.is_mobile:
      device = "Mobile"
  elif request.user_agent.is_tablet:
      device = "Tablet"
  elif request.user_agent.is_pc:
      device = "PC"
  else:
      device = "Unknown" 
      
  browser = request.user_agent.browser.family
  os = request.user_agent.os.family
  
  node_device_name = None
  processor = None
  
  if device == "PC":
    node_device_name = platform.node()
    processor = platform.processor()

    loginDetails, created = LoginDetail.objects.get_or_create(user = user, device_type = "PC", browser = browser, os = os, node_device_name = node_device_name,processor = processor )
  else:
    loginDetails, created = LoginDetail.objects.get_or_create(user = user, device_type = device, browser = browser, os = os, node_device_name = node_device_name, processor = processor )
    
  if created:
    subject = "SECURITY ALERT !!"
    message = (
    f"<p>Hello <strong>{user.username}</strong>,</p>"
    "<p>We noticed a new login to your TechBlog account.</p>"
    "<strong>Details of the login:</strong>"
    "<ul>"
        f"<li><strong>Device:</strong> {device}</li>"
        f"<li><strong>Browser:</strong> {browser}</li>"
        f"<li><strong>Processor:</strong> {processor}</li>"
        f"<li><strong>Date & Time:</strong> {timezone.now()}</li>" 
    "</ul>"
    "<p>If you recognize this activity, you can ignore this email, and no further action is needed.</p>"
    
    '<p class="warning">If you did <strong>not</strong> initiate this login:</p>'
    '<ol>'
        f"<li>Please change your password from here <a href='http://127.0.0.1:8000/user/password_change/'>http://127.0.0.1:8000/user/password_change/</a> .</li>"
        '<li>Review the devices that have accessed your account.</li>'
        "<li>Consider enabling two-factor authentication for an extra layer of security.</li>"
        '<li>Let us know at <a href="mailto:content.techblog@gmail.com">content.techblog@gmail.com</a>, so we can assist you further.</li>'
    "</ol>"
    "<p>Your security is our top priority. Regularly update your password and always use unique passwords for different online services.</p>"
    "<p>Best Regards,<br>"
    "The Tech-Blog Team</p>"
    )
    to = user.email
    send_email(subject=subject, message=message, to=to)
    

  
    
  
  
    
