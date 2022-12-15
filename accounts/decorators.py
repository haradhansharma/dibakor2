
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import PermissionDenied
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.urls.base import reverse
from django.contrib import messages

# Funtion protector to access by user type of expert or staff or superuser
def contractor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_contractor or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            return HttpResponseRedirect(reverse('accounts:profile_setting'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap 


def screening_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.sreening_done or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            return HttpResponseRedirect(reverse('accounts:profile_setting'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap 

def payout_verification_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.payout_verified or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            return HttpResponseRedirect(reverse('accounts:profile_setting'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap 




