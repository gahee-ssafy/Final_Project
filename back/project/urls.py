from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # products 앱의 URL을 /api/v1/products/ 로 시작하게 연결
    path('api/v1/products/', include('products.urls')),
    # 인증 관련 URl은 accounts로
    path('accounts/', include('accounts.urls')),   
]