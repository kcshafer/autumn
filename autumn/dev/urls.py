from django.conf.urls import patterns, include, url


from autumn.dev import views

urlpatterns = patterns('',
    url(r'^executeanonymous', views.execute_anonymous),
    url(r'^execute', views.execute),
)