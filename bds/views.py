from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from django.views import View
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doc.doc_processor import site_info
from mimetypes import guess_type
import pdfkit
from django.test import override_settings
from django.template.loader import get_template
import platform
from django.contrib.auth.decorators import login_required  
from accounts.forms import OrderInLineSignUpForm, OtpForm
from accounts.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone

def payment_instruction(request, *args, **kwargs):
   
    id = request.GET.get('pm')    
    method = PaymentMethod.objects.get(id = int(id))
    return render(request, 'bds/payment_instruction.html', {'instruction' : method.instruction}) 

# Create your views here.
class ServiceList(ListView):
    model = BdService
    paginate_by = 100  # if pagination is desired    
   

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    

    
 
# @method_decorator(login_required, name='dispatch') 
class ServiceDetailView(DetailView):

    model = BdService

    def get_context_data(self, **kwargs):        
        
        context = super().get_context_data(**kwargs) 
       
        service = context['bdservice']
        context['options'] = [[op.id, float(op.value)] for op in service.serviceoptions_set.all()]
        if not self.request.user.is_authenticated:
            context['inline_form'] = OrderInLineSignUpForm()
        
        return context
    
    
    def post(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            inline_form = OrderInLineSignUpForm(request.POST)
            if inline_form.is_valid():
                user = inline_form.save()            
                subject = 'Please use this OTP on order confirmation form!'  
                message = f'Dear {user.email}, \n \n \n This is your OTP {user.otp}. \n Thanks \n SIteName'             
                user.email_user(subject, message)   
                request.session['ordering_email'] = user.email
                request.session['ordering_mobile'] = user.mobile        
                        
            else:
                messages.error(request, f"Something wrong, try again!")
                return HttpResponseRedirect(request.build_absolute_uri(request.path)) 
        else:
            user = request.user
            request.session['ordering_email'] = user.email
            request.session['ordering_mobile'] = user.mobile   
            
        
       
        
        service_id = kwargs.get('pk')
        service = BdService.objects.get(id = service_id)    
        
        
        option_id = request.POST.get('option_id')  
        if option_id == '':
            messages.error(request, f"Selection of any one of listed service mandatory!")
            return HttpResponseRedirect(request.build_absolute_uri(request.path))  
        
        service_option = ServiceOptions.objects.get(id = int(option_id))   
        tentative_delivery_date = timezone.now() + timezone.timedelta(days=int(service_option.require_day_to_complete))
        
        if service_option.partial_allowed:
            full_payment_date = tentative_delivery_date - timezone.timedelta(days=int(service_option.full_payment_before_day))
        else:
            full_payment_date = None
        
        
        order = Order.objects.create(
            user = user, 
            service = service, 
            service_option = service_option, 
            order_amount = service_option.value, 
            tentative_delivery_date=tentative_delivery_date, 
            full_payment_date=full_payment_date,
            
            )
        
 
        
        
        for k, v in request.POST.items():          
            if k.startswith(str(service_id)):    
                                                   
                require_title = k.split('-')[1]                                
                required_option_id = int(k.split('-')[2])
                   
                
                if service_id == '' or required_option_id == '':
                    messages.error(request, 'You are trying to do something danger. Do not do that!')                    
                    return HttpResponseRedirect(request.build_absolute_uri(request.path))
                
                required_option = RequiredOption.objects.get(id = required_option_id)   
                
                title_value = v  
                
                
                if required_option.required:
                    if title_value == '':  
                        messages.error(request, f"Value is essential in {required_option}")
                        return HttpResponseRedirect(request.build_absolute_uri(request.path)) 
                             
                if len(list(title_value)) > required_option.maxlength:                    
                    messages.error(request, f"Value more then limit in the {required_option}")
                    return HttpResponseRedirect(request.build_absolute_uri(request.path))    
                if required_option.type != 'file':            
                    OrderRequire.objects.create(order = order, required_option = required_option, require_title = require_title, title_value = title_value)
                
        for key, value in request.FILES.items():
            if key.startswith(str(service_id)):                                                   
                require_file_title = key.split('-')[1]                                
                required_file_option_id = int(key.split('-')[2])
                
                if service_id == '' or required_option_id == '':
                    messages.error(request, 'You are trying to do something danger. Do not do that!')
                    return HttpResponseRedirect(request.build_absolute_uri(request.path))
                required_option = RequiredOption.objects.get(id = required_file_option_id)               
                title_value = value  
                
                if required_option.required:
                    if title_value == '':  
                        messages.error(request, f"Value is essential in {required_option}")                                                
                        return HttpResponseRedirect(request.build_absolute_uri(request.path)) 
                    
                    
                allowed_image_type = ['image/jpeg', 'image/png']
                entry_type = guess_type(title_value.name)[0]
                if entry_type not in allowed_image_type:
                    messages.error(request, f"Only {allowed_image_type} are allowed" )                                              
                    return HttpResponseRedirect(request.build_absolute_uri(request.path)) 
                    
                if required_option.type == 'file':  
                    OrderRequireFiles.objects.create(order = order, required_option = required_option, require_title = require_file_title, title_value = title_value)
                
        order.last_status = 'pending'
        order.save()
        
        OrderStatus.objects.create(
            order = order, 
            status = 'pending', 
            due = service_option.value, 
            update_by = 'System During Making Order' 
            ) #marking order value as due ass payment is not confrmed yet
                
        
        return HttpResponseRedirect(reverse('bds:order_confirm', kwargs={'order_id' : order.id }))
    
    
def delete_extra_file(request, id, order_id):
    
    try:
        ordering_email = request.session['ordering_email']
        ordering_mobile = request.session['ordering_mobile']
    except:        
        return HttpResponse("It is not a good way you are trying to do! Can not delete the file!")  
    
    
    order = Order.objects.get(id = order_id)    
    ordering_user = User.objects.get(email = ordering_email)
    
    if order.user != ordering_user:
        return HttpResponse("File Can not delete! You are trying to do do illegal something!")  
        
    #if order confirm file can not be deleted
    if order.paid_amount <= 0:
        require_file = OrderRequireFiles.objects.get(id = int(id))
        require_file.title_value.delete()
        require_file.title_value = ''
        require_file.save()   
   
    return render(request, 'bds/swap.html', {'order':order})
    
    # return redirect(reverse('bds:order_confirm', kwargs={'order_id' : order_id }))
    
 
def get_should_paid(order):
    if order.service_option.partial_allowed:
        should_paid = ( settings.SHOULD_PAID_PERCENT * order.order_amount ) / 100
    else:
        should_paid = order.order_amount
        
    return int(should_paid)
    
# @method_decorator(login_required, name='dispatch')       
class OrderConfirm(View):
    confirm_dataForm = ConfirmDataForm   
    template_name = 'bds/order-confirm.html'  
   
    
    def get(self, request, *args, **kwargs):
        refrer = request.META.get('HTTP_REFERER')
        
        if request.user.is_authenticated:            
            request.session['ordering_email'] = request.user.email
            request.session['ordering_mobile'] = request.user.mobile
        
        try:               
            ordering_email = request.session['ordering_email']
            ordering_mobile = request.session['ordering_mobile']
        except:
            messages.error(request, f"It is not a good way you are trying to do!")
            return HttpResponseRedirect(refrer)  
            
            
        # user = request.user
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id = order_id)
        user = order.user
        
        if order.is_payment_processing:
            messages.info(request, f"Order already confirmed!")
            return HttpResponseRedirect(reverse('bds:invoice', kwargs={'invoice_id': order.orderinvoice.id}))     
        
        if order.is_partial_progressing:
            messages.info(request, f"You can pay partial due payment!")
            return HttpResponseRedirect(reverse('bds:due_payment', kwargs={'id':request.user.id,'order_id': order.id}))  
            
        
        orderring_user = User.objects.get(email = ordering_email)
        
        if user != orderring_user:
            messages.error(request, f"It is not your order!")
            return HttpResponseRedirect(refrer)          
        try:
            address = Address.objects.get(user = user) 
            form = AddressForm(instance=address)  
        except:
            form = AddressForm(initial={'user':user})  
        
        payment_methods = PaymentMethod.objects.filter(is_active = True)
        
        context = {
            'order' : order,
            'should_paid' : get_should_paid(order),
            'form' : form,
            'payment_methods' : payment_methods,
            'confirm_dataForm' : self.confirm_dataForm(),
            
        }
        if not request.user.is_authenticated:
            otp_form = OtpForm
            context['otp_form'] = otp_form
            

        return render(request, self.template_name, context = context)
    
    
    def post(self, request, *args, **kwargs):
        
        refrer = request.META.get('HTTP_REFERER')
        try:
            ordering_email = request.session['ordering_email']
            ordering_mobile = request.session['ordering_mobile']
        except:
            messages.error(request, f"It is not a good way you are trying to do!")
            return HttpResponseRedirect(refrer)     
        
        
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id = order_id)
        user = order.user        
        site = site_info()
        
        orderring_user = User.objects.get(email = ordering_email)
        
        if user != orderring_user:
            messages.error(request, f"It is not your order!")
            return HttpResponseRedirect(refrer)   
        
        otp_form = OtpForm(request.POST)
        if otp_form.is_valid():
            form_otp = otp_form.cleaned_data['otp']
            user_otp = orderring_user.otp
            if form_otp == user_otp:
                orderring_user.is_active = True
                orderring_user.save()
                login(request, orderring_user)
            else:
                messages.error(request, f"OTP not matched!")
                return HttpResponseRedirect(refrer)  
                
            
        
        
        post = request.POST
        files = request.FILES
        
     
        
        shipping_address = post.get('shipping_address')
        payment_address = post.get('payment_address')
        payment_method_id = post.get('pm')
        payment_method = PaymentMethod.objects.get(id = payment_method_id)
        
        paying_amount = int(post.get('value'))        
        # order_amount = order.order_amount
        
        should_paid = get_should_paid(order)
        
        
            
        
        identification = post.get('indetity')
        # value = post.get('value')
        remarks = post.get('remarks')
        
        if paying_amount < should_paid:
            messages.error(request, f"Amount cannot be less then {should_paid}")
            return HttpResponseRedirect(request.build_absolute_uri(request.path))         

                
        
        order.shipping_address = shipping_address
        order.payment_address = payment_address
        
        try:
            address = Address.objects.get(user = orderring_user)
            address.shipping_address = shipping_address
            address.payment_address = payment_address
            address.save()
        except:
            Address.objects.create(user = orderring_user, shipping_address= shipping_address, payment_address = payment_address)
            
            
        order.payment_method = payment_method
        paying_amount = paying_amount
        OrderStatus.objects.create(
            order = order, 
            status = 'processing', 
            update_by = 'System During Making Order' 
            ) # due will be updated during confirmation from admin nd it is 0 set
        
        order.last_status = 'processing'
        
        Transection.objects.create(
            order = order, 
            for_user = order.user,
            payment_method = payment_method, 
            identification = identification, 
            paying_amount = paying_amount,
            paying_commited = False,
            verified = False,
            type = 'credit',
            value = 0 , #paid amount will be updated after confirming from backend by admin
            remarks = remarks
            ) 
        
        # order.paid_amount += int(paid_amount)
        order_require = {}
        for k, v in post.items():
            if k.startswith('require'):
                require_id = k.split('-')[1]
                require = OrderRequire.objects.get(id = int(require_id))
                require.title_value = v
                require.save()
                dict_requires = {
                    require.require_title : v
                }
                order_require.update(dict_requires)
                
        order_require_file = {}
        if files:
            for key, value in files.items():                
                if key.startswith('require'):
                    require_id = key.split('-')[1]
                    require = OrderRequireFiles.objects.get(id = int(require_id))
                    allowed_image_type = ['image/jpeg', 'image/png']
                    entry_type = guess_type(value.name)[0]
                    
                    if entry_type in allowed_image_type:
                        require.title_value = value
                        require.save()                
                        dict_requires = {
                            require.require_title : require.title_value.url
                        }
                        order_require_file.update(dict_requires)
                    else:
                        messages.error(request, f"Only {allowed_image_type} are allowed" )                                              
                        return HttpResponseRedirect(request.build_absolute_uri(request.path)) 
        else:
            require = OrderRequireFiles.objects.filter(order = order)
            for r in require:
                dict_requires = {
                    r.require_title : r.title_value.url
                }
                order_require_file.update(dict_requires)
                
                    
        order.save()   
        
        if order.service_option.apndix != 0:
            service_option_title = str(order.service_option.title) + str(order.service_option.apndix)
        else:
            service_option_title = str(order.service_option.title)
            
            
        
        
        invoice = Invoice.objects.create(
            from_name= site.get('name'),
            from_email = site.get('email'),
            from_phone = site.get('phone'),
            from_location = site.get('location'),
            
            order_id = order.id, 
            order_status = order.last_status,
            
            service_title = order.service.title, 
            service_description = order.service.description, 
            service_image = order.service.primary_image,
            
            service_option_title = service_option_title,
            service_option_description = order.service_option.description,
            
            tentative_delivery = order.tentative_delivery_date,
            due_payment_by = order.full_payment_date,
            
            
            
            to_name = orderring_user.get_full_name(),
            to_email = orderring_user.email,
            to_phone = orderring_user.mobile,           
            shipping_address=shipping_address, 
            payment_address=payment_address, 
            
            payment_method_title=payment_method.title,
            payment_method_isntruction=payment_method.instruction,
            paid_amount=0, #will be updatedd during payment confirmation from backend
            order_amount=order.order_amount,
            
            order_require=order_require,    
            order_require_file=order_require_file,   
            ) 
        InvoiceRecord.objects.create(
            invoice = invoice, 
            due = order.order_amount, 
            invoice_remarks = f'Firt Invoice genareted on {timezone.now()}'
            )#due as payment is not confirm
        
        del request.session['ordering_email']
        del request.session['ordering_mobile']
        
    
        
        return HttpResponseRedirect(reverse('bds:invoice', kwargs={'invoice_id': invoice.id }))
    
