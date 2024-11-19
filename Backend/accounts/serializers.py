from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # 비밀번호는 쓰기 전용

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'name', 
            'age', 'address', 'profile_img', 'fin_products', 
            'joined_date', 'is_active', 'is_staff',
        ]
        read_only_fields = ['id', 'joined_date', 'is_active', 'is_staff']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            address=validated_data.get('address'),
            profile_img=validated_data.get('profile_img'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update only writable fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
