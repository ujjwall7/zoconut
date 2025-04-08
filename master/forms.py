from django import forms
from django.contrib.auth import authenticate
from . models import *

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Authenticate the user
            user = authenticate(username=email, password=password)
            print(user)

            if user is None or not user.is_active:
                self.add_error("password", "Couldn't Sign In With Provided Details.")
        print(cleaned_data)
        return cleaned_data
