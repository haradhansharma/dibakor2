from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . models import *
from django.contrib import messages

class ServiceOptionInline(admin.TabularInline):
    model = ServiceOptions
    extra = 0
    
class RequiredOptionInline(admin.TabularInline):
    model = RequiredOption
    extra = 0
class ServiceImagesInline(admin.TabularInline):
    model = ServiceImages
    extra = 0
class BdServiceAdmin(admin.ModelAdmin):
    model = BdService
    
    inlines = [ServiceOptionInline, RequiredOptionInline, ServiceImagesInline]


admin.site.register(BdService, BdServiceAdmin)

admin.site.register(PaymentMethod)


class TransectionAdmin(admin.ModelAdmin):
    model = Transection
    def change_view(self, request, object_id, form_url='', extra_context=None):     
        obeject = Transection.objects.get(id = object_id) 
        if obeject.verified:
            messages.error(request, 'It is already verified!')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])       
        return super().change_view(request, object_id, form_url, extra_context=extra_context)    
admin.site.register(Transection, TransectionAdmin)



class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 0   
    can_delete = False
    
         
    def has_change_permission(self, request, obj=None):
        return False
    
    
    
    
 
class TransectionInline(admin.TabularInline):
    model = Transection
    extra = 0
    can_delete = False    
    fk_name = 'order'  
    
    
    def has_change_permission(self, request, obj=None):
        return False
    
    


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [ 'id', 'user', 'service', 'service_option', 'order_amount', 'paid_amount', 'payment_method']
    readonly_fields = [
        'user', 
        'service', 
        'service_option', 
        'order_amount', 
        'paid_amount', 
        'payment_method', 
        'tentative_delivery_date', 
        'full_payment_date', 
        'shipping_address', 
        'payment_address',
        'last_status',
        ]
    inlines= [OrderStatusInline, TransectionInline, ]
    
    
    def change_view(self, request, object_id, form_url='', extra_context=None):     
        obeject = Order.objects.get(id = object_id) 
        unveried_trans = Transection.objects.filter(order = obeject, verified = False)
        if unveried_trans.exists():
            messages.error(request, 'There is unverified transsection for this order')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        return super().change_view(request, object_id, form_url, extra_context=extra_context)    


admin.site.register(Order, OrderAdmin)
admin.site.register(PickedOrder)




    
class InvoiceRecordInline(admin.TabularInline):
    model = InvoiceRecord
    extra = 0
    can_delete = False
    readonly_fields = ['invoice', 'invoice_remarks', ]


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = [ 'id', 'order', 'order_status']
    readonly_fields = [
        'order', 
        'order_status', 
        'from_name', 
        'from_email', 
        'from_phone', 
        'from_location', 
        'service_title', 
        'service_description', 
        'service_image', 
        'service_option_title',
        'service_option_description',
        'tentative_delivery',
        'due_payment_by',
        'to_name',
        'to_email',
        'to_phone',
        'shipping_address',
        'payment_address',
        'payment_method_title',
        'payment_method_isntruction',
        'paid_amount',
        'order_amount',
        'order_require',
        'order_require_file',
        ]
    inlines= [InvoiceRecordInline]
    
admin.site.register(Invoice, InvoiceAdmin)

