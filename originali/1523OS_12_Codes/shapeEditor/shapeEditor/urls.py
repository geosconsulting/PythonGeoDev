from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^editor/', include('shapeEditor.editor.urls')),
    url(r'^tms/',    include('shapeEditor.tms.urls')),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
