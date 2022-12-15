from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import calendar
import datetime as dt

# Create your models here.
class BdService(models.Model):
    title = models.CharField(max_length=152)
    description = models.TextField()
    option_price_auto_calculate = models.BooleanField(default=False)
    bdt_rate = models.FloatField(default=settings.BDT_RATE, editable=False)  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("bds:service_detail", kwargs={"pk": self.pk})  
   
    
    @property
    def images(self):
        return self.serviceimages_set.all()[:5]
    
    
    @property
    def primary_image(self):
        last_image = self.serviceimages_set.all().order_by('-created_at').first()        
        return last_image.image.url
    
class ServiceImages(models.Model):
    service = models.ForeignKey(BdService, on_delete=models.CASCADE)
    image = models.FileField(upload_to='serice_image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    
    
    
class ServiceOptions(models.Model):
    service = models.ForeignKey(BdService, on_delete=models.CASCADE)
    title = models.CharField(max_length=152)
    apndix = models.FloatField('Perday Original Cost', default=0, help_text='Original Cost perday or buying price in default currency, curently USD')
    description = models.TextField(max_length=300, default='')
    value = models.DecimalField(decimal_places = 2, max_digits = 20, default=0)
    is_active = models.BooleanField(default=True)
    require_day_to_complete = models.IntegerField(help_text='Order need minimum days')
    partial_allowed = models.BooleanField(default=True)
    full_payment_before_day = models.IntegerField(help_text='If partial payment then full payment should be paid before mentioned days of delivery date')    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class RequiredOption(models.Model):
    service = models.ForeignKey(BdService, on_delete=models.CASCADE)
    title = models.CharField(max_length=152)
    required = models.BooleanField(default=True)
    maxlength = models.IntegerField(default=150)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    TYPES = [
        ("text", "Text Box"),
        ("textarea", "Text Area"),
        ("file", "File"),        
    ]
    type = models.CharField(default="", max_length=20, choices=TYPES)
    
class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='address', verbose_name='user', on_delete=models.CASCADE)   
    shipping_address = models.TextField(max_length=300)
    payment_address = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
