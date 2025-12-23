from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

# F08
from .models import User
from products.models import DepositProducts, SavingProducts

# F08
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts # 예금/적금 구조가 비슷하므로 예시로 작성
        fields = ('fin_prdt_nm', 'kor_co_nm', 'id')

class UserProfileSerializer(serializers.ModelSerializer):
    # 가입한 상품의 상세 정보를 포함
    joined_deposit_products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'nickname', 'age', 'money', 'joined_deposit_products')
        read_only_fields = ('username',)


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, allow_blank=True)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['money'] = self.validated_data.get('money', 0)
        data['salary'] = self.validated_data.get('salary', 0)
        return data

    def save(self, request):
        user = super().save(request)
        cleaned = self.get_cleaned_data()

        # ✅ 네 User 모델 필드명이 nickname/money/salary 라는 전제
        user.nickname = cleaned.get('nickname', '')
        user.money = cleaned.get('money', 0)
        user.salary = cleaned.get('salary', 0)
        user.save()
        return user


from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        # dj-rest-auth 기본 필드 + 우리가 추가한 필드들
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'nickname',
            'age',
            'money',
            'salary',
            'financial_products',
        )
        read_only_fields = ('email',)


from rest_framework import serializers
from .models import User

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'nickname', 'age', 'money', 'salary', 'financial_products')
