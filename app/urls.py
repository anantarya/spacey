# urls.py

from django.urls import path
from .views import product_view, customer_view, employee_view, token_view, order_view

urlpatterns = [
    path('api/products/', product_view.product, name='products-list'),
    path('api/products_add/', product_view.product_add, name='products-add'),
    path('api/products_update/<int:id>', product_view.product_update, name='products-update'),
    path('api/products_delete/<int:id>', product_view.product_delete, name='products-delete'),
    
    path('api/customers_add/', customer_view.create_customer, name='create-customer'),
    path('api/customers/', customer_view.get_customers, name='get-customers'),
    path('api/customers_update/<int:pk>/', customer_view.update_customer, name='update-customer'),
    path('api/customers_delete/<int:pk>/', customer_view.delete_customer, name='delete-customer'),
    
    path('employee/register/', employee_view.employee_register, name='employee_register'),
    
    path('api/token/', token_view.obtain_token_pair_view, name='token_obtain_pair'),
    
    path('bill/', order_view.bill_customer, name='bill_customer'),
    path('orders/', order_view.get_past_orders, name='past_orders'),
    
]

