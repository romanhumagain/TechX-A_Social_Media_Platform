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
  likes_count = models.IntegerField(null=True, default=0)
  
  # to create the slug field..
  def save(self, *args, **kwargs):
    if not self.pk:
        self.slug = generate_slugs(BlogPost, self.title)
    super(BlogPost, self).save(*args, **kwargs)

    
  def __str__(self) -> str:
    return f'{self.title} by ({self.author})'
  
  def get_absolute_url(self):
    return reverse('post-details' , kwargs={'slug':self.slug})
  
class BlogComment(models.Model):
  user = models.ForeignKey(User , on_delete=models.CASCADE)
  post = models.ForeignKey(BlogPost , on_delete=models.CASCADE)
  comment = models.TextField()
  parent_comment = models.ForeignKey('self' , on_delete=models.CASCADE , null=True )
  comment_posted_date = models.DateTimeField(default= timezone.now)
  
  def __str__(self) -> str:
    return f'commented by {self.user.username} on {self.post.author}`s {self.post} post'
  
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    
    def __str__(self):
      return f'liked by {self.user.username } on {self.post.author}`s {self.post} post'
    
    class Meta:
        unique_together = ('user', 'post')
  
  
  
    
  
  
    
  
