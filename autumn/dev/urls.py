from django.conf.urls import patterns, include, url


from autumn.dev import views

urlpatterns = patterns('',
    url(r'^executeanonymous', views.execute_anonymous),
    url(r'^execute', views.execute),
    url(r'^tests', views.test_view),
    url(r'^runtests', views.run_tests),
    url(r'^testitems', views.retrieve_test_items),
    url(r'^testresults', views.retrieve_test_results),
    url(r'^retrieve', views.retrieve_metadata),
    url(r'^downloadmetadata', views.download_metadata),
)