from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''

app_name = 'doc'

urlpatterns = [
    path('webmanifest/', views.webmanifest, name='webmanifest'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  
    
] 


