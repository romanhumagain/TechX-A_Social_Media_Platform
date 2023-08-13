from django.utils.text import slugify
import uuid

def generate_slugs(model_class, title: str) -> str:
    slug = slugify(f'{title}-{uuid.uuid4()}')
    
    while model_class.objects.filter(slug=slug).exists():
        slug = slugify(f"{title}-{uuid.uuid4()}")
    
    return slug
