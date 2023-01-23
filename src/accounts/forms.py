from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']