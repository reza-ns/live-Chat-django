from rest_framework.serializers import ModelSerializer
from users.models import User


class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')