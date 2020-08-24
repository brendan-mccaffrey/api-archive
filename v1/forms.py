from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):

    class Meta:

		model = Profile
		fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only': True}
		}

class ProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = UserChangeForm.Meta.fields