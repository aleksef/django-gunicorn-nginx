from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
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
                messages.error(request, 'Incorrect username or password.')
        else:
            messages.error(request, 'Form is invalid.')     
        return render(request, 'accounts/login.html', {'form': form})


class Create(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:settings')
        return render(request, 'accounts/create.html', {'form': CreateForm()})

    def post(self, request):
        form = CreateForm(request.POST)
        if form.is_valid():
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
        return render(request, 'accounts/settings.html')
