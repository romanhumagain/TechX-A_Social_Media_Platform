from django.urls import path
from Blog import views

# making the routes for the urls
urlpatterns = [
  path('' ,views.home , name="blog-home"),
  path('about/' ,views.about , name='blog-about'),
]