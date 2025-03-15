from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from utils.rest_crud_handler import get_related_object

class UserSerializer(serializers.ModelSerializer):

    # Email and Age (with age validation) fields a mandatory
    age = serializers.IntegerField(min_value=0, max_value=120, required=True)  
    email = serializers.EmailField(required=True)

    class Meta:
        # Auth user table
        model = User
        fields = ['first_name', 'email', 'age']

    # First name validation
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    # Email existing validation
    def validate_email(self, value):
        user = get_related_object(value, User, 'email')
        if user is None:
            return value
        raise serializers.ValidationError("A user with this email already exists.")

    # Create User and UserProfile objects with validated data
    def create(self, validated_data):
        age = validated_data.pop('age') 
        email = validated_data.pop('email')  
        user = User.objects.create(username=email, email=email, **validated_data)  
        UserProfile.objects.create(user_id=user.id, age=age) 
        return user