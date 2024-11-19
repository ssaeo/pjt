from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),           # 회원가입
    path('login/', views.login, name='login'),             # 로그인
    path('profile/<str:username>/', views.profile, name='profile'),  # 프로필 조회 및 수정
    path('delete/<str:username>/', views.delete_user, name='delete_user'),  # 회원 탈퇴
]
