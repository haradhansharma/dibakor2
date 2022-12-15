from django.contrib import messages
from urllib.parse import urlparse
from django.http import Http404, HttpResponseRedirect

# from selfurl.decorators import coockie_exempts, coockie_required
from .models import *
from .forms import (
    UserCreationFormFront, 
    PasswordChangeForm, 
    UserForm, 
    ProfileForm,
    AvatarForm,
    ContractorSignUpForm,
    ContractorForm,
    UserPayoutForm,
    )
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from doc.doc_processor import site_info
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import CreateView
from accounts.decorators import contractor_required, screening_required, payout_verification_required
from bds.models import *


import logging
log =  logging.getLogger('log')



class ContractorSignUpView(CreateView):
    model = User
    form_class = ContractorSignUpForm
    template_name = 'registration/contractor_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'contractor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        subject = 'Account activation required!' 
        message = render_to_string('emails/account_activation_email.html', {
            'user': user,                    
            'domain': site_info().get('domain'),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),                
        })
        
        user.email_user(subject, message)            
        messages.success(self.request, 'Please Confirm your email to complete registration.') 
        return HttpResponseRedirect(reverse_lazy('login'))
        





# @coockie_exempts
@login_required
def profile_setting(request): 
    # try:
    #     if int(id) != request.user.id:
    #         messages.error(request, 'Request is not accessible')         
    #         return HttpResponseRedirect(reverse('bds:bds_list'))
    # except:
    #     raise PermissionDenied
        
    
    # title = username
    # description = 'You can manage your personal information here.'
    
    # seo_info = site_info() 
    # if not seo_info:
    #     messages.warning(request, 'Something wrong, Try again later')
    #     log.debug('No data in site setting')
    #     return HttpResponseRedirect(reverse('bds:bds_list'))   

    # modify = {
    #     'canonical' : request.build_absolute_uri(reverse('accounts:profile_setting', args=[str(username)])),
    #     'description': description,        
    #     'slogan': title, #it will work as a title as well.
             
    # }    
    # seo_info.update(modify)  
    
     
    if request.method == "POST" :
       
        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
                 
            if user_form.is_valid():                
                user_form.save()
                messages.success(request,('Your profile was successfully updated!'))                
            else:
                messages.error(request, 'Invalid form submission.')                
                messages.error(request, user_form.errors)    
                
        if 'profile_form' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user.profile)   		    
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,('Your profile data was successfully updated!'))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, profile_form.errors)  
    
           
        if 'avatar_form' in request.POST:
            
            avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)   		    
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request,('Your Avatar Saved!'))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, avatar_form.errors)     
                
        if 'contractor_form' in request.POST:            
            contractor_form = ContractorForm(request.POST, instance=request.user.contractor)   		    
            if contractor_form.is_valid():
                contractor_form.save()
                messages.success(request,('Your Skills Saved!'))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, contractor_form.errors)   
                
        if 'user_payout_form' in request.POST:            
            user_payout_form = UserPayoutForm(request.POST, instance=request.user.userpayout)   		    
            if user_payout_form.is_valid():
                user_payout_form.save()
                messages.success(request,('Your Payout Saved Saved!'))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, contractor_form.errors)            
                
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)     
    avatar_form = AvatarForm(instance=request.user.profile)
    
    if hasattr(request.user, 'contractor'):
        contractor_form = ContractorForm(initial={'skills_in' : request.user.contractor.skills_in.all() })    
    else:
        contractor_form = None    
        
        
    if hasattr(request.user, 'userpayout'):        
        pass
    else:
        UserPayout.objects.create(user=request.user)          
    user_payout_form = UserPayoutForm(
        initial={
            'payout_method' : request.user.userpayout.payout_method,
            'payout_account' : request.user.userpayout.payout_account,
            
                 })
  
        
    
    
    context = {
        "user":request.user,
        "user_form":user_form,
        "profile_form":profile_form,   
        'avatar_form' : avatar_form,
        'contractor_form' : contractor_form,
        'user_payout_form' : user_payout_form
        # 'site' : seo_info ,               
    }
    
    
    
    
    return render(request, 'registration/profile_settings.html', context = context)

@login_required
def delete_avatar(request):    
    user = request.user
    profile = Profile.objects.get(user = user)
    profile.avatar.delete()
    profile.avatar = ''
    profile.save()
    avatar_form = AvatarForm(instance=request.user.profile)    
   
    return render(request, 'registration/avatar_swap.html', {'avatar_form':avatar_form})
    
