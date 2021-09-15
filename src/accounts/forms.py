from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(min_length=3, max_length=16)
    password = forms.CharField(min_length=8, max_length=24, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email and not password:
            raise forms.ValidationError('Form is invalid.')