from django.db.models.signals import  post_delete , pre_delete
from Blog.models import BlogPost
from django.dispatch import receiver
    
# ===== To delete the image when the blog post is deleted =====
@receiver(post_delete ,sender = BlogPost )
def delete_post_image_file(sender, instance , **kwargs):
  if instance.image:
    instance.image.delete(save = False)

# ==== To make the blog post archived before the user delete the post ======
@receiver(pre_delete , sender = BlogPost)
def make_post_archived(sender , instance , **kwargs):
  instance.is_archived = True
  instance.save(update_fields = ['is_archived'])