# @coockie_exempts
@login_required
def password_change(request): 
    
    
    # from doc.models import MetaText, Acordion
    
    # meta_data = MetaText.objects.get(path='accounts:change_pass')   
    # title = meta_data.title
    # description = meta_data.description    
    
    # seo_info = site_info() 
    # modify = {
    #     'canonical' : request.build_absolute_uri(reverse('accounts:change_pass')),
    #     'description': description,        
    #     'slogan': title,              
    # }    
    # seo_info.update(modify)   
    
    if request.method == "POST":        
        password_form = PasswordChangeForm(user=request.user, data=request.POST)        
        if password_form.is_valid():            
            password_form.save()            
            update_session_auth_hash(request, password_form.user)            
            messages.success(request,('Your password was successfully updated!')) 
        else:
            messages.error(request, 'Invalid form submission.')            
            messages.error(request, password_form.errors)         
        return HttpResponseRedirect(reverse('accounts:change_pass'))    
    password_form = PasswordChangeForm(request.user)  
    
    context = {
        "user":request.user,        
        "password_form":password_form,
        # 'meta_data' : meta_data ,
        # 'site' : seo_info ,
    }
    return render(request, 'registration/change_pass.html', context = context)

# @method_decorator(coockie_exempts, name='dispatch')
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    
   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        # from doc.models import MetaText, Acordion
    
        # meta_data = MetaText.objects.get(path='accounts:password_reset_complete')   
        # title = meta_data.title
        # description = meta_data.description    
        
        # seo_info = site_info() 
        # modify = {
        #     'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset_complete')),
        #     'description': description,        
        #     'slogan': title + f" to {seo_info.get('domain')}"            
        # }    
        # seo_info.update(modify)   
        
        # context['meta_data'] = meta_data
        # context['site'] = seo_info
        
        return context
    
# @method_decorator(coockie_exempts, name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    from .forms import PasswordResetForm
    
    #overwriting form class to take control over default django
    form_class = PasswordResetForm
   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        # from doc.models import MetaText, Acordion
    
        # meta_data = MetaText.objects.get(path='accounts:password_reset')   
        # title = meta_data.title
        # description = meta_data.description    
        
        # seo_info = site_info() 
        # modify = {
        #     'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset')),
        #     'description': description,        
        #     'slogan': title + f" to {seo_info.get('domain')}"            
        # }    
        # seo_info.update(modify)   
        
        # context['meta_data'] = meta_data
        # context['site'] = seo_info
        
        return context
    
# @method_decorator(coockie_exempts, name='dispatch')    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books       
        
        # from doc.models import MetaText, Acordion
    
        # meta_data = MetaText.objects.get(path='accounts:password_reset_done')   
        # title = meta_data.title
        # description = meta_data.description    
        
        # seo_info = site_info() 
        # modify = {
        #     'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset_done')),
        #     'description': description,        
        #     'slogan': title + f" to {seo_info.get('domain')}"            
        # }    
        # seo_info.update(modify)   
        
        # context['meta_data'] = meta_data
        # context['site'] = seo_info
        
        return context
    
# @method_decorator(coockie_exempts, name='dispatch')   
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    from .forms import SetPasswordForm
    
    #overwriting form class to take control over default django
    form_class = SetPasswordForm
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books  
        
        # from doc.models import MetaText, Acordion
    
        # # meta_data = MetaText.objects.get(path='accounts:password_reset_confirm')   
        # title = 'Confirm your new password'
        # description = 'Please select a strong password and remember it for further use!  '
        
        # seo_info = site_info() 
        # modify = {
        #     'canonical' : self.request.build_absolute_uri(self.request.META['PATH_INFO']),
        #     'description': description,        
        #     'slogan': title + f" to {seo_info.get('domain')}"            
        # }    
        # seo_info.update(modify)   
        
        # # context['meta_data'] = meta_data
        # context['site'] = seo_info
        
        return context

    

