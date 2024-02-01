from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


# register serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'email', 'password', 'password1']
        extra_kwargs = {'password': {'write_only': True}}
    
    
    def create(self, validated_data):
        if validated_data['password'] == validated_data['password1']:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        raise serializers.ValidationError("passwords doesn't match")

# login serializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")