from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from utils.rest_crud_handler import get_related_object

class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=0, max_value=120, required=True)  
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'age']

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_email(self, value):
        user = get_related_object(value, User, 'email')
        if user is None:
            return value
        raise serializers.ValidationError("A user with this email already exists.")

    def create(self, validated_data):
        age = validated_data.pop('age') 
        email = validated_data.pop('email')  
        user = User.objects.create(username=email, email=email, **validated_data)  
        UserProfile.objects.create(user_id=user.id, age=age) 
        return user