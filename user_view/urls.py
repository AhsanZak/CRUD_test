from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-setprofile/', views.edit_user_profile, name="edit_userProfile"),
]
