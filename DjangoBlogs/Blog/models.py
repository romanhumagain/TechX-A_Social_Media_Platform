from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Blog.utils import generate_slugs
from django.urls import reverse
# Create your models here.
class BlogPost(models.Model):
  author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts')
  slug = models.SlugField(null=True,unique=True)
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default = timezone.now)
  
  # to create the slug field..
  def save(self, *args, **kwargs):
    if not self.pk:
        self.slug = generate_slugs(BlogPost, self.title)
    super(BlogPost, self).save(*args, **kwargs)

    
  def __str__(self) -> str:
    return self.title
  
  def get_absolute_url(self):
    return reverse('post-details' , kwargs={'slug':self.slug})
    
  
  
    
  
