from django.urls import path
from .views import PostListView , PostDetailsView , PostCreateView , PostUpdateView , PostDeleteView , UserProfileDetailsView , PostCommentView ,LikePostView , CommentDeleteView

# making the routes for the urls
urlpatterns = [
    path('' , PostListView.as_view() , name="blog-home"),
    path('post/new/' , PostCreateView.as_view() , name="post-create"),  # Move this above the slug pattern
    path('post-details/<slug:slug>/' , PostDetailsView.as_view() , name="post-details"),
    path('post/<slug:slug>/update/' , PostUpdateView.as_view() , name="post-update"),  
    path('post/<slug:slug>/delete/' , PostDeleteView.as_view() , name="post-delete"),
    path('post/comment/<slug:slug>/' , PostCommentView.as_view() , name="post-comment"),
    path('user/profile-details/<slug:slug>/' , UserProfileDetailsView.as_view() , name="user-profile-details"),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('delete/comment/<int:comment_id>/', CommentDeleteView.as_view(), name='delete_comment'),

]