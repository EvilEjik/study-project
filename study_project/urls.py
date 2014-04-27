from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings

from study_project.lection_part.views import *
from study_project.main.views import index, contact, thanks



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',     
     url(r'^lection_part/', include('study_project.lection_part.urls')),
     url(r'^practic_part/', include('study_project.practic_part.urls')),
     url(r'^accounts/', include('study_project.accounts.urls')),
     
     url(r'^contact/', contact),
     url(r'^thanks/', thanks),
     url(r'^$', index),
     
     url(r'^admin/', include(admin.site.urls)),
     url(r'^favicon\.ico$', RedirectView.as_view(url='/media/favicon.ico')),
     url(r'^captcha/', include('captcha.urls')),     
                       
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
