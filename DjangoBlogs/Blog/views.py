from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import get_object_or_404, render , redirect
from django.views import View
from django.contrib import messages
from django.views.generic import ListView , DetailView , CreateView, UpdateView , DeleteView
from . forms import BlogPostForm
from django.http import HttpResponse
from Blog.models import *
from Users.models import *
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search)|
                                       Q(content__icontains=search)|
                                       Q(author__username__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user_liked_post_ids = Like.objects.filter(user=self.request.user).values_list('post__id', flat=True)
            context['user_liked_post_ids'] = list(user_liked_post_ids)

        return context
       

class PostDetailsView(DetailView):
  model = BlogPost 
  template_name = 'blog/post_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post = get_object_or_404(BlogPost, slug = self.kwargs.get('slug'))
    context['comments'] = BlogComment.objects.filter(post = post).order_by('-comment_posted_date')
    
    if self.request.user.is_authenticated:
            has_liked_post = Like.objects.filter(user=self.request.user , post = post).exists()
            context['has_liked_post'] = has_liked_post
    return context
  
class PostCreateView(LoginRequiredMixin , CreateView):
  model = BlogPost
  form_class = BlogPostForm
  template_name = 'blog/post_form.html'
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
   
class PostUpdateView(LoginRequiredMixin , UserPassesTestMixin, UpdateView):
  model = BlogPost
  form_class = BlogPostForm
  template_name = 'blog/post_form.html'
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
      
class PostDeleteView( LoginRequiredMixin , UserPassesTestMixin ,DeleteView):
  model = BlogPost
  template_name = 'blog/post_confirm_delete.html'
  success_url = '/'
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
    
class UserProfileDetailsView(LoginRequiredMixin, View):
    def get(self, request , *args , **kwargs):
        profile = Profile.objects.get(slug=kwargs.get('slug'))
        is_following = Follow.objects.filter(follower = request.user.profile , followed = profile).exists()
        user = profile.user
        posts = BlogPost.objects.filter(author = user).order_by('-date_posted')
        paginator = Paginator(posts , 2)
        page = request.GET.get('page' , 1)
        page_obj = paginator.get_page(page)
        
        search = self.request.GET.get('search')
        if search:
            page_obj = posts.filter(title__icontains = search)
        
        context = {
            'target_user':user,
            'title':'Profile',
            'page_obj':page_obj,
            'is_following':is_following
            }
        
        if self.request.user.is_authenticated:
            user_liked_post_ids = Like.objects.filter(user=self.request.user).values_list('post__id', flat=True)
            context['user_liked_post_ids'] = list(user_liked_post_ids)
        return render(request, 'blog/view_other_profile.html', context)
      
class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, slug=kwargs.get('slug'))
        
        comment_text = request.POST.get('comment')

        if not comment_text:
            messages.error(request, "Comment cannot be empty!")
            return redirect('post-details', slug=post.slug) 

        BlogComment.objects.create(user=request.user, post=post, comment=comment_text)
        
        messages.success(request, "Successfully added comment!")
        return redirect('post-details', slug=post.slug)

from django.db import transaction


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(BlogPost, id=post_id)
        liked = False

        with transaction.atomic():
            like = Like.objects.filter(post=post, user=request.user).first()
            if like:
                like.delete()
                BlogPost.objects.filter(id=post_id).update(likes_count=models.F('likes_count') - 1)
            else:
                Like.objects.create(post=post, user=request.user)
                BlogPost.objects.filter(id=post_id).update(likes_count=models.F('likes_count') + 1)
                liked = True

        return JsonResponse({'liked': liked, 'likes_count': post.likes_count})
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get_comment(self):
        return BlogComment.objects.filter(id=self.kwargs.get('comment_id'), user=self.request.user).first()

    def test_func(self):
        self.comment = self.get_comment()
        if not self.comment:
            return False
        return self.request.user == self.comment.user

    def post(self, request, *args, **kwargs):
        if self.comment:  # Since test_func is called before post, self.comment will be set.
            post_slug = self.comment.post.slug
            self.comment.delete()
            return redirect('post-details', slug=post_slug)
        else:
            return HttpResponseForbidden('Comment not found or you are not the owner.')

