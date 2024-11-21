from django.urls import path
from . import views

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit-products/top-rate/', views.top_rate, name='top_rate'),
    path('save-saving-products/', views.save_saving_products, name='save_saving_products'),
    path('saving-products/', views.saving_products, name='saving_products'),
    path('saving-product-options/<str:fin_prdt_cd>/', views.saving_product_options, name='saving_product_options'),
    path('saving-products/top-rate/', views.top_saving_rate, name='top_saving_rate'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:product_type>/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/join/', views.join_product, name='join_product'),
    path('products/cancel/', views.cancel_product, name='cancel_product'),
    path('products/user/', views.user_products, name='user_products'),
]