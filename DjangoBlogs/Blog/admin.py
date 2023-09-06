from django.contrib import admin
from Blog.models import *

# Register your models here.

admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(Like)
admin.site.register(Notification)
