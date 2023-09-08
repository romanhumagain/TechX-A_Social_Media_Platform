from django.db import models
from django.db.models.query import QuerySet

class BlogPostManager(models.Manager):
  def get_queryset(self) -> QuerySet:
    return super().get_queryset().filter(is_archived = False)