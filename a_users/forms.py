from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(),
            'display_name': forms.TextInput(attrs={'placeholder': 'Add Display Name'}),
            'info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add Information'}),
        }

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter new email address'})
        }
       