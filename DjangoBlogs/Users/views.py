from django.shortcuts import render, redirect
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
        context['posts'] = BlogPost.objects.filter(author=self.object).order_by('-date_posted')[:5]  # Limit to 5 posts for example
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
            
            
    
