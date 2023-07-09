from django.contrib.auth.models import User
from django import forms

from .models import UserProfile, Photo

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def save(self):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        # first set_password, then save, or the password can't be saved correctly
        user.save()
        profile = UserProfile.objects.create(user=user)
        return profile

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']