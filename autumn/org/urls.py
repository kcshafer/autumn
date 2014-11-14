from django.conf.urls import patterns, include, url


from autumn.org import views

urlpatterns = patterns('',
    url(r'^sobjects', views.sobject_overview),
    url(r'^generateobject', views.generate_sobject),
    url(r'^generatexcel', views.generate_excel),
)