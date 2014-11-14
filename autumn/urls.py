from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from authentication import views as auth_views
from views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autumn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^logout/', auth_views.logout),
    url(r'^callback/', auth_views.handle_callback),
    url(r'^home/', home),
    
    url(r'^data/', include('autumn.data.urls')),
    url(r'^dev/', include('autumn.dev.urls')), 
    url(r'^org/', include('autumn.org.urls')),


    url(r'login/', auth_views.authentication_landing),
)
