from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
    # name = models.CharField(max_length=30)
    # password = models.CharField()
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)     # 양수 + 1이상
    address = models.CharField(max_length=255, blank=True, null=True)
    # profile_img = models.ImageField(upload_to='', default='') 폴더 추가예정
    fin_products = models.TextField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    # AbstractUser에 이미 포함되어 작성하지 않은 필드
    '''
    username
    password
    is_active - 정지, 탈퇴 데이터 관리용
    is_staff - 관리자
    '''
    # 커스텀 유저관련, 예적금 추가필요 

    
    def __str__(self):
        return self.username