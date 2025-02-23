from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.
                               TextInput(attrs={'class': 'input100', "placeholder":"Username"})
                               )
    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'input100', "placeholder":"Password"})
                               )

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is not None:
            return self.cleaned_data
        else:
            raise forms.ValidationError("Incorrect Username or Password", code='invalid_login')


# account/forms.py


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder':'Email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'Confirm Password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # email validation
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise forms.ValidationError("Please enter a valid email address!")

        # email existence
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken!")
        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
