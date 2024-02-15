# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=500, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username','bio', 'email']

