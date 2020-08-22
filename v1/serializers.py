from rest_framework import serializers
from v1.models import Profile, Transaction, Account
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:

		model = Profile
		fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'address', 
				'birth_date', 'password', 'password2', 'is_superuser', 'is_admin', 'is_staff', 'is_active']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def save(self):
		profile = Profile(
				email = self.validated_data['email'],
				username = self.validated_data['username'],
				first_name = self.validated_data['first_name'],
				last_name = self.validated_data['last_name'],
				phone = self.validated_data['phone'],
				address = self.validated_data['address'],
				birth_date = self.validated_data['birth_date'],

			)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		profile.set_password(password)
		profile.save()
		return profile

