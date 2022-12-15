from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from doc.doc_processor import site_info
# from selfurl.models import Shortener
from .models import *
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox

from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from . utils import generate_otp
from django.db import transaction

class ContractorSignUpForm(UserCreationForm):
    skills_in = forms.ModelMultipleChoiceField( 
        queryset=BdService.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True, 
        
    )
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={"class": "form-control" }))
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)   
    class Meta:
        model = User
        fields = ( 'email', 'mobile',  'password1', 'password2', )
        
        widgets = {                      
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class':'form-control', 'aria-label':'email' }),    
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile', 'class':'form-control', 'aria-label':'Mobile' }), 
        }
    
        

        
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_contractor = True
        user.save()
        contractor = Contractor.objects.create(user=user)
        UserPayout.objects.create(user=user)        
        contractor.skills_in.add(*self.cleaned_data.get('skills_in'))
        return user
    
    def clean(self, *args, **kwargs):
        mobile = self.cleaned_data.get('mobile')        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        
        if not mobile:
            raise forms.ValidationError(f'Mobile Number is essential!')
            
        
        if email and password:
            email_qs = User.objects.filter(email=email)
            if not email_qs.exists():
                pass    
            else:               
                is_active_qs = User.objects.filter(email=email, is_active=False).first()          
                if is_active_qs:    
                    subject = 'Account activation required!'  
                    current_site = Site.objects.get_current()  
                    message = render_to_string('emails/account_activation_email.html', {
                        'user': is_active_qs,                    
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(is_active_qs.pk)),
                        'token': account_activation_token.make_token(is_active_qs),                        
                    })
                    
                    is_active_qs.email_user(subject, message)                   
                    raise forms.ValidationError(f'You have an account already with this email. An account activation link has been sent to your mailbox {email}')
        return super(ContractorSignUpForm, self).clean(*args, **kwargs)   

class OtpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'otp',)
        
        widgets = {                      
            'otp': forms.TextInput(attrs={'placeholder': 'OTP', 'class':'form-control', 'aria-label':'otp',  }),     
            
        }
    


class OrderInLineSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'email', 'mobile',)
        
    
    mobile = forms.CharField(label = 'Mobile', widget=forms.TextInput(attrs={"class": "form-control" }))    
    email = forms.EmailField(label = 'E-Mail Address', widget=forms.EmailInput(attrs={"class": "form-control"}))
    # password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={"class": "form-control" }))
    # password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    
    def clean(self, *args, **kwargs):
        mobile = self.cleaned_data.get('mobile')        
        email = self.cleaned_data.get('email')
        # password = self.cleaned_data.get('password1')
        
        if not mobile:
            raise forms.ValidationError(f'Mobile Number is essential!')
        
        if not email:
            raise forms.ValidationError('Email is essential!')    
        
        
            
        
        
        
        
        
    
    def save(self, commit=True):
        otp = generate_otp() 
        
        has_user = User.objects.filter(email=self.cleaned_data.get('email')).first()
        if has_user:            
            has_user.otp = otp
            
        else:
            has_user = super().save(commit=False)
            has_user.set_password(otp)
            has_user.mobile = self.cleaned_data.get('mobile')  
            has_user.email = self.cleaned_data.get('email')
            has_user.otp = otp
            
        if commit:
            has_user.save()   
            
            
      
            
        return has_user

            
        
                
  


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile', 'email']
        
        widgets = {                      
            'username': forms.TextInput(attrs={'placeholder': 'username', 'class':'form-control', 'aria-label':'username',  }),
            'first_name': forms.TextInput(attrs={'placeholder': 'first_name', 'class':'form-control', 'aria-label':'first_name' }),
            'last_name': forms.TextInput(attrs={'placeholder': 'last_name','class':'form-control', 'aria-label':'last_name', }), 
            # 'orgonization': forms.TextInput(attrs={'placeholder': 'orgonization','class':'form-control', 'aria-label':'orgonization', }), 
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile','class':'form-control', 'aria-label':'mobile', }), 
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class':'form-control', 'aria-label':'email' , }),     
            
        }
        labels = {                    
            'username':'Username',
            'first_name':'First name',
            'last_name':'Last Name',
            # 'orgonization':'Orgonization',
            'mobile':'Mobile',
            'email': 'Email',            
        }
        
# custom input typ        
class DateInput(forms.DateInput):
    input_type = 'date'       
   
        
