from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
import pyotp
from .forms import UserRegisterForm , UserLoginForm , UserUpdateForm , ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from Blog.models import BlogPost, Like , Notification
from django.core.paginator import Paginator
from . models import Profile , Follow , LoginDetail
from Users.otp import send_otp
from datetime import datetime

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, 'your account has been created!')
            return redirect('/account/login/')
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
        
            # send_otp(request)
            # username = request.session.get('username')
            # return redirect('otp')
            
        else:
            messages.error(request ,'Invalid Credentials')
            return redirect('login_user')
        
# === dead code ==== #
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        username = request.session.get('username')
        
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username = username )
                    login(request, user)
                    
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    print("working")
                else:
                    messages.error(request, "Invalid Code")       
                
            else:
             messages.error(request, "Sessioned expired !!")  
             print("EXPIRED")     
                   
        else:
            messages.error(request, "something went wrong !!")       
            
        
    return render(request, 'users/otp.html')


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
        
        if self.request.user.is_authenticated:
            user_liked_post_ids = Like.objects.filter(user=self.request.user).values_list('post__id', flat=True)
            context['user_liked_post_ids'] = list(user_liked_post_ids)
        
        profile =  Profile.objects.get(user = self.request.user)
        
        followers = profile.follower_set.all()
        followings = profile.following_set.all()
        
        context['followers'] = followers
        context['followings'] = followings
        
        login_details = LoginDetail.objects.filter(user = self.request.user, is_read = False).order_by('-login_date')
        context['login_details'] = login_details
        
        
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
    login_user_profile = get_object_or_404(Profile , user = request.user)

    if not Follow.objects.filter(follower=request.user.profile, followed=target_profile).exists() and request.user.profile != target_profile:
        Follow.objects.create(follower=request.user.profile, followed=target_profile)
        
        # Increase the follower count
        target_profile.follower_count += 1
        target_profile.save()
        
        login_user_profile.following_count += 1
        login_user_profile.save()
        
        notification, created= Notification.objects.get_or_create(
            receiver = target_profile.user,
            sender = request.user,
            type = "follow", 
        )
        
        if not created:
            notification.timestamp = timezone.now()
            notification.save()
            
        notification.message = f"{request.user.username} started following you."
        notification.save()
        
    
        return JsonResponse({'success': True, 'follower_count': target_profile.follower_count})
    return JsonResponse({'success': False})

@login_required
def unfollow(request, slug):
    target_profile = get_object_or_404(Profile, slug=slug)
    login_user_profile = get_object_or_404(Profile , user = request.user)
    
    unfollowed = Follow.objects.filter(follower=request.user.profile, followed=target_profile).delete()
    
    # Decrease the follower count if someone was unfollowed
    if unfollowed[0]:  # [0] because .delete() returns a tuple (num_deleted, details)
        target_profile.follower_count  -= 1
        target_profile.save()
        
        login_user_profile.following_count -= 1
        login_user_profile.save()

    return JsonResponse({'success': True, 'follower_count': target_profile.follower_count,'following_count': login_user_profile.following_count })

@login_required
def confirm_login_activity(request):
    
    not_confirmed_activity = LoginDetail.objects.filter(user = request.user, is_read = False)
    
    for detail in not_confirmed_activity:
        detail.is_read = True
        detail.save()
    
    return render(request, 'users/profile.html')

    

        
