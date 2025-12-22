from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # [F02] 회원 커스터마이징 & [F09] 상품 추천 알고리즘을 위한 추가 필드
    nickname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(default=0, null=True, blank=True)      # 나이
    money = models.IntegerField(default=0, null=True, blank=True)    # 현재 자산
    salary = models.IntegerField(default=0, null=True, blank=True)   # 연봉

    # [F08] 가입한 상품 목록 (ManyToManyField)
    # 핵심 수정 사항: 모델 클래스를 직접 import하지 않고 '앱이름.모델명' 문자열로 참조합니다.
    # 이렇게 하면 ImportError(순환 참조)를 완벽하게 방지할 수 있습니다.
    joined_deposits = models.ManyToManyField(
        'products.DepositProducts', 
        blank=True, 
        related_name='joined_users'
    )
    
    joined_savings = models.ManyToManyField(
        'products.SavingProducts', 
        blank=True, 
        related_name='joined_users'
    )

    def __str__(self):
        return self.username
    