from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth.views import *
from django.contrib.auth import views as auth_views

from back_end import views

urlpatterns = [
    # Examples:
    
    url(r'^$', views.login, name='login'),
    url('', include('django.contrib.auth.urls')),


    url(r'', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

#    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
#    url(r'^logout/$', LogoutView.as_view(), name='logout'),
#    url(r'^accounts/logout', LogoutView.as_view(), name='logout'),
#    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^back_end/', include('back_end.urls')),
    url(r'^billingPOS/', include('gallery.urls')),
    
    
    url(r'^billingPOS/([0-9]{1})', include('gallery.urls')),
    
    #Para poder redirigir dependiendo del Rol del User
    url(r'login_success/$', views.login_success, name='login_success'),
    
    url(r'^back_end/verVenta/', include('back_end.urls')),
]