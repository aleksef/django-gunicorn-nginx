from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from .forms import LoginForm
from urllib.parse import urlencode


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user', 'user@gmail.com', 'password')
    
    def test_can_logout(self):
        user = User.objects.get(username='user')
        # Log in client
        self.client.login(username='user', password='password')
        # Check if client is logged in
        response = self.client.get('/accounts/settings/')
        self.assertEquals(response.status_code, 200)
        # Log out client
        response = self.client.get('/accounts/logout/')
        # Check if client is logged out
        self.assertEquals(response.url, '/accounts/login/')

    def test_can_login(self):
        user = User.objects.get(username='user')
        # Log out
        self.client.login(username='user', password='password')
        self.client.logout()
        # Check if client logged out
        response = self.client.get('/accounts/settings/')
        self.assertEquals(response.url, '/accounts/login/')
        # Log in
        form_data = {'email': 'user@gmail.com',
                     'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        data = urlencode(form_data)
        response = self.client.post('/accounts/login/', data, content_type="application/x-www-form-urlencoded")
        # Check if client logged in
        self.assertEquals(response.url, '/accounts/settings/')
