from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authusers.models import User
from authusers.serializers import UserSerializer


@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serialized = UserSerializer(users, many=True)

    return Response(serialized.data)

@api_view(['POST'])
def register(request):
    inbound_user = UserSerializer(data=request.data)
    inbound_user.is_valid(raise_exception=True)
    inbound_user.save()

    return Response(inbound_user.data)


def login(request):
    ...
