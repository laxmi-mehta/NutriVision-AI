from django import forms
from django.contrib.auth import get_user_model
from .models import Posts
from django.contrib.auth.forms import AuthenticationForm
from .models import AdminProfile

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class AdminLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AdminProfile
        fields = ['email', 'password']


User = get_user_model()  # Dynamically fetch the user model

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image_url']