class PaymentMethod(models.Model):
    title = models.CharField(max_length=252)
    instruction = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
    def __str__(self):
        return self.title
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orderuser', verbose_name='user', on_delete=models.CASCADE, default=1)   
    service = models.ForeignKey(BdService, on_delete=models.RESTRICT, related_name="orderservice")
    service_option = models.ForeignKey(ServiceOptions, on_delete=models.RESTRICT, related_name="orderoption")
    order_amount = models.FloatField("Order Amount", default=0)
    paid_amount = models.FloatField("Paid Amount",  default=0)
    shipping_address = models.TextField(null=True, blank=True)
    payment_address = models.TextField(null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, null=True, blank=True, related_name='orderpaymentmethod')
    tentative_delivery_date = models.DateTimeField(null=True, blank=True)
    full_payment_date = models.DateTimeField(null=True, blank=True)     
    last_status = models.CharField(max_length=152, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return 'Order#' + str(self.id) 
    
    @property
    def due(self):
        due = self.order_amount - self.paid_amount
        # status = self.orderstatus.all()
        # due = 0        
        # for s in status:
        #     due += s.due
        if self.paid_amount > self.order_amount:
            return 0.0
        return round(due, 2)
    
    @property
    def over_due_penalty(self): 
        
        if self.full_payment_date:
            due_date = self.full_payment_date
        else:
            due_date = self.tentative_delivery_date  
        
        over_due_day = ((timezone.now() +  timezone.timedelta(days = settings.OVERDUE_GRACE_DAY)) - due_date).days
        
        date=self.full_payment_date
        year=date.year
        days_of_year=366 if calendar.isleap(year) else 365     
        p = self.due
        r = settings.COMPUND_INTEREST_PERCENT
        n = days_of_year
        y = over_due_day / days_of_year
      
        
        compound_interest = (p * ((1 + ((r/100)/n)) ** (n*y)))-p
        # FV = p * ((1 + (r/100))**y)
        
        if over_due_day > 0:            
            return round(compound_interest, 2)
        return 0.0
    @property
    def total_due(self):
        return self.due + self.over_due_penalty
    
    
 
    
    
    
    @property
    def status_list(self):
        order_status = self.orderstatus.all()
        lists = [o.last_status for o in order_status]        
        return lists
    
    @property
    def is_progressing(self):
        if self.last_status in ['progressing']:
            return True
        return False
    
    @property
    def is_partial_progressing(self):
        if self.last_status in ['partial_progressing']:
            return True
        return False
    
    @property
    def is_complete(self):
        if self.last_status in ['complete']:
            return True
        return False
    
    @property
    def is_reject(self):
        if self.last_status in ['payment_reject']:
            return True
        return False
    
    @property
    def is_payment_processing(self):
        if self.last_status in ['processing']:
            return True
        return False
    
    @property
    def is_pending(self):
        if self.last_status in ['pending']:
            return True
        return False
    
    @property
    def has_pending_trans(self):
        trans = self.ordertransection.filter(verified = False)
        if trans.exists():
            return True
        return False
       
    @property
    def in_picked(self):
        data = self.picked_user_order.values('user').distinct().count()
        return data
    
    @property
    def is_picked(self):
        picked = self.picked_user_order.filter(approved = True)
        if picked.exists():
            return True
        return False
    
    @property
    def picked_users(self):
        picked = self.picked_user_order.filter(approved = True)
        users = set(p.user for p in picked)
        return users
        
        
        
        
        
    
   
   
    
class OrderRequire(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")    
    required_option = models.ForeignKey(RequiredOption, on_delete=models.CASCADE, related_name="orderitemserviceoption")    
    require_title = models.CharField(max_length=252)
    title_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
class OrderRequireFiles(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitemsfile")    
    required_option = models.ForeignKey(RequiredOption, on_delete=models.CASCADE, related_name="orderitemserviceoptionfile")    
    require_title = models.CharField(max_length=252)
    title_value = models.FileField(upload_to='require_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  

    
class OrderStatus(models.Model):
    STATUS = [
        ("paid", "Paid"), # if partial paid. can be updated from admin
        ("processing", "Processing"), # if order confirm. Can not updateable from admin
        # ("fullpaid", "Full Paid"), # if full paid. Can be updated from Admin
        ("pending", "Pending"), #untill order not confirm can not updated from admin     
        ("progressing", "Progressing"), # after payment confirmation. Autometically update after payment accept either partial or full     
        ("partial_progressing", "Partial Progressing"), # after payment confirmation. Autometically update after payment accept either partial or full          
        ("payment_reject", "Payment Reject"),   # if payment wrong. Can e updated from Admin
        ("complete", "Complete"),   # if order complete delivery. Can be updated from Admin
        ('over_due', 'Over Due'),          
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderstatus")   
    status = models.CharField(choices=STATUS, max_length=20, default=None, null=True, blank=True)    
    due = models.FloatField(editable=False, default=0)
    remarks = models.TextField()
    update_by = models.CharField(null=True, blank=True, max_length=252, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    

    
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="orderinvoice", )  
    order_status = models.CharField( max_length=252, null=True)
    from_name = models.CharField( max_length=250, null=True)
    from_email = models.EmailField( null=True)
    from_phone = models.CharField( max_length=250, null=True)
    from_location = models.TextField( null=True)

    service_title = models.CharField( max_length=252, null=True)
    service_description = models.TextField( null=True)
    service_image = models.TextField( null=True)

    
    service_option_title = models.CharField( max_length=252, null=True)
    service_option_description = models.TextField( null=True)
    
    tentative_delivery = models.DateTimeField(null=True, blank=True)
    due_payment_by = models.DateTimeField(null=True, blank=True)
    


    to_name = models.CharField( max_length=250, null=True)  
    to_email = models.EmailField( null=True)
    to_phone = models.CharField( max_length=250, null=True)
    shipping_address = models.TextField( null=True)
    payment_address = models.TextField( null=True)
    payment_method_title = models.CharField( max_length=252, null=True)
    payment_method_isntruction = models.TextField( null=True)
    paid_amount = models.FloatField(  null=True)
    order_amount= models.FloatField( null=True)
    order_require = models.JSONField( null=True)   
    order_require_file = models.JSONField( null=True)   
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
   
    @property
    def due(self):       
        return self.order.due
    
    @property
    def over_due_penalty(self):         
        return self.order.over_due_penalty
    
    @property
    def total_due(self):
        return self.order.total_due
    
    @property
    def has_pending_trans(self):        
        return self.order.has_pending_trans
        
    
class InvoiceRecord(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.RESTRICT, related_name='invoicerecord')
    due = models.FloatField(default=0)
    invoice_remarks = models.TextField( null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    

    
    
    

    
class Transection(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="ordertransection", editable=False)
    for_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transuser', verbose_name='user', on_delete=models.SET_NULL, null=True)   
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, related_name='methodstransection')
    identification = models.CharField(max_length=252)
    paying_amount = models.FloatField(default=0)
    paying_commited = models.BooleanField(default=False, editable=False)
    TYPES = [
        ("credit", "Credit"),
        ("debit", "Debit"),            
    ]
    
    type = models.CharField(max_length=20, choices=TYPES)
    value= models.FloatField(default=0, editable=False)
    remarks = models.CharField(max_length=250)
    verified = models.BooleanField(default=False)
    vefiried_by = models.CharField(null=True, blank=True, max_length=252, editable=False)    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        if self.order:
            data = self.order
        else:
            data = self.for_user
        return f'for order number {data}' 
    
    
class PickedOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='picked_order', verbose_name='user', on_delete=models.CASCADE)  
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='picked_user_order')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return 'Order#' + str(self.order.id) 

    
    
    
    
    
    
    
    
    
    
    

    
    