from django.shortcuts import render
from admin_console.models import *
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages



# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user_detail = User.objects.filter(username=request.user)
        return render(request, 'UserView/index.html')
    else:
        return render(request, 'UserView/index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        print("method is post")
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                messages.info(request, 'User is Blocked')
            else:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(home)
        else:
            messages.info(request, "Invalid Credentials")
            return redirect(login)
    else:
        print("not post")
        return render(request, 'UserView/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, 'UserView/register.html')
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                                last_name=last_name, date_of_birth=date_of_birth)
                return redirect('login')
        else:
            messages.info(request, "Passwords Not Matching")
            return render(request, 'UserView/register.html')
    else:
        return render(request, 'UserView/register.html')



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'UserView/profile.html')
    else:
        return redirect(login)


def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.date_of_birth = request.POST['date_of_birth']

            user_detail = User.objects.get(username=user)
            if 'imageInput' not in request.POST:
                user_image = request.FILES.get('imageInput')
            else:
                user_image = user_detail.profile_image

            user_detail.profile_image = user_image
            user_detail.save()
            user.save()
            return redirect(user_profile)

    else:
        return redirect(login)
