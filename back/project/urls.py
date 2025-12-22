from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # products 앱의 URL을 /api/v1/products/ 로 시작하게 연결
    path('api/v1/products/', include('products.urls')),
    # 로그인/회원가입
    path('accounts/', include('dj_rest_auth.urls')),                # 로그인, 로그아웃
    # path('accounts/signup/', include('dj_rest_auth.registration.urls')), # 회원가입
    path('accounts/signup/', CustomRegisterView.as_view(), name='rest_register'),
    path('accounts/', include('accounts.urls')),
]