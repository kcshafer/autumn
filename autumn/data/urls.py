from django.conf.urls import patterns, include, url


from autumn.data import views

urlpatterns = patterns('',
    url(r'^query', views.query),
    url(r'^soql', views.soql),
)