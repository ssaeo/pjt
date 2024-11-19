from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article-list'),
    path('<int:article_pk>/', views.article_detail, name='article-detail'),
    path('user/<str:username>/', views.user_article_list, name='user-article-list'),
    path('<int:article_pk>/comments/', views.comment_list, name='comment-list'),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment-detail'),
]
