from django.urls import path
from django.contrib.auth import views as auth_views
from Users.views import register_user , register_user, LoginView ,ProfileView, UpdateProfileView
urlpatterns = [
  path('register/', register_user , name="register_user" ),
  path('login/', LoginView.as_view() , name="login_user" ),
  path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html') , name="logout_user"),
  path('profile/', ProfileView.as_view() , name="user_profile" ),
  path('update_profile/', UpdateProfileView.as_view() , name="update_profile" ),
  
]