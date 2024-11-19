from django.db import models

# Create your models here.
# finlife/models.py

class DepositProducts(models.Model): # 예금상품
    fin_prdt_cd = models.TextField(unique=True)         # 금융 상품 코드
    kor_co_nm = models.TextField()                      # 금융회사명
    fin_prdt_nm = models.TextField()                    # 금융 상품명
    etc_note = models.TextField()                       # 금융 상품 설명
    join_deny = models.IntegerField()                   # 가입 제한 (1: 제한없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField()                    # 가입 대상
    join_way = models.TextField()                       # 가입 방법
    spcl_cnd = models.TextField()                       # 우대조건

class DepositOptions(models.Model): # 예금상품 옵션
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명 - 단리/복리
    intr_rate = models.FloatField()                         # 저축금리 
    intr_rate2 = models.FloatField()                        # 최고우대금리 
    save_trm = models.IntegerField()                        # 저축기간 (단위:개월)

class SavingProducts(models.Model): # 적금상품
    fin_prdt_cd = models.TextField(unique=True)         # 금융 상품 코드
    kor_co_nm = models.TextField()                      # 금융회사명
    fin_prdt_nm = models.TextField()                    # 금융 상품명
    etc_note = models.TextField()                       # 금융 상품 설명
    join_deny = models.IntegerField()                   # 가입 제한 (1: 제한없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField()                    # 가입 대상
    join_way = models.TextField()                       # 가입 방법
    spcl_cnd = models.TextField()                       # 우대조건

class SavingOptions(models.Model): # 적금상품 옵션
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명
    intr_rate = models.FloatField()                         # 저축금리 
    intr_rate2 = models.FloatField()                        # 최고우대금리 
    save_trm = models.IntegerField()                        # 저축기간 (단위:개월)
    # rsrv_type_nm = models.CharField(max_length=100)         # 저금형태 / 자유적립,정액정립