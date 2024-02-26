from rest_framework.serializers import ModelSerializer
from authusers.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'password']