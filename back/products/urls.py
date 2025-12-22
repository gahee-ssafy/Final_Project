from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_products), # 예적금 조회
    path('spot/', views.spot_price),          # 현물(금/은) 조회
    # F08
    path('deposit/<str:fin_prdt_cd>/join/', views.join_deposit, name='join_deposit'),
]