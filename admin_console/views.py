from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import *
from django.contrib.auth.models import auth
from django.http import JsonResponse

# Create your views here.


def admin_panel(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        details = User.objects.filter(is_superuser=False).order_by('id')

        context = {
                'user': details, 
        }
        return render(request, 'AdminConsole/index.html', context)
    else:
        return redirect(login)


def login(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        return redirect(admin_panel)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(admin_panel)
        else:
            messages.info(request, "Invalid credentials")
            return render(request, 'AdminConsole/login.html')
    else:
        return render(request, 'AdminConsole/login.html')


def logout(request):
    auth.logout(request)
    return redirect(admin_panel)


def create_user(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            designation = request.POST['designation']
            manager = request.POST['manager']
            date_of_birth = request.POST['date_of_birth']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    return render(request, 'AdminConsole/register_user.html')
                else:
                    user = User.objects.create_user(username=username, password=password1,
                                                    first_name=first_name, last_name=last_name, manager=manager, 
                                                    designation=designation, date_of_birth=date_of_birth)
                    return redirect(admin_panel)
            else:
                messages.info(request, "Passwords not Matching")
        else:
            designations = {"Manager", "Supervisor", "Cleaner", "Driver", "Coordinator", "Project Lead"}
            return render(request, 'AdminConsole/register_user.html', {'designations': designations})
    else:
        return redirect(admin_panel)


def update_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        user = User.objects.get(id=id)
        designations = {"Manager", "Supervisor", "Cleaner", "Driver", "Coordinator", "Project Lead"}
        managers = User.objects.filter(designation="Manager")
        return render(request, 'AdminConsole/update_user.html', {'details': user, 'managers':managers, 'designations': designations})
    else:
        return redirect(admin_panel)


def edit_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            user = User.objects.get(id=id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.designation = request.POST['designation']
            user.manager = request.POST['manager']
            user.save()
            return redirect(admin_panel)
        else:
            return redirect(update_user)
    else:
        return redirect(admin_panel)


def delete_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        user = User.objects.get(id=id)
        user.delete()
        return redirect(admin_panel)
    else:
        return redirect(admin_panel)
