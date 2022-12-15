
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView 
from .forms import LoginForm


app_name = 'accounts'
'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/contractor/', views.ContractorSignUpView.as_view(), name='contractor_signup'),
    path('contractor/dashboard/', views.ContractorDashboard.as_view(), name='contractor_dashboard'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',  authentication_form=LoginForm), name='login'), 
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'), 
    path("password_reset/done/",  views.CustomPasswordResetDoneView.as_view(), name="password_reset_done" ),
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(),  name="password_reset_confirm" ),
    path("reset/done/", views.CustomPasswordResetCompleteView.as_view(),  name="password_reset_complete", ),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),   
    path('profile-setting/', views.profile_setting, name='profile_setting'), 
    path('change-pass/', views.password_change, name='change_pass'),  
    path('delete-avatar/', views.delete_avatar, name='delete_avatar'),   
    path('myorders/', views.MyOrders.as_view(), name='myorders'),  
    path('pick-order/<int:order_id>/<int:user_id>', views.PickOrder.as_view(), name='pick_order'),   
    path('submit-picked/<int:order_id>/<int:user_id>', views.SubmitPicked.as_view(), name='submit_picked'),   
    
     
    
     
    
]












