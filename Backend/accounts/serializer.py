from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',  # Primary Key
            'username',
            'email',
            'age',
            'address',
            'fin_products',
            'joined_date',
            'is_active',  # AbstractUser에서 상속받은 필드
            'is_staff',   # AbstractUser에서 상속받은 필드
        ]
        read_only_fields = ['id', 'joined_date', 'is_active', 'is_staff']  # 읽기 전용 필드
