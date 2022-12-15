from django import forms

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from .helper import get_ip
from .models import *


class AddressForm(forms.ModelForm):   
    class Meta:
        model = Address
        fields = ['shipping_address', 'payment_address']
        
        widgets = {                      
            'shipping_address': forms.Textarea(attrs={'name':'shipping_address', 'rows':'10', 'class':'form-control', 'aria-label':'Shipping Adddress' }),
            'payment_address': forms.Textarea(attrs={ 'name':'payment_address', 'rows':'10', 'class':'form-control', 'aria-label':'Payment Address' }),
        }
        labels = {                    
            'shipping_address':'Shipping Address',
            'payment_address':'Payment Address',
                     
        }
        
class ConfirmDataForm(forms.Form):
    indetity = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'aria-label':'Paid Amount'}), label="Trasection Indentity", label_suffix='')
    value = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control', 'aria-label':'Paid Amount', 'hx-include':"[name='order_id']", 'hx-get': reverse_lazy('bds:should_paid'), 'hx-target': '#amount_error', 'hx-trigger': 'keyup'}), label="Transection Value", label_suffix='')
    remarks = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'class':'form-control', 'aria-label':'Remarks'}), label="Remarks", label_suffix='')
    

    
    
class PartialPaidForm(forms.Form):
    indetity = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'aria-label':'Paid Amount'}), label="Trasection Indentity", label_suffix='')
    value = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control', 'aria-label':'Paid Amount', 'hx-include':"[name='order_id']", 'hx-get': reverse_lazy('bds:should_partial_paid'), 'hx-target': '#amount_error', 'hx-trigger': 'keyup'}), label="Transection Value", label_suffix='')
    remarks = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'class':'form-control', 'aria-label':'Remarks'}), label="Remarks", label_suffix='')
    
    
    
