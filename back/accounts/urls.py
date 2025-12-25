from django.urls import path, include
from .views import CustomRegisterView, MeView

urlpatterns = [
    # ✅ dj-rest-auth 기본 URL들: login/, logout/, password/change/ 등
    path('', include('dj_rest_auth.urls')),

    # ✅ 회원가입
    path('signup/', CustomRegisterView.as_view(), name='signup'),

    # ✅ 마이페이지(내 정보 조회/수정)
    path('me/', MeView.as_view(), name='me'),
]
