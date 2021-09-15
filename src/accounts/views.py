from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm


class Login(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:settings', slug=request.user.username)
        return render(request, 'accounts/login.html', {'form': LoginForm()})
    
    def post(self, request):
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                user = authenticate(request,
                                    username=User.objects.get(email=form.cleaned_data['email']).username,
                                    password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('accounts:settings')
                else:
                    messages.error(request, 'Incorrect username or password.')
            else:
                messages.error(request, 'Form is invalid.')
        except:
            messages.error(request, 'Internal Server Error.')        
        return render(request, 'accounts/login.html', {'form': form})