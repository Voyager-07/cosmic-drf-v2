from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Include fields you want to expose via API
        fields = ['id', 'email', 'name', 'username', 'bio', 'role', 'pfp']
        read_only_fields = ['id', 'role', 'email', 'username']
