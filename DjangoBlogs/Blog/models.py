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
  image = models.ImageField(null= True , blank=True, upload_to='blog_image')
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
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
      return f'liked by {self.user.username } on {self.post.author}`s {self.post} post'
    
    class Meta:
        unique_together = ('user', 'post')
        
        
class Notification(models.Model):
  TYPES = (
    ('comment', 'comment'),
    ('like', 'like'),
    ('follow', 'follow')
  )
  
  receiver = models.ForeignKey(User , on_delete=models.CASCADE)
  sender = models.ForeignKey(User , on_delete = models.SET_NULL , null=True, related_name= '+' )
  type = models.CharField(choices=TYPES , max_length=10)
  post = models.ForeignKey(BlogPost , on_delete=models.SET_NULL, null=True)
  message = models.TextField(null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)
  
  def __str__(self):
     return f"Notification for {self.receiver}: {self.message}"
   
   
class ChatRoom(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['receiver', 'sender']  
        
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE) 
    text_content = models.TextField()
    file = models.FileField(upload_to='chat_files', null=True, blank=True)
    image = models.ImageField(upload_to='chat_images', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


  
   
   

  
  
  
  
    
  
  
    
  
