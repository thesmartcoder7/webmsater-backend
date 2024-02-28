from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from authusers.models import User
from authusers.serializers import UserSerializer
from django.shortcuts import get_object_or_404

import jwt, datetime



@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serialized = UserSerializer(users, many=True)
    return Response(serialized.data)


@api_view(['POST'])
def register(request):
    inbound_user = UserSerializer(data=request.data)

    if inbound_user.is_valid():
        inbound_user.save()
        return Response({"user": inbound_user.data})
  
    return Response(inbound_user.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = get_object_or_404(User, email=email)

    if not user:
        raise AuthenticationFailed('User not found!')
    else:
        logged_user = UserSerializer(user)
    
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect Password")
    
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    # token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        'jwt': token
    }

    return response
        

@api_view(['GET'])
def check_user(request):
    token = request.COOKIES.get('jwt')
    print(request.COOKIES.get('jwt'))
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    
    user = User.objects.get(id=payload['id'])
    serialized_user = UserSerializer(user)

    return Response(serialized_user.data)
      

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'Successfully Logged Out'
    }

    return response
