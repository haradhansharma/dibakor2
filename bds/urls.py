
from django.urls import path
from . import views
import math





app_name = 'bds'


urlpatterns = [
    path('', views.ServiceList.as_view(), name='bds_list'),  
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='service_detail'),  
    path('order-confirm/<int:order_id>', views.OrderConfirm.as_view(), name='order_confirm'),  
    path('pay-instruction/', views.payment_instruction, name = 'payment_instruction'),
    path('should-paid/', views.should_paid, name='should_paid'),  
    path('should-partial-paid/', views.should_partial_paid, name='should_partial_paid'),    
      
    path('invoice/<int:invoice_id>', views.invoice, name='invoice'),
    path('invoicepdf/<int:invoice_id>', views.invoicepdf, name='invoicepdf'),    
    path('delete-extra-file/<int:id>/<int:order_id>', views.delete_extra_file, name='delete_extra_file'),
    path('due-payment/<int:id>/<int:order_id>', views.DuePayment.as_view(), name='due_payment')
    
    
]



