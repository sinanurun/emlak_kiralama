from django.urls import path

from . import views
#app_name = 'user'
urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('user_rentalads/', views.user_rentalads, name='user_rentalads'),
    path('user_rentalads_add/', views.user_rentalads_add, name='user_rentalads_add'),
    path('delete_rentalad/<int:id>', views.user_delete_rentalad,name='user_delete_rentalad' ),
    path('update_rentalad/<int:id>', views.user_update_rentalad,name='user_update_rentalad' ),
    # path('orders_product/', views.user_order_product, name='user_order_product'),
    # path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    # path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),

]