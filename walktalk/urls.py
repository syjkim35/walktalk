from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'backend.views.home'),
    url(r'^login/', 'backend.views.login', name='login'),
    url(r'^register/', 'backend.views.register', name='register'),
    url(r'^schedule/', 'backend.views.schedule', name='schedule'),
    # url(r'^admin/', include(admin.site.urls)),
)
