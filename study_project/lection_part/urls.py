from django.conf.urls import *
from study_project.lection_part.views import courses_list, course_detail, lection_detail

urlpatterns = patterns('',
url(r'^courses/$', courses_list),
url(r'^courses/(?P<course_id>\d+)/$', course_detail, name='course_detail'),
url(r'^courses/(?P<course_id>\d+)/lections/(?P<lection_id>\d+)/$', lection_detail, name='lection_detail'),
)
