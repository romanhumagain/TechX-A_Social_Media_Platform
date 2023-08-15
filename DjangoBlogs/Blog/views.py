from typing import Any, Dict
from django.db import models
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

class PostListView(ListView):
  model = BlogPost
  template_name = 'blog/home.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 5

class PostDetailsView(DetailView):
  model = BlogPost 
  template_name = 'blog/post_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post = get_object_or_404(BlogPost, slug = self.kwargs.get('slug'))
    context['comments'] = BlogComment.objects.filter(post = post).order_by('-comment_posted_date')
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
        user = profile.user
        posts = BlogPost.objects.filter(author = user).order_by('-date_posted')
        paginator = Paginator(posts , 2)
        page = request.GET.get('page' , 1)
        page_obj = paginator.get_page(page)
        
        context = {
            'target_user':user,
            'title':'Profile',
            'page_obj':page_obj,
            }
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
    
    
  
def about(request):
  return render(request ,'blog/about.html',{'title':"About"} )