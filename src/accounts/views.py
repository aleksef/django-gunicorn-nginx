from django.views import generic
from django.shortcuts import render


class Login(generic.View):
    def get(self, request):
        return render(request, 'accounts/login.html')
