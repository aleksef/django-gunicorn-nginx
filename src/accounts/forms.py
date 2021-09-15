from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(min_length=3, max_length=16)
    password = forms.CharField(min_length=8, max_length=24, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email and not password:
            raise forms.ValidationError('Form is invalid.')


class CreateForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=16)
    email = forms.EmailField(min_length=8, max_length=254)
    password = forms.CharField(min_length=8, max_length=24, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=8, max_length=24, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(CreateForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if username in [None, ''] or email in [None, ''] or password in [None, ''] or confirm_password in [None, '']:
            raise forms.ValidationError("Some fields are empty.")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        try:
            match = User.objects.get(email=email)
            raise forms.ValidationError('This email address is already in use.')
        except User.DoesNotExist:
            # OK, no matches
            pass
        try:
            match = User.objects.get(username=username)
            raise forms.ValidationError('This username is already in use.')
        except User.DoesNotExist:
            # OK, no matches
            pass
