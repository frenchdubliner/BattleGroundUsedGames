from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    # Add User model fields
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(),
            'display_name': forms.TextInput(attrs={'placeholder': 'Add Display Name'}),
            'info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add Information'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for User fields if instance exists
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone_number'].initial = self.instance.phone_number
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update phone_number field
        profile.phone_number = self.cleaned_data['phone_number']
        if commit:
            profile.save()
            # Update User model fields
            if profile.user:
                profile.user.first_name = self.cleaned_data['first_name']
                profile.user.last_name = self.cleaned_data['last_name']
                profile.user.save()
        return profile

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter new email address'})
        }
       