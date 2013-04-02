from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^sim$', 'frontend.views.kickoff', name='kickoff'),
    url(r'^stop', 'frontend.views.stop_all', name='stop_all'),
    url(r'^', 'frontend.views.show_results', name='show_results'),
    # url(r'^nhl_sim/', include('nhl_sim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
