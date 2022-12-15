from django.urls import reverse


def site_info():
    from doc.models import ExSite    
    try:  
        site = ExSite.on_site.get()   
        site_info = {
            'name' : site.site.name,
            'domain' : site.site.domain, 
            'canonical' : reverse('bds:bds_list'),
            'meta_name': site.site_meta,
            'description': site.site_description,
            'tag': site.site_meta_tag,
            'favicon': site.site_favicon.url,
            'mask_icon': site.mask_icon.url,
            'logo': site.site_logo.url,
            'slogan': site.slogan,
            'og_image': site.og_image.url,
            'phone': site.phone,
            'email': site.email,
            'location': site.location,
            'facebook_link': site.facebook_link,
            'twitter_link': site.twitter_link, 
            'linkedin_link': site.linkedin_link,    
            'reported_url_limit': site.reported_url_limit,     
        } 
        
        return site_info
    except:
        return None

# def footer_menu():
#     from django.urls import reverse
#     from .models import Menus    
#     menus = Menus.objects.filter(location = 'footer').order_by('sort_order')  
    
#     menu_items = {}     
#     for menu in menus:
#         menu_item = {
#             menu.name : reverse( menu.path ),
#         }         
#         menu_items.update(menu_item)       
        
    
    
    # return menu_items

# def header_menu():
#     from django.urls import reverse
#     from .models import Menus    
#     menus = Menus.objects.filter(location = 'header').order_by('sort_order')  
    
#     menu_items = {}     
#     for menu in menus:
#         menu_item = {
#             menu.name : reverse( menu.path ),
#         }         
#         menu_items.update(menu_item)     
     
    
#     return menu_items


    
    

def comon_doc(request):
    from django.template.loader import render_to_string
    
    google_code = render_to_string("layouts/googlescripts.html")
    
    text = {
        'user_congrets': f"Hi , {request.user.username}",        
    }
    return {   
            'site': site_info(),
            'text': text,
            # 'footer_menu': footer_menu(),
            # 'header_menu' : header_menu(),
            'google_code' : google_code
            
    }
    
