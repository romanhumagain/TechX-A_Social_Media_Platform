from django.urls import path
from .views import PostListView , PostDetailsView , PostCreateView , PostUpdateView , PostDeleteView , UserProfileDetailsView
from Blog import views


# making the routes for the urls
urlpatterns = [
    path('' , PostListView.as_view() , name="blog-home"),
    path('post/new/' , PostCreateView.as_view() , name="post-create"),  # Move this above the slug pattern
    path('post-details/<slug:slug>/' , PostDetailsView.as_view() , name="post-details"),
    path('post/<slug:slug>/update/' , PostUpdateView.as_view() , name="post-update"),  # This one might also cause problems; consider using int:pk
    path('post/<slug:slug>/delete/' , PostDeleteView.as_view() , name="post-delete"),
    path('user/profile-details/<slug:slug>/' , UserProfileDetailsView.as_view() , name="user-profile-details"),
    path('about/' , views.about , name='blog-about'),
]