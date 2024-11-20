from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)  # 사용자 이름
    email = models.EmailField()  # 이메일
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)  # 나이
    address = models.CharField(max_length=255, blank=True, null=True)  # 주소
    profile_img = models.ImageField(upload_to='image/', default='image/profile.png')  # 프로필 이미지
    fin_products = models.TextField(blank=True, null=True)  # 가입한 금융 상품 (쉼표 구분 텍스트)
    joined_date = models.DateTimeField(auto_now_add=True)  # 가입 날짜
    wealth = models.IntegerField(blank=True, null=True)  # 재산
    salary = models.IntegerField(blank=True, null=True)  # 월수입

    def __str__(self):
        return self.username
