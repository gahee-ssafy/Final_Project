from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # products 앱의 URL을 /api/v1/products/ 로 시작하게 연결
    path('api/v1/products/', include('products.urls')),
]