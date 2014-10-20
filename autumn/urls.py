from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from authentication import views as auth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autumn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^callback/', auth_views.handle_callback),
    
    url(r'^data/', include('autumn.data.urls')), # admin app


)
