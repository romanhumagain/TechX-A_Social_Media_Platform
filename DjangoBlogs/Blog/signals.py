from django.db.models.signals import  post_delete
from Blog.models import BlogPost
from django.dispatch import receiver
    
# ===== To delete the image when the blog post is deleted =====
@receiver(post_delete ,sender = BlogPost )
def delete_post_image_file(sender, instance , **kwargs):
  if instance.image:
    instance.image.delete(save = False)
