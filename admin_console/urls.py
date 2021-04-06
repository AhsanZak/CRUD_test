from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name="admin_panel"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="admin_logout"),
    path('create-user', views.create_user, name="create_user"),
    path('update-user/<int:id>/', views.update_user, name="update_user"),
    path('edit-user/<int:id>/', views.edit_user, name="edit_user"),
    path('delete-user/<int:id>/', views.delete_user, name="delete_user"),
]
