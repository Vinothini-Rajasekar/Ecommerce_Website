from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('product_list', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    #path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart_quantity, name='update_cart'),

    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    #path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cards/', views.card_view, name='card_view'),
    path('add_card/<int:id>', views.add_card, name='add_card'),
    #path('cart/', views.view_cart, name='view_cart'),
    
    
    path('payment/', views.payment_page, name='payment_page'),  # Payment page where user selects COD
    path('process-payment/', views.process_cod_payment, name='process_cod_payment'),  # Handle Cash on Delivery payment

    
    
]
