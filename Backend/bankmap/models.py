from django.db import models

class BankBranch(models.Model):
    BANK_CHOICES = [
        ('004', '국민은행'),
        ('011', '농협은행'),
        ('020', '우리은행'),
        ('081', '하나은행'),
    ]

    brch_name = models.CharField(max_length=100)
    addr = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    brch_telno = models.CharField(max_length=20, null=True, blank=True)
    bank_code = models.CharField(
        max_length=3, 
        choices=BANK_CHOICES,
        null=True,  # null 허용
        blank=True  # 폼에서 빈 값 허용
    )

    def __str__(self):
        return f"[{self.get_bank_code_display()}] {self.brch_name}"