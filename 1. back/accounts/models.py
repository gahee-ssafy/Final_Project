from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 기본 필드 (AbstractUser가 제공): 
    # username, password, first_name, last_name, email, is_staff 등
    
    # [F02] 회원 커스터마이징 & [F09] 상품 추천 알고리즘을 위한 추가 필드
    nickname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(default=0)            # 나이 (추천 알고리즘용)
    money = models.IntegerField(default=0)          # 현재 자산 (추천 알고리즘용)
    salary = models.IntegerField(default=0)         # 연봉 (추천 알고리즘용)
    
    # [F04] 가입한 상품 목록 (쉼표로 구분된 텍스트로 저장하거나, 추후 M2M 필드로 변경 가능)
    # 지금은 간단하게 텍스트로 저장하는 방식을 제안합니다.
    financial_products = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username