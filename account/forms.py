from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'input100', "placeholder":"Username"}))
    password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class': 'input100', "placeholder":"Password"}))

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is not None:
            return self.cleaned_data
        else:
            raise forms.ValidationError("Incorrect Username or Password", code='invalid_login')