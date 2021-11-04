from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from .forms import LoginForm, CreateForm
from urllib.parse import urlencode


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user', 'user@gmail.com', 'password')
    
    def test_can_logout(self):
        # Log in client
        self.client.login(username='user', password='password')
        # Check if client is logged in
        response = self.client.get('/accounts/settings/')
        self.assertEquals(response.status_code, 200) # client can access settings
        # Log out client
        response = self.client.get('/accounts/logout/')
        # Check if client is logged out
        self.assertEquals(response.url, '/accounts/login/') # client was redirected to login page

    def test_can_login(self):
        # Log in client
        form_data = urlencode({'email': 'user@gmail.com',
                               'password': 'password'})
        response = self.client.post('/accounts/login/', form_data, content_type="application/x-www-form-urlencoded")
        # Check if client is logged in
        self.assertEquals(response.url, '/accounts/settings/') # client can access settings
    
    def test_can_create_account(self):
        form_data = {'username': 'alice',
                     'email': 'alice@gmail.com',
                     'password': 'password',
                     'confirm_password': 'password'}
        response = self.client.post('/accounts/create/',
                                    urlencode(form_data),
                                    content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.url, '/accounts/settings/') # client can access settings
        self.assertTrue(User.objects.filter(username='alice').exists()) # user exists
