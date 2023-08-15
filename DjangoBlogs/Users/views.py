from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm , UserLoginForm , UserUpdateForm , ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from Blog.models import BlogPost
from django.core.paginator import Paginator
from . models import Profile , Follow

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, 'your account has been created!')
            return redirect('login_user')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title':'Register'})


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {'form': form, 'title':'Login'}
        return render(request, 'users/login.html', context)
        
    def post(self, request):
        form = UserLoginForm(request.POST)
        data = request.POST
        username = data.get('username')
        password = data.get('password')
            
        if not User.objects.filter(username=username).exists():
            messages.error(request ,'Invalid Username')
            return redirect('login_user')
                
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request ,'Invalid Credentials')
            return redirect('login_user')


class ProfileDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailsView, self).get_context_data(**kwargs)
        
        # Add additional context
        posts = BlogPost.objects.filter(author=self.object).order_by('-date_posted')
        
        paginator = Paginator(posts, 5) # Show 2 posts per page
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, serve the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), serve the last page of results
            page_obj = paginator.page(paginator.num_pages)
        
        search = self.request.GET.get('search')
        if search:
            page_obj = posts.filter(title__icontains = search)
        
        context['page_obj'] = page_obj
        context['title'] = 'Profile'
        return context

    def test_func(self):
        # Check if the logged-in user is the owner of the profile.
        # If not, deny access.
        if self.get_object() == self.request.user:
            return True
        return False

class UpdateProfileView(LoginRequiredMixin, View):
    def get_forms(self , request):
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
        return user_update_form, profile_update_form
    
    def get(self , request):
        user_update_form , profile_update_form = self.get_forms(request)
        
        context = {
            'title':'Update Profile',
            'user_update_form':user_update_form,
            'profile_update_form':profile_update_form 
            }
        return render(request, 'users/update_profile.html' , context)
    
    def post(self ,request):
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'your profile has been updated')
            return redirect('user_profile')
            
            
# for follow and unfollow
@login_required
def follow(request, slug):
    target_profile = get_object_or_404(Profile, slug=slug)
    if not Follow.objects.filter(follower=request.user.profile, followed=target_profile).exists() and request.user.profile != target_profile:
        Follow.objects.create(follower=request.user.profile, followed=target_profile)
        
        # Increase the follower count
        target_profile.follower_count += 1
        target_profile.save()

        return JsonResponse({'success': True, 'follower_count': target_profile.follower_count})
    return JsonResponse({'success': False})

@login_required
def unfollow(request, slug):
    target_profile = get_object_or_404(Profile, slug=slug)
    unfollowed = Follow.objects.filter(follower=request.user.profile, followed=target_profile).delete()
    
    # Decrease the follower count if someone was unfollowed
    if unfollowed[0]:  # [0] because .delete() returns a tuple (num_deleted, details)
        target_profile.follower_count -= 1
        target_profile.save()

    return JsonResponse({'success': True, 'follower_count': target_profile.follower_count})
