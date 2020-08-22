import json
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from v1.models import Profile


def index(request):
    return HttpResponse(Profile.objects.all())

@api_view(['POST',])
def registration_view(request):

	serializer = RegistrationSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		profile = serializer.save()
		data['response'] = "Successfully registered a new user!"
		token = Token.objects.get(user=profile).key
		data['token'] = token
		data['email'] = profile.email
		data['username'] = profile.username
		data['first_name'] = profile.first_name
		data['last_name'] = profile.last_name
		data['phone'] = profile.phone
		data['address'] = profile.address
		data['birth_date'] = profile.birth_date
		
	else:
		data = serializer.errors

	return Response(data)