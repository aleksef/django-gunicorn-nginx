import uuid
import os

from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# from src.utils.images import check_image, process_user_image
# from src.settings import userimage as settings_userimage
# from accounts.models import UserImage, userimage_delete 
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
            userimage = request.user.userimage.src.url
        except:
            userimage = '/media/user_images/user-default.jpg'
        finally:
            return render(request, 'accounts/settings.html', {'userimage': userimage})
    
    # def post(self, request):
    #     if request.user.is_authenticated:
    #         # User Image
    #         if request.FILES.getlist('user-image'):
    #             # Check image
    #             if not check_image(request.FILES['user-image'],
    #                                settings_userimage['height'],
    #                                settings_userimage['width'],
    #                                settings_userimage['max_size']):
    #                 messages.error(request, 'Image must be JPEG or PNG type, at least 150x150 pixels and 2MB maximum size.')                    
    #                 return render(request, 
    #                               'accounts/settings-profile.html', 
    #                               {'userimage': '/media/user_images/user-default.jpg'})
    #             # Check if userimge exists and delete it
    #             try:
    #                 UserImage.objects.get(user=request.user).delete()
    #             except:
    #                 pass
    #             finally:
    #                 # Create new blank model
    #                 userimage = UserImage(user=request.user)
    #                 userimage.save()
    #                 # Save image to directory
    #                 filename = "userimage-" + str(uuid.uuid4()) + ".jpg"
    #                 path = os.getcwd() + "/media/images/profiles/" + filename # folder is not creating problem
    #                 cv2.imwrite(path, process_user_image(request.FILES['user-image']))
    #                 # Save new src in model
    #                 userimage.src = "images/profiles/" + filename
    #                 userimage.save()
