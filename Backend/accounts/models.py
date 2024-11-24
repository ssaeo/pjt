from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import os

class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_img = models.ImageField(upload_to='image/', default='image/profile.png')
    fin_products = models.TextField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    wealth = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # 기존 프로필 이미지 삭제 (회원 정보 수정)
        if self.pk:
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_img and old_user.profile_img.url != self.profile_img.url:
                if old_user.profile_img.name != 'image/profile.png':
                    old_user.profile_img.delete(save=False)
        super().save(*args, **kwargs)