from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'DIBAKOR admin'
admin.site.site_title = 'DIBAKOR admin'
# admin.site.site_url = ''
admin.site.index_title = 'DIBAKOR administration'
# admin.empty_value_display = '**Empty**'

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('', include('bds.urls')),    
    path('doc/', include('doc.urls')),  
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



