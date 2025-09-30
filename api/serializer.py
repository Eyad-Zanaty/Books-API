from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
            user = User(
                username=validated_data['username'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                email=validated_data.get('email', ''),
                is_staff=validated_data.get('is_staff', False),
                is_active=validated_data.get('is_active', True),
                is_superuser=validated_data.get('is_superuser', False)
            )
            
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError({"email": "Email is already in use."})
            
            user.set_password(validated_data['password'])
            user.save()
            return user