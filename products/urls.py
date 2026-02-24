from django.urls import path
from . import views


urlpatterns = [
    path('category/list/', views.category_list, name='category_list'),
    path('categories/update/<int:id>/', views.category_update, name='category_update'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    
    path('expense/category/', views.expense_category_view, name='expense_category'),
    path('expense/category/delete/<int:id>/', views.expense_category_delete, name='expense_category_delete'),
    path("expense/category/update/<int:id>/", views.expense_category_update, name="expense_category_update"),
    
    path('income/category/', views.income_category_view, name='income_category'),
    path('income/category/delete/<int:id>/', views.income_category_delete, name='income_category_delete'),
    path("income/category/update/<int:id>/", views.income_category_update, name="income_category_update"),
    
    path('list/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
    path('supplier/', views.supplier_list, name='supplier'),
    path('supplier/create/', views.supplier_create, name='supplier_create'),
    path('supplier/update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('supplier/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    
    path('customer/', views.customer_list, name='customer'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/update/<int:pk>/', views.customer_update, name='customer_update'),
    path('customer/delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    
    path('index/', views.index, name='index'),
    
    path('settings/list/', views.settings_list, name='settings_list'),
    path('setting/create/', views.setting_create, name='setting_create'),
    path('settins/update/<int:pk>/', views.setting_update, name='settings_update'),
    
    path('fund/', views.fund_list, name='fund_list'),
    path('fund/create/', views.fund_create, name='fund_create'),
    path('fund/update/<int:id>/', views.fund_update, name='fund_update'),
    path('fund/delete/<int:id>/', views.fund_delete, name='fund_delete'),
    
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:id>/update/', views.expense_update, name='expense_update'),
    path('expenses/<int:id>/delete/', views.expense_delete, name='expense_delete'),
    
    path('income/list/', views.income_list, name='income_list'),
    path('income/create/', views.income_create, name='income_create'),
    path('income/<int:id>/update/', views.income_update, name='income_update'),
    path('income/<int:id>/delete/', views.income_delete, name='income_delete'),
    
    path('supplier-payment/list/', views.payment_list, name='supplier_payment_list'),
    path('supplier-payment/create/', views.payment_create, name='supplier_payment_create'),
    path('supplier-payment/<int:id>/update/', views.payment_update, name='payment_update'),
    path('supplier-payment/<int:id>/delete/', views.payment_delete, name='payment_delete'),
    
    path('customer-payment/list/', views.customer_payment_list, name='customer_payment_list'),
    path('customer-payment/create/', views.customer_payment_create, name='customer_payment_create'),
    path('customer-payment/<int:id>/update/', views.customer_payment_update, name='customer_payment_update'),
    path('customer-payment/<int:id>/delete/', views.customer_payment_delete, name='customer_payment_delete'),
    
    path('fund-transfer/list/', views.fund_transfer_list, name='fund_transfer_list'),
    path('fund-transfer/create/', views.fund_transfer_create, name='fund_transfer_create'),
    path('fund-transfer/<int:pk>/update/', views.fund_transfer_update, name='fund_transfer_update'),
    path('fund-transfer/<int:id>/delete/', views.fund_transfer_delete, name='fund_transfer_delete'),
    
    path('orders/create/', views.create_collect_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/category/<int:category_id>/', views.order_list, name='order_list_by_category'),
    path('order/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('pending/order/', views.pending_order_list, name='pending_orders'),

    path('purchase/list/', views.purchase_list, name='purchase_list'),
    path('purchase/create/', views.purchase_create, name='purchase_create'),
    path('purchase/update/<int:id>/', views.purchase_update, name='purchase_update'),
    path('purchase/delete/<int:id>/', views.purchase_delete, name='purchase_delete'),

    path('purchase/return/', views.purchase_return, name='purchase_return'),
    path('purchase/return/list/', views.purchase_return_list, name='purchase_return_list'),
    
    path('sales/report/', views.sales_report_list, name='sales_report'),
    
    path('purchase/report/', views.purchase_report, name='purchase_report'),

]