@login_required    
def invoice(request, invoice_id):
    invoice = Invoice.objects.get(id = int(invoice_id))
    if invoice.order.user != request.user:
        messages.error(request, f"You are not allowed to access this invoice!")
        return HttpResponseRedirect(reverse('bds:bds_list')) 
    
    context = {
        'invoice' : invoice
    }
    return render(request, 'bds/invoice.html', context = context)
   
def should_paid(request, *args, **kwargs):
  
    get = request.GET   
    
    paying_amount = int(get.get('value'))  
    order_id = int(get.get('order_id'))  
      
    order = Order.objects.get(id = order_id)   
    

    
    
    
    should_paid = get_should_paid(order)
    
    if int(paying_amount) < int(should_paid):
        return HttpResponse(f"<span class = 'text-danger'>Amount can not be less then {should_paid}</span>")    
    return HttpResponse("<span class = 'text-success'>Valid amount</span>")


def render_html(request, invoice_id):
    
    invoice = Invoice.objects.get(id = int(invoice_id))
    if invoice.order.user != request.user:
        messages.error(request, f"You are not allowed to access this invoice!")
        return HttpResponseRedirect(reverse('bds:bds_list')) 
    
    context = {
        'invoice' : invoice
    }  
    #active below for windows development server
    static_url = '%s://%s%s' % (request.scheme,
                                request.get_host(), settings.STATIC_URL)
    # media_url = '%s://%s%s' % (request.scheme,
    #                            request.get_host(), settings.MEDIA_URL)
    # media_link = '%s://%s%s%s' % (request.scheme,
    #                            request.get_host(), settings.STATIC_URL, settings.MEDIA_URL)
    # print(media_link)
    title = '{}_{}_invoice.pdf'.format(str(invoice_id), str(invoice.order.id)) 
    
    context = {
        'invoice' : invoice,
        'title' : title
    }
    
    
    #active below for windows development server
    with override_settings(STATIC_URL=static_url):
        template = get_template('bds/invoicepdf.html')
        context = context
        html = template.render(context)
        return html
    
