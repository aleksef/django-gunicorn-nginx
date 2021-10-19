import uuid
import os

from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# from src.utils.images import check_image, process_user_image
# from src.settings import userimage as settings_userimage
from accounts.models import UserImage, userimage_delete 
from .forms import LoginForm, CreateForm



class Logout(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('accounts:login')


class Login(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:settings')
        return render(request, 'accounts/login.html', {'form': LoginForm()})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = None
            try:
                user = authenticate(request,
                                    username=User.objects.get(email=form.cleaned_data['email']).username,
                                    password=form.cleaned_data['password'])
                login(request, user)
                return redirect('accounts:settings')
            except:
                form.add_error(None, 'Incorrect username or password.')
        else:
            form.add_error(None, 'Form is invalid.')
        return render(request, 'accounts/login.html', {'form': form})


class Create(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:settings')
        return render(request, 'accounts/create.html', {'form': CreateForm()})

    def post(self, request):
        form = CreateForm(request.POST)
        if form.is_valid():
            try:
                user = User()
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('accounts:settings')
            except:
                form.add_error(None, 'Internal Server Error.')
        return render(request, 'accounts/create.html', {'form': form})


class Delete(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                messages.error(request, "This action is not allowed.")
                return redirect('accounts:settings')
            try:
                request.user.delete()
                messages.success(request, "Your account was succesfully deleted.")
                return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, "User does not exist")
            except Exception as e: 
                messages.error(request, e.message)
            return redirect('accounts:settings')
        return redirect('accounts:login')
        

class Settings(generic.View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        userimage = ''
        try:            
            userimage = request.user.userimage.src
        except:
            userimage = '/static/images/user-default.jpg'
        finally:
            return render(request, 'accounts/settings.html', {'userimage': userimage})


class UploadUserImage(generic.View):
    def post(self, request):
        if request.user.is_authenticated:
            if request.FILES["image_file"]:
                image_file = request.FILES["image_file"]
                fs = FileSystemStorage()
                #TODO CHECK IMAGE
                #TODO PROCESS IMAGE
                #TODO USE TRY
                filename = fs.save("users/userimage-" + str(uuid.uuid4()) + ".jpg",
                                   image_file)
                image_url = fs.url(filename)

                if UserImage.objects.filter(user=request.user).exists():
                    userimage = UserImage.objects.get(user=request.user)
                    userimage.src = image_url
                    userimage.save()
                else:
                    # Create new blank model
                    userimage = UserImage(user=request.user)
                    userimage.save()
                    # Save new src in model
                    userimage.src = image_url
                    userimage.save()
                return render(request, 'accounts/settings.html', {'userimage': userimage.src})
        messages.error(request, "Unable to upload new user image.")
        return redirect('accounts:settings')
