from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from doc.models import ExSite
from doc.doc_processor import site_info
from django.templatetags.static import static

# from selfurl.decorators import coockie_exempts



def webmanifest(request):
    site = site_info()      
    icons = []    
    ic192 = {
        # "src": static(site['og_image']),
        "sizes": "192x192",
        "type": "image/png"        
    }
    
    icons.append(ic192)   
    ic512 = {
        # "src": static(site['og_image']),
        "sizes": "512x512",
        "type": "image/png"        
    }
    icons.append(ic512)    
    data = {
        'name' : site['name'],
        'short_name' : site['name'],
        'icons' : icons,
        # 'meta_name': site.site_meta,
        # 'description': site.site_description,
        # 'tag': site.site_meta_tag,
        # 'favicon': site.site_favicon.url,
        # 'logo': site.site_logo.url,
        # 'slogan': site.slogan,
        # 'og_image': site.og_image.url,
        # 'phone': site.phone,
        # 'email': site.email,
        # 'location': site.location,
        # 'facebook_link': site.facebook_link,
        # 'twitter_link': site.twitter_link,
        # 'linkedin_link': site.linkedin_link,
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"        
    }
    
    return JsonResponse(data, safe=False)


def terms_and_conditions(request):
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='doc:terms_and_conditions')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('doc:terms_and_conditions')),
        'description': description,        
        'slogan': title, 
    }    
    seo_info.update(modify)  
    context = {
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='doc:terms_and_conditions') 
    }
    return render(request, 'doc/terms.html', context = context)


def privacy_policy(request):
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='doc:privacy_policy')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('doc:privacy_policy')),
        'description': description,        
        'slogan': title, 
    }    
    seo_info.update(modify)  
    context = {
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='doc:privacy_policy') 
    }
    return render(request, 'doc/privacy.html', context = context)


    
