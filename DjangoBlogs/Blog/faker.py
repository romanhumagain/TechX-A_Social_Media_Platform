import django
from faker import Faker


from Blog.models import BlogComment, BlogPost, User  
from django.utils import timezone

fake = Faker()

def create_fake_comment(n=10):
    
    users = list(User.objects.all())
    posts = list(BlogPost.objects.all())
    comments = list(BlogComment.objects.all())  # for parent comments

    for _ in range(n):
        user = fake.random_element(users)
        post = fake.random_element(posts)

        if comments and fake.random_int(min=0, max=1):  # 50% chance to set a parent_comment
            parent_comment = fake.random_element(comments)
        else:
            parent_comment = None

        BlogComment.objects.create(
            user=user,
            post=post,
            comment=fake.sentence(),
            parent_comment=parent_comment,
            comment_posted_date=timezone.now()
        )