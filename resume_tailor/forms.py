from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, ResumeUpload

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 101)
    last_name = forms.CharField(max_length = 101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',\
         'email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['loc', 'phone', 'linkedin']

class UploadFileForm(forms.ModelForm):

    class Meta:
        model = ResumeUpload
        fields = ['title', 'resume']
