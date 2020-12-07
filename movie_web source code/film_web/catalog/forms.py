from django import forms
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    name = forms.CharField(label='Username:', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='Password:', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    #regular expression constraint + username&password
    regex_name = r'^[a-z0-9_-]{3,16}$'
    regex_password = r'^[a-z0-9_-]{6,18}$'
    username_validator = RegexValidator(regex=regex_name, message='Username invaild')
    password_validator = RegexValidator(regex=regex_password, message='Password invaild')
    
    name = forms.CharField(label='Username', max_length=128, validators=[username_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='Password', max_length=256, validators=[password_validator], widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_pw = forms.CharField(label='Confirm Password', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    email = forms.EmailField(label='Email', max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
