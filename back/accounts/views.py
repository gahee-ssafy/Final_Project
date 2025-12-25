# back/accounts/views.py

from dj_rest_auth.registration.views import RegisterView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .serializers import (
    CustomRegisterSerializer,
    UserMeSerializer,                 # 혹시 다른 곳에서 쓰면 유지
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class MeView(APIView):
    """
    F08 프로필 페이지용 API
    - GET  : 내 회원 기본 정보 + 가입상품 리스트 + 차트 데이터
    - PATCH: 내 회원 정보 수정 후, 최신 프로필 데이터 반환
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # F08 요구사항용 프로필 응답(가입상품/차트 포함)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # 회원 정보 수정(부분 수정)
        update_serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        # 수정 후 최신 프로필 반환
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
