from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from .models import UserProfile, Photo
from .forms import UserRegistrationForm, PhotoUploadForm


# Create your views here.
def home(request):
    recent_photos = Photo.objects.order_by("upload_time")[:5]
    return render(request, 'upimg/home.html', {'photos': recent_photos})


def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {'error': "Invalid username or password", 'form': form}
        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            return render(request, 'upimg/login.html', context)
        check_user = authenticate(request, username=user_profile.user.username, password=password)
        if check_user is not None and check_user.is_active:
            login(request, check_user)
            return redirect('home')
        else:
            return render(request, 'upimg/login.html', context)
    else:
        return render(request, 'upimg/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'upimg/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(uploader=request.user.userprofile, title=request.POST["title"], image=request.FILES["image"])
            photo.scale()
            photo.save()
            return redirect('home')
    else:
        form = PhotoUploadForm()
    return render(request, 'upimg/upload.html', {'form': form})

def user_images(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    photos = Photo.objects.filter(uploader=request.user.userprofile)
    return render(request, 'upimg/user_images.html', {'photos': photos})

def user_delete(request, username):
    if (request.user.username != username):
        return HttpResponseForbidden()
    error = ""
    if request.method == 'POST':
        photos = request.POST.getlist('images')
        if photos:
            Photo.objects.filter(id__in=photos).delete()
            remainder = Photo.objects.filter(uploader=request.user.userprofile)
            return render(request, 'upimg/user_images.html', {'photos': remainder})
        else:
            error = "You didn't select any images!"
    photos = Photo.objects.filter(uploader=request.user.userprofile)
    return render(request, 'upimg/delete.html', {'photos': photos, 'error': error})
    