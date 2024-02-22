# from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from users.serializers import UserSerializer


@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serialized = UserSerializer(users, many=True)
    return Response({'users': serialized.data})


@api_view(['GET'])
def check_user(request):
    try:
        user = User.objects.get(email=request.query_params.get('email'))
        if user:
            return Response({'message': 'User exists'})
    except:
        return Response({'message': 'User doen not exist'})
