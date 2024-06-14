from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest,CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email").lower()
        user = User.objects.filter(email=email).first()
        if user:
            attrs['email'] = user.email
        return super().validate(attrs)
        
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = FriendRequest
        fields = ['id','from_user','to_user','timestamp','accepted']