from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from Blog.models import *

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
  readonly_fields = ['author','slug','title','image','content','date_posted','likes_count']
  list_display = ['title', 'is_archived']
  list_filter = ['is_archived']
  
  def get_queryset(self, request):
    return BlogPost.all_objects.all().order_by('is_archived')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogComment)
admin.site.register(Like)
admin.site.register(Notification)
