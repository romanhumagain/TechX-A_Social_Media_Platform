from django.utils.text import slugify
import uuid

def generate_slugs(title:str)->str:
  from Blog.models import BlogPost
  slug = slugify(f'{title}-{uuid.uuid4()}')
  
  while(BlogPost.objects.filter(slug=slug).exists()):
    slug = slugify(f"{title}-{uuid.uuid4()}")
    
  return slug
    