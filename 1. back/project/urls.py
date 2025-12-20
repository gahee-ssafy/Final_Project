from django.contrib import admin
from django.urls import path, include  # include를 꼭 임포트해야 합니다!

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # [F02] 회원가입 및 로그인 URL 연결
    # 1. 로그인, 로그아웃, 비밀번호 변경 등 (dj-rest-auth 기본)
    path('accounts/', include('dj_rest_auth.urls')),
    
    # 2. 회원가입 (dj-rest-auth.registration)
    path('accounts/registration/', include('dj_rest_auth.registration.urls')),
]
