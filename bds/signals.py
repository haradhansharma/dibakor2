from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from bds.middleware import GetCurentUser
import requests
from django.conf import settings



        

        
        
    


# @receiver(pre_save, sender=Order)
# def update_order(sender, instance, *args, **kwargs,):
#     curent_user = GetCurentUser().instance    

    
#     if instance.id is None: # new object created here
#         pass
#     else:
#         previous = sender.objects.get(id = instance.id)
#         saving = instance
        
        
#         # When changing order status from admin
#         if previous.last_status != saving.last_status:            
#             OrderStatus.objects.create(status = saving.last_status, update_by = curent_user)
            
            
#             order_invoice = Invoice.objects.get(order = instance)
#             order_invoice.order_status = saving.last_status
#             order_invoice.save()
            
#             InvoiceRecord.objects.create(invoice = order_invoice, invoice_remarks = f'Changed during order status update by user {curent_user.email}')


# @receiver(pre_save, sender=OrderStatus)
# def update_order(sender, instance, *args, **kwargs,):
#     curent_user = GetCurentUser().instance   
#     if instance.id is None: # new order will be created
#         pass 
#     else:
#         previous = sender.objects.get(id = instance.id)
#         saving = instance
#         if saving.status == 'hold':
#             saving.remarks = "Order Marked as hold. It's genarelly happend while no payment verified succesfully!"
#             saving.update_by = curent_user
#             saving.save()
            
#             order = Order.objects.get(id = saving.order.id)
#             order.last_status = saving.status
#             order.save()
            
#             invoice = order.orderinvoice
#             invoice.order_status = saving.status
#             invoice.save()
            
#             invoice_record = InvoiceRecord.objects.get(invoice = invoice)

@receiver(post_save, sender=BdService)
def set_price(sender, instance, created, *args, **kwargs):
    
    bdt_rate = instance.bdt_rate
    if instance.option_price_auto_calculate:
        service_option = instance.serviceoptions_set.all()
        
        for so in service_option:
            value = (so.apndix * so.require_day_to_complete * bdt_rate) * settings.PROFIT_INTEREST_WITH_DOLLAR_INVESTMENT / 100
            before_day = so.require_day_to_complete * settings.SHOULD_PAID_PERCENT / 100
            so.full_payment_before_day = int(before_day)
            so.value = value
            so.save()
        
        
        

@receiver(post_save, sender=Transection)
def verify_transection(sender, instance, created, *args, **kwargs):
    get_global = GetCurentUser()
    curent_user = get_global.instance   
    if not created:
        if instance.verified and not instance.paying_commited:
            print('call Tras signal')
            # instance.vefiried_by = f'By user #{curent_user.id}' 
            # instance.verified = True 
            # instance.value = instance.paying_amount   
            # instance.paying_commited = True 
            # instance.save()
            
            order = instance.order
            # order.paid_amount += instance.paying_amount  
            # order.save() 
            
            OrderStatus.objects.create(
                order = order,
                status = 'paid', # it will call the orderstatus signal
                due = order.total_due,
                remarks = 'Created during payment verification',
                update_by = curent_user.id  
                
            )
        
        

@receiver(post_save, sender=OrderStatus)
def update_order_status(sender, instance, created, *args, **kwargs):
    get_global = GetCurentUser()
    curent_user = get_global.instance   
    if created:
        instance.update_by = f'By user #{curent_user.id}'      
        instance.save()
  
        status = instance.status
        
        
        order = instance.order
        
        
        if status == 'pending' or status =='processing' or status =='progressing' or status =='partial_progressing' :
            if curent_user.is_staff:
                from django.contrib import messages
                rqst = get_global.staff_request
                messages.error(rqst, 'The selected status has no effect in the admin!')
            else:
                pass
            
            
        elif status == 'over_due':
            order.last_status = status
            order.save() 
            
            invoice = order.orderinvoice
            invoice.order_status = status            
            invoice.save()      
            
            InvoiceRecord.objects.create(invoice = invoice, invoice_remarks = f"Order marked as overdue as {order.full_payment_date} over!")
            
        elif status == 'complete':
            order.last_status = status
            order.save() 
            
            invoice = order.orderinvoice
            invoice.order_status = status            
            invoice.save()
            
            
            
            InvoiceRecord.objects.create(invoice = invoice, invoice_remarks = f"Order completed by {curent_user.id}! it's naturally happend if order marked as completed!")
            

        
        elif status == 'payment_reject':  
            
            order.last_status = status
            order.save()               
            
            invoice = order.orderinvoice
            invoice.order_status = status            
            invoice.save()
            
            InvoiceRecord.objects.create(invoice = invoice, invoice_remarks = f"Payment Reject by {curent_user.id}! it's naturally happend if no pament verified!")
            
        elif status == 'paid':
         
            print('call paid status')
             
            trans = Transection.objects.filter(order = order, paying_commited = False, verified = True)   #Paying comited false is mandatory here
            non_comited_paying = 0         
            for t in trans:
                print('loop running__')
                non_comited_paying += t.paying_amount
                t.value = t.paying_amount
                t.paying_commited = True #marktig as comited nt to add further
                t.save()
            
            order.last_status = status
            order.paid_amount += non_comited_paying   
            # order.paying_amount = 0         
            order.save()              
            
            due_amount = order.total_due
            
            instance.due = due_amount # as it i updating no recall from here
            instance.save()          
            
            
            # Transection.objects.create(
            #     order = order, 
            #     payment_method = order.payment_method, 
            #     value = order.paid_amount,                
            #     remarks = 'Payment Accepted in admin'
            #     ) 
         
            invoice = order.orderinvoice
            invoice.order_status = status    
            invoice.paid_amount = order.paid_amount                  
            invoice.save()  
            
            # InvoiceRecord.objects.create(invoice = invoice, invoice_remarks = 'Invoice marked as paid by admin')
            
            if due_amount > 0:
                sufix_text = 'Partial'
                progressing = 'partial_progressing'
            else:
                sufix_text = 'Full'
                progressing = 'progressing'
               
            order.last_status = progressing
            order.save() 
            
            invoice.order_status = progressing  
            invoice.save()   
            
            InvoiceRecord.objects.create(invoice = invoice, invoice_remarks = 'As amount updated seting progressing status') 
            
           
            OrderStatus.objects.create( # it should be at th last as it will call again
                order = order,
                status = progressing,
                due = due_amount,
                remarks = f'{sufix_text} Payment Accepted by {curent_user.id}',
                update_by = curent_user.id                
            )
        else:
            if curent_user.is_staff or curent_user.is_superuser:
                messages.error(rqst, 'Nothing happend!')
            

    
    


# OrderStatus
# Invoice
# InvoiceRecord
# Transection