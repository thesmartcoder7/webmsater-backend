from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from authusers.models import User
from authusers.serializers import UserSerializer

import jwt, datetime



@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serialized = UserSerializer(users, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def retrieve_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        raise AuthenticationFailed('Unauthenticated')
    
    user = User.objects.get(id=payload['id'])
    serialized_user = UserSerializer(user)

    return Response(serialized_user.data)


@api_view(['POST'])
def register(request):
    inbound_user = UserSerializer(data=request.data)
    inbound_user.is_valid(raise_exception=True)
    inbound_user.save()
    return Response(inbound_user.data)

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.get(email=email)

    if not user:
        raise AuthenticationFailed
    else:
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        else:

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            # depricated:
            # token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)

            response.data = {
                'jwt': token
            }

            return response
        

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'Successfully Logged Out'
    }

    return response