@login_required     
def invoicepdf(request, invoice_id):
    site = site_info()
    site_email = site.get('email')
    
    invoice = Invoice.objects.get(id = int(invoice_id))
    if invoice.order.user != request.user:
        messages.error(request, f"You are not allowed to access this invoice!")
        return HttpResponseRedirect(reverse('bds:bds_list')) 
    
    
    
    content = render_html(request, invoice_id)
    
    if 'html' in request.GET:
        # Output HTML        
        return HttpResponse(content)
    else: 
        if platform.system() == 'Windows':
            wkhtmltopdf_bin = 'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        elif platform.system() == 'Linux':
            wkhtmltopdf_bin = '/usr/local/bin/wkhtmltopdf'
        else:
            messages.warning(request,f'OS Unknow! Please drop a mail to {site_email}')    
            return  HttpResponseRedirect(reverse('bds:bds_list'))
            
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_bin)
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'margin-top': '0.15in',
            'margin-right': '0.15in',
            'margin-bottom': '0.15in',
            'margin-left': '0.15in',            
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 1,
        }        
        pdf = pdfkit.from_string(input=content, output_path=False,
                                options=options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        if 'download' in request.GET and 'inline' not in request.GET:
                response['Content-Disposition'] = 'attachment; filename=%s' % '{}_{}_invoice.pdf'.format(str(invoice_id), str(invoice.order.id))              
        
        return response
    
# @login_required        
# def due_payment(request, id, order_id):
#     context = {
#         'sss' : 'sasd'
#     }
#     return render(request, 'bds/partial_payment.html', context = context)

def should_partial_paid(request, *args, **kwargs):
  
    get = request.GET   
    
    paying_amount = int(get.get('value'))  
    order_id = int(get.get('order_id'))  
      
    order = Order.objects.get(id = order_id)   
    

    
    
    
    should_paid = order.total_due
    
    if int(paying_amount) < int(should_paid):
        return HttpResponse(f"<span class = 'text-danger'>Amount can not be less then {should_paid}</span>")    
    return HttpResponse("<span class = 'text-success'>Valid amount</span>")


@method_decorator(login_required, name='dispatch')       
class DuePayment(View):
    confirm_dataForm = PartialPaidForm 
    template_name = 'bds/partial_payment.html'  
    
    def __allowed(self, user_id, request, order):
        
        order_owner = order.user        
        logged_user = request.user
        
        if int(user_id) != logged_user.id:
            messages.error(request, f"Do not do that what you are trying to do!")
            return False            
        
        if logged_user != order_owner:
            messages.error(request, f"It is not your order!")
            return False  
        
        return True
        
    
    def get(self, request, *args, **kwargs):
        
        
        refrer = request.META.get('HTTP_REFERER')           
            
        # user = request.user
        order_id = kwargs.get('order_id')
        user_id = kwargs.get('id')
        
        order = Order.objects.get(id = order_id)
         
        
        if not self.__allowed(user_id, request, order):
            return HttpResponseRedirect(refrer)     
              
        
        payment_methods = PaymentMethod.objects.filter(is_active = True)
        
  
        
        context = {
            'order' : order,
            
            'payment_methods' : payment_methods,
            'confirm_dataForm' : self.confirm_dataForm(),
            
        }
        
        return render(request, self.template_name, context = context)
    def post(self, request, *args, **kwargs):       
        
        refrer = request.META.get('HTTP_REFERER')           
            
        # user = request.user
        order_id    = kwargs.get('order_id')
        user_id     = kwargs.get('id')        
        order       = Order.objects.get(id = order_id)
         
        
        if not self.__allowed(user_id, request, order):
            return HttpResponseRedirect(refrer)  
        
        post_order_id = request.POST.get('order_id')         
        if int(post_order_id) != int(order_id):
            messages.error(request, f"Do not do that what you are trying to do!")
            return HttpResponseRedirect(refrer)  
            
        
        payment_method_id  = request.POST.get('pm')   
        payment_method = PaymentMethod.objects.get(id = payment_method_id)
             
        
        form = self.confirm_dataForm(request.POST)
        if form.is_valid():
            indetity    = form.cleaned_data['indetity']
            paying_amount       = form.cleaned_data['value']       
            remarks     = form.cleaned_data['remarks']
            
            
            Transection.objects.create(
            order = order, 
            for_user= order.user,
            payment_method = payment_method, 
            identification = indetity, 
            paying_amount = paying_amount,
            paying_commited = False,
            verified = False,
            type = 'credit',            
            remarks = remarks
            ) 
            
            
            
            
            
        
        return HttpResponseRedirect(reverse('bds:invoice', kwargs={'invoice_id': order.orderinvoice.id }))
      