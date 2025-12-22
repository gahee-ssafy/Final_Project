from django.urls import path, include
# [수정] views.py에서 CustomRegisterView를 가져옵니다.
from .views import CustomRegisterView 

app_name = 'accounts'

urlpatterns = [
    # 1. 회원가입: CustomRegisterView 사용
    # 기존에 오류가 나던 views.signup 대신, 클래스형 뷰인 as_view()를 사용합니다.
    path('signup/', CustomRegisterView.as_view(), name='rest_register'),

    # 2. 로그인, 로그아웃, 비밀번호 변경, 내 정보 조회(/user/) 등
    # dj_rest_auth 라이브러리의 기능을 통째로 가져옵니다.
    # 이 한 줄로 'login/', 'logout/', 'user/', 'password/change/' 등이 모두 생성됩니다.
    path('', include('dj_rest_auth.urls')),
]