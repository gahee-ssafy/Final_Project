from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    # 기본 필드 외에 추가로 입력받고 싶은 필드 정의
    nickname = serializers.CharField(max_length=20, required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    # age = serializers.IntegerField(required=False) # 필요하면 주석 해제

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['money'] = self.validated_data.get('money', 0)
        data['salary'] = self.validated_data.get('salary', 0)
        # data['age'] = self.validated_data.get('age', 0)
        return data

    def save(self, request):
        user = super().save(request)
        # cleaned_data에 저장된 값을 user 모델의 필드에 할당
        user.nickname = self.cleaned_data.get('nickname')
        user.money = self.cleaned_data.get('money')
        user.salary = self.cleaned_data.get('salary')
        # user.age = self.cleaned_data.get('age')
        user.save()
        return user