class ProfileForm(forms.ModelForm):   
    class Meta:    
        model = Profile
        fields = ['about_me', 'my_location']        
        widgets = {                      
            'about_me': forms.Textarea(attrs={'placeholder': 'About Me', 'class':'form-control', 'aria-label':'about_me', 'style':"height: 150px;" }),
            'my_location': forms.TextInput(attrs={'placeholder': 'My Location', 'class':'form-control', 'aria-label':'my_location' }),
            'avatar': forms.FileInput(attrs={ 'class':'form-control', 'aria-label':'avatar' }),   
        }
        labels = {    
            'about_me': 'About Me',
            'my_location': 'My Location',
        }
class AvatarForm(forms.ModelForm):
    class Meta:    
        model = Profile
        fields = ['avatar']        
        widgets = {  
            'avatar': forms.FileInput(attrs={ 'class':'form-control', 'aria-label':'avatar' }),   
        }
        
class ContractorForm(forms.ModelForm):   
    # skills_in = forms.ModelMultipleChoiceField(
    #     queryset=BdService.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )
    class Meta:
        model = Contractor
        fields = ['skills_in','cv_link']
        widgets = {                      
            'skills_in': forms.CheckboxSelectMultiple(),
            'cv_link': forms.TextInput(attrs={'placeholder': 'htts://example.com', 'class':'form-control', 'aria-label':'cv_link' }),
            

        }

        
class UserPayoutForm(forms.ModelForm):   
    class Meta:    
        model = UserPayout
        fields = ['payout_method', 'payout_account']
        
    

class SetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)        
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        
        
        
class PasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)        
        self.fields['email'].widget = forms.EmailInput(attrs={ 'class':'form-control'}) 
        
        


class PasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        
        

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        
        
        
class UserCreationFormFront(UserCreationForm):
    class Meta:
        model = User
        fields = ( 'email', 'mobile',  'password1', 'password2')
        
    # username = forms.CharField(label = 'Username', widget=forms.TextInput(attrs={"class": "form-control" }))
    mobile = forms.CharField(label = 'Mobile', widget=forms.TextInput(attrs={"class": "form-control" }))
    
    email = forms.EmailField(label = 'E-Mail Address', widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={"class": "form-control" }))
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)   
    
    def clean(self, *args, **kwargs):
        mobile = self.cleaned_data.get('mobile')        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        
        if not mobile:
            raise forms.ValidationError(f'Mobile Number is essential!')
            
        
        if email and password:
            email_qs = User.objects.filter(email=email)
            if not email_qs.exists():
                pass    
            else:               
                is_active_qs = User.objects.filter(email=email, is_active=False).first()          
                if is_active_qs:    
                    subject = 'Account activation required!'  
                    current_site = Site.objects.get_current()  
                    message = render_to_string('emails/account_activation_email.html', {
                        'user': is_active_qs,                    
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(is_active_qs.pk)),
                        'token': account_activation_token.make_token(is_active_qs),                        
                    })
                    
                    is_active_qs.email_user(subject, message)                   
                    raise forms.ValidationError(f'You have an account already with this email. An account activation link has been sent to your mailbox {email}')
        return super(UserCreationFormFront, self).clean(*args, **kwargs)    

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
 
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']    
        
        
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"  }))    
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # remember_me = forms.BooleanField(label = 'Remember me ', initial=False,  required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    
    
    
    
    def clean(self, *args, **kwargs):        
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            email_qs = User.objects.filter(email=email)
            if not email_qs.exists():
                raise forms.ValidationError("The user does not exist")
            else:
                is_active_qs = User.objects.filter(email=email, is_active=False).first()
                if is_active_qs:
                    subject = 'Account activation required!'  
                    current_site = Site.objects.get_current()  
                    message = render_to_string('emails/account_activation_email.html', {
                        'user': is_active_qs,                    
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(is_active_qs.pk)),
                        'token': account_activation_token.make_token(is_active_qs),                        
                    })
                    
                    is_active_qs.email_user(subject, message)                      
                    raise forms.ValidationError(f'Account is not active, your need to activate your account before login. An account activation link has been sent to your mailbox {email}')                
                else:
                    user = authenticate(email=email, password=password)  
                    
                    
                    '''
                    if reported_url_limit crossed it is last time login to delete reported url.
                    '''
                    # try:
                    #     site = site_info()
                    #     report_limit = site.get('reported_url_limit')                        
                    #     data = Shortener.objects.filter(creator = user, active = False)
                    #     if data.count() > int(report_limit):
                    #         user.is_active=False
                    #         user.save()
                    #         raise forms.ValidationError(f"You have more than {report_limit} reported url! Please delete the reported url to login further! if you can not do that please contact with us using contact form!")                             
                    # except:
                    #     pass    
                    
                    
                    
                    if not user:
                        raise forms.ValidationError("Incorrect password. Please try again!")    
        else:
            raise forms.ValidationError("Add you credentials!") 
                                           
        return super(LoginForm, self).clean(*args, **kwargs)
    
