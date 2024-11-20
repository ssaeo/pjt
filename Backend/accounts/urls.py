from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),           # 회원가입
    path('login/', views.login, name='login'),             # 로그인
    path('logout/', views.logout, name='logout'),           # 로그아웃
    path('profile/<str:username>/', views.profile, name='profile'),  # 프로필 조회 및 수정
    
]
