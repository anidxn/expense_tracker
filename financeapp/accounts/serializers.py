from rest_framework import serializers
# from .models import CustomUser
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = CustomUser(username=validated_data['username'], email=validated_data['email'])
        user = User.objects.create_user(validated_data['username'], validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user