from django.urls import path
from django.contrib.auth import views as auth_views
from Users.views import register_user, LoginView , UpdateProfileView , ProfileDetailsView , follow, unfollow
urlpatterns = [
  path('register/', register_user , name="register_user" ),
  path('login/', LoginView.as_view() , name="login_user" ),
  path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html') , name="logout_user"),
  path('profile/', ProfileDetailsView.as_view() , name="user_profile" ),
  path('update_profile/', UpdateProfileView.as_view() , name="update_profile" ),
  path('password-reset/' , auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name='password_reset'),
  path('password-reset/done/' , auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
  path('password-reset/confirm/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name='password_reset_confirm'),
  path('password-reset/complete/' , auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
  path('follow/<slug:slug>/', follow, name='follow'),
  path('unfollow/<slug:slug>/', unfollow, name='unfollow'),

  
  
]