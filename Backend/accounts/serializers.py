from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password', 'email', 'name', 
            'age', 'address', 'profile_img', 'fin_products',
            'wealth', 'salary'
        )

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),  # 이메일 저장
            name=validated_data.get('name', ''),    # 이름 저장
            age=validated_data.get('age'),          # 나이 저장
            address=validated_data.get('address', ''),  # 주소 저장
            wealth=validated_data.get('wealth'),    # 재산 저장
            salary=validated_data.get('salary'),    # 월수입 저장
        )
        return user