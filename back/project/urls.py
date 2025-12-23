from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # products
    path('api/v1/products/', include('products.urls')),

    # ✅ accounts (로그인/로그아웃/회원가입/me 등 전부 accounts/urls.py에서 관리)
    path('accounts/', include('accounts.urls')),

    # community
    path('api/v1/community/', include('community.urls')),
]
