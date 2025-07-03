import json
import os
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Invalid email')

        file_path = os.path.join(os.getcwd(), 'users.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    users = json.load(f)
                    if any(user['email'] == value for user in users):
                        raise serializers.ValidationError('Email already exists')
                except json.JSONDecodeError:
                    pass
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters')
        return value

    def create(self, validated_data):
        file_path = os.path.join(os.getcwd(), 'users.json')

        validated_data['password'] = make_password(validated_data['password'])
        
        users = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []

      
        users.append(validated_data)

        with open(file_path, 'w') as f:
            json.dump(users, f, indent=4)

        return validated_data