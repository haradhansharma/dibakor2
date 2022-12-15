from django.db import models
from bds.models import BdService, PaymentMethod
# Create your models here.
import uuid
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone

class QIUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return super(QIUserManager, self).create_user(username, email, password, **extra_fields)

    def create_superuser(self, username = None, email=None, password=None, **extra_fields):
        return super(QIUserManager, self).create_superuser(username, email, password, **extra_fields)




class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        null=True,
        blank=True,
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
   
    email = models.EmailField('E-Mail Address', unique=True)
    mobile = models.CharField('Mobile Number', max_length=252, unique=True)
    otp = models.CharField(max_length=6)
    has_given_consent = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)

   
     
    
    objects = QIUserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']
    
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):        
        return reverse('accounts:user_link', args=[str(self.id)])
    
    @property
    def payout_verified(self):
        if self.userpayout.is_verified:
            return True
        return False
    
    @property
    def sreening_done(self):
        if self.contractor.screening_done:
            return True
        return False
    
    
class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)    
    skills_in = models.ManyToManyField(BdService, related_name='skilled_contarctor') 
    cv_link = models.URLField(null=True, blank=True)
    screening_done = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  
    

class UserPayout(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)       
    payout_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, related_name='payout_method')  
    payout_account = models.CharField(max_length=15, null=True) 
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  
      

    
class Profile(models.Model):
    # It is beeing created autometically during signup by using signal.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ProcessedImageField(upload_to='profile_photo',
                                           processors=[ResizeToFill(200, 200)],
                                           format='JPEG',
                                           options={'quality': 60})
    about_me = models.TextField('About Me', max_length=500, blank=True, null=True)
    
    
    my_location = models.CharField('My Location', max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  
    
    def __str__(self):
        return 'Profile for ' +  str(self.user.email)  
    


