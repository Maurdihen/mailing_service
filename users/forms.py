from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('email', 'username', 'avatar', 'phone', 'country')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        } 