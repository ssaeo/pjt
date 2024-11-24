from django.db import models

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
    # rsrv_type_nm = models.CharField(max_length=100)         # 적립유형 > 자유적립 / 정액적립식 >> 이건 적금에만 있으므로 제외
    intr_rate = models.FloatField()                         # 저축금리 
    intr_rate2 = models.FloatField()                        # 최고우대금리 
    save_trm = models.IntegerField()                        # 저축기간 (단위:개월)

class SavingProducts(models.Model): # 적금상품
    fin_prdt_cd = models.TextField(unique=True)         # 금융 상품 코드
    kor_co_nm = models.TextField()                      # 금융회사명
    fin_prdt_nm = models.TextField()                    # 금융 상품명
    etc_note = models.TextField()                       # 금융 상품 설명
    join_deny = models.IntegerField()                   # 가입 제한
    join_member = models.TextField()                    # 가입 대상
    join_way = models.TextField()                       # 가입 방법
    spcl_cnd = models.TextField()                       # 우대조건

class SavingOptions(models.Model): # 적금상품 옵션
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명 // 복리 or 단리
    rsrv_type_nm = models.CharField(max_length=100, null=True, blank=True)    # 적립유형 > 자유적립 / 정액적립식 / black, null 추가했는데 오류뜨면 수정
    intr_rate = models.FloatField()                         # 저축금리 
    intr_rate2 = models.FloatField()                        # 최고우대금리 
    save_trm = models.IntegerField()                        # 저축기간 (단위:개월)