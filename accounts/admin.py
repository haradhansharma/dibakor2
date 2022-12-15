from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from .forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib import messages

class UserProfile(admin.StackedInline):
    model = Profile
    can_delete = False 



class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [ 'email', 'username', 'is_staff', 'is_active',]
    
    list_filter = ('is_active', 'is_staff', )
    search_fields = ('email', 'mobile',  'username',  )   
    inlines = [UserProfile]    

admin.site.register(User, UserAdmin)

admin.site.register(Contractor)
admin.site.register(UserPayout)



    
    

    