# @method_decorator(coockie_exempts, name='dispatch')
class CustomLoginView(LoginView):
    #To avoid circular reference it is need to import here
    from .forms import LoginForm
    
    #overwriting form class to take control over default django
    form_class = LoginForm 
    
    
    #overwriting to set custom after login path
    # next_page = ''
    
    def get_default_redirect_url(self):        
        return reverse('accounts:profile_setting')     
    #taking control over default of Django  
    def form_valid(self, form): 
        
        #set after login url 
        # self.next_page = reverse('accounts:profile_setting', kwargs={'id': self.request.user.pk})           
        
        #rememberme section        
        # remember_me = form.cleaned_data.get('remember_me')  
        # # as during signup user need to accept our policy so we can set term accepted 
        # self.request.session['term_accepted'] = True   
        
        # if not remember_me:
        #     # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
        #     self.request.session.set_expiry(0)
        #     # Set session as modified to force data updates/cookie to be saved.
        #     self.request.session.modified = True  
        # self.request.session.set_test_cookie()
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
    
    def get_context_data(self,  **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        # from doc.models import MetaText, Acordion
    
        # meta_data = MetaText.objects.get(path='accounts:login')   
        # title = meta_data.title
        # description = meta_data.description    
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(reverse('accounts:login')),
            # 'description': description,        
            # 'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        # context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context



# @coockie_required
def signup(request):    
    
    
    

    
    # seo_info = site_info() 
    # modify = {
    #     'canonical' : request.build_absolute_uri(reverse('accounts:signup')),
    #     'description': description + f" at {seo_info.get('domain')}"  ,       
    #     'slogan': title + f" to {seo_info.get('domain')}"            
    # }    
    # seo_info.update(modify)  
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile_setting'))
    
    
           
    if request.method == 'POST':
        current_site = get_current_site(request)
        form = UserCreationFormFront(request.POST)
        if form.is_valid():     
            new_user = form.save(commit=False)    
            new_user.is_active = False       
            new_user.save()
            subject = 'Account activation required!' 
            message = render_to_string('emails/account_activation_email.html', {
                'user': new_user,                    
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),                
            })
            
            new_user.email_user(subject, message)            
            messages.success(request, 'Please Confirm your email to complete registration.') 
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else: 
        form = UserCreationFormFront()
    context = {
        'form': form,
        # 'meta_data' : meta_data ,
        # 'site' : seo_info ,      
        
    }
    return render(request, 'registration/register.html', context = context) 


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        messages.warning(request, ('Activation link is invalid!'))
        return HttpResponseRedirect(reverse_lazy('bds:bds_list'))
    
@method_decorator(login_required, name='dispatch') 
class MyOrders(View):
    template_name = 'registration/user_orders.html'  
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # active_orders = user.orderuser.filter(last_status__in = )
        # complete_orders = user.orderuser.filter(last_status = 'complete')
        # payment_pending_orders = user.orderuser.filter(last_status = 'partialpaid')
        
        user_orders = user.orderuser.all()
        
        progressing_orders = [order for order in user_orders if order.is_progressing and order.total_due <= 0]
        partial_progressing_orders = [order for order in user_orders if order.is_partial_progressing and order.total_due >= 0]
        complete_orders = [order for order in user_orders if order.is_complete and order.total_due <= 0]
        reject_orders = [order for order in user_orders if order.is_reject]
        processing_orders = [order for order in user_orders if order.is_payment_processing and order.due >= order.order_amount] 
        pending_orders = [order for order in user_orders if order.is_pending and order.due >= order.order_amount] 
        
        context = {
            'progressing_orders' : progressing_orders,
            'partial_progressing_orders' : partial_progressing_orders,
            'complete_orders' : complete_orders,
            'reject_orders' : reject_orders,
            'processing_orders' : processing_orders,
            'all_orders' : user_orders,
            'pending_orders' : pending_orders           
        }
        return render(request, self.template_name, context = context)
    def post(self, request, *args, **kwargs):
        pass
    
@method_decorator(login_required, name='dispatch')     
@method_decorator(contractor_required, name='dispatch')    
class ContractorDashboard(View):
    
    template_name = 'registration/contractor_dashboard.html'  
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_skills = user.contractor.skills_in.all()
        picked_order_ids = [o.order.id for o in request.user.picked_order.filter(approved = True)] 
        progressing_orders = Order.objects.filter(last_status__in = ['progressing', 'partial_progressing'], service__in = user_skills).exclude(id__in = picked_order_ids)
        picked_orders = set(o.order for o in request.user.picked_order.filter(approved = True))
        waiting_to_pick = set(o.order for o in request.user.picked_order.filter(approved = False) if o.order not in picked_orders )
        
        context = {
            'progressing_orders' : progressing_orders,
            'picked_orders' : list(picked_orders),
            'picked_order_ids' : picked_order_ids,
            'waiting_to_pick' : list(waiting_to_pick)
        }
        return render(request, self.template_name, context = context)
    def post(self, request, *args, **kwargs):
        pass

