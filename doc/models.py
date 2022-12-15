from django.db import models
from django.apps import apps
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.apps import apps
from django.template.defaultfilters import slugify
from django.core.validators import FileExtensionValidator
# from selfurl.urls import get_self_urls    
# from contact.urls import get_contact_urls
# from accounts.urls import get_accounts_urls




    
class ExSite(models.Model):    
    site = models.OneToOneField(Site, primary_key=True, verbose_name='site', on_delete=models.CASCADE)
    site_meta = models.CharField(max_length=256)
    site_description = models.TextField(max_length=500)
    site_meta_tag =models.CharField(max_length=255)
    site_favicon = models.ImageField(upload_to='site_image')
    site_logo = models.ImageField(upload_to='site_image')
    slogan = models.CharField(max_length=150, default='')
    og_image = models.ImageField(upload_to='site_image')
    mask_icon = models.FileField(upload_to='site_image', validators=[FileExtensionValidator(['svg'])])
    
    
    phone = models.CharField(max_length=15)
    email = models.EmailField()    
    location=models.CharField(max_length=120)
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()
    
    
    reported_url_limit = models.IntegerField(default=3)
    
    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()  
    
# class MetaText(models.Model):  
#     from doc.urls import get_doc_urls
    
#     get_urls = get_self_urls() 
#     get_urls += get_contact_urls()
#     get_urls += get_doc_urls()
#     get_urls += get_accounts_urls()
   
    
    

#     title = models.CharField(max_length=60)
#     description = models.TextField(max_length=160)
#     body = models.TextField()
#     path = models.CharField(max_length=50, choices=get_urls)
    
    
#     def __str__(self):
#         return self.path


# class Acordion(models.Model): 
#     from doc.urls import get_doc_urls
    
#     get_urls = get_self_urls()  
#     get_urls += get_contact_urls() 
#     get_urls += get_doc_urls()
#     get_urls += get_accounts_urls()
   
    
     
#     button_text = models.CharField(max_length=256)
#     button_des = models.TextField()
#     path = models.CharField(max_length=50, choices=get_urls)   
#     fa_icon_class = models.CharField(max_length=250, blank=True, null=True) 
    
#     def __str__(self):
#         return self.button_text + '(' + self.path + ')'
    

    
    
# class Menus(models.Model):
    # from doc.urls import get_doc_urls
    
    # get_urls = get_self_urls()  
    # get_urls += get_contact_urls() 
    # get_urls += get_doc_urls()
    # get_urls += get_accounts_urls()
   
    
    # LOC =(
    # ("footer", "Footer"),
    # ("header", "Header"),    
    # )
    
    
    # path = models.CharField(max_length=50, choices=get_urls)    
    # name = models.CharField(max_length=50)       
    # location = models.CharField(max_length=50, choices=LOC)   
    # sort_order = models.IntegerField(default=1) 
    
    
    # def __str__(self):
    #     return str(self.sort_order) + '-' + self.name + '(' + self.location + ')'
    