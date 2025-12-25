from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import User

from django.db.models import Max, Value
from django.db.models.functions import Coalesce

from products.models import DepositProducts


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, allow_blank=True)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["nickname"] = self.validated_data.get("nickname", "")
        data["money"] = self.validated_data.get("money", 0)
        data["salary"] = self.validated_data.get("salary", 0)
        return data

    def save(self, request):
        user = super().save(request)
        cleaned = self.get_cleaned_data()

        user.nickname = cleaned.get("nickname", "")
        user.money = cleaned.get("money", 0)
        user.salary = cleaned.get("salary", 0)
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "age",
            "money",
            "salary",
            "financial_products",
        )
        # 필요하면 email도 수정 가능하게 바꿀 수 있지만,
        # 보통 요구사항에는 없어서 read-only 추천
        read_only_fields = ("email",)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "nickname", "age", "money", "salary", "financial_products")


class JoinedDepositProductSerializer(serializers.ModelSerializer):
    # annotate로 내려주는 가공 필드
    max_intr_rate = serializers.FloatField()
    max_intr_rate2 = serializers.FloatField()

    class Meta:
        model = DepositProducts
        fields = ("fin_prdt_cd", "kor_co_nm", "fin_prdt_nm", "max_intr_rate", "max_intr_rate2")


class UserProfileSerializer(serializers.ModelSerializer):
    joined_products = serializers.SerializerMethodField()
    chart = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "age",
            "money",
            "salary",
            "joined_products",
            "chart",
        )

    def _get_joined_codes(self, user: User) -> list[str]:
        raw = user.financial_products or ""
        return [c.strip() for c in raw.split(",") if c.strip()]

    def get_joined_products(self, user: User):
        codes = self._get_joined_codes(user)
        if not codes:
            return []

        qs = (
            DepositProducts.objects
            .filter(fin_prdt_cd__in=codes)
            .annotate(
                # ✅ 금리 옵션이 없거나(null) max가 None이면 0.0으로 강제
                max_intr_rate=Coalesce(Max("options__intr_rate"), Value(0.0)),
                max_intr_rate2=Coalesce(Max("options__intr_rate2"), Value(0.0)),
            )
            .order_by("kor_co_nm", "fin_prdt_nm")
        )
        return JoinedDepositProductSerializer(qs, many=True).data

    def get_chart(self, user: User):
        products = self.get_joined_products(user)
        labels = [p["fin_prdt_nm"] for p in products]
        values = [p["max_intr_rate2"] for p in products]  # 이미 0.0 처리됨
        return {"labels": labels, "values": values}


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # ✅ email 수정은 막는 걸 추천 (요구사항에 보통 없음)
        fields = ("first_name", "last_name", "nickname", "age", "money", "salary")