@method_decorator(login_required, name='dispatch')     
@method_decorator(contractor_required, name='dispatch')      
class PickOrder(View):
    
    template_name = 'registration/pick_order.html'  
    
    def get(self, request, *args, **kwargs):
        refrer = request.META.get('HTTP_REFERER')
        user_id= kwargs.get('user_id')
        order_id = kwargs.get('order_id')
        if int(user_id) != int(request.user.id):
            messages.error(request, f"It is not a good way you are trying to do!")
            return HttpResponseRedirect(refrer)  
        order = Order.objects.get(id = order_id)
        picked_order = [o.order.id for o in request.user.picked_order.all()] 
        context = {
            'order' : order,
            'picked_order' : picked_order
        }
        return render(request, self.template_name, context = context)
    def post(self, request, *args, **kwargs):
        refrer = request.META.get('HTTP_REFERER')
        user_id= kwargs.get('user_id')
        order_id = kwargs.get('order_id')
        if int(user_id) != int(request.user.id):
            messages.error(request, f"It is not a good way you are trying to do!")
            return HttpResponseRedirect(refrer)  
        request_order_id = request.POST.get('order_id')
        
        if int(order_id) != int(request_order_id):
            messages.error(request, f"It is not a good way you are trying to do!")
            return HttpResponseRedirect(refrer)  
        picked_order = [o.order.id for o in request.user.picked_order.all()] 
       
        order= Order.objects.get(id = request_order_id)
        if order.is_picked:
            messages.error(request, f"This order picked by other!")
            return HttpResponseRedirect(refrer)  
            
        
        if int(request_order_id) in picked_order:            
            messages.error(request, f"Order already picked by you!")
            return HttpResponseRedirect(refrer)  
            
        PickedOrder.objects.create(
            user = request.user,
            order= order
        )
        
        return HttpResponseRedirect(reverse('accounts:pick_order', kwargs={'order_id' : order_id, 'user_id':user_id }))
    
    
@method_decorator(login_required, name='dispatch')     
@method_decorator(contractor_required, name='dispatch')      
class SubmitPicked(View):
    
    template_name = 'registration/submit_picked.html'  
    def get(self, request, *args, **kwargs):
        # refrer = request.META.get('HTTP_REFERER')
        # user_id= kwargs.get('user_id')
        # order_id = kwargs.get('order_id')
        # if int(user_id) != int(request.user.id):
        #     messages.error(request, f"It is not a good way you are trying to do!")
        #     return HttpResponseRedirect(refrer)  
        # order = Order.objects.get(id = order_id)
        # picked_order = [o.order.id for o in request.user.picked_order.all()] 
        context = {
            'order' : order,
            'picked_order' : picked_order
        }
        return render(request, self.template_name, context = context)
    def post(self, request, *args, **kwargs):
        # refrer = request.META.get('HTTP_REFERER')
        # user_id= kwargs.get('user_id')
        # order_id = kwargs.get('order_id')
        # if int(user_id) != int(request.user.id):
        #     messages.error(request, f"It is not a good way you are trying to do!")
        #     return HttpResponseRedirect(refrer)  
        # request_order_id = request.POST.get('order_id')
        
        # if int(order_id) != int(request_order_id):
        #     messages.error(request, f"It is not a good way you are trying to do!")
        #     return HttpResponseRedirect(refrer)  
        # picked_order = [o.order.id for o in request.user.picked_order.all()] 
       
        # order= Order.objects.get(id = request_order_id)
        # if order.is_picked:
        #     messages.error(request, f"This order picked by other!")
        #     return HttpResponseRedirect(refrer)  
            
        
        # if int(request_order_id) in picked_order:            
        #     messages.error(request, f"Order already picked by you!")
        #     return HttpResponseRedirect(refrer)  
            
        # PickedOrder.objects.create(
        #     user = request.user,
        #     order= order
        # )
        
        return HttpResponseRedirect(reverse('accounts:submit_picked', kwargs={'order_id' : order_id, 'user_id':user_id }))
    
    
        
    




    
    
    
    
    
    
    

