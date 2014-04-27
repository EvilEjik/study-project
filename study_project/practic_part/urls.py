from django.conf.urls import *
from study_project.practic_part.views import *

urlpatterns = patterns('',
url(r'^courses/$', practic_courses_list),
url(r'^courses/(?P<course_id>\d+)/$', practic_course_detail, name='practic_course_detail'),
url(r'^courses/(?P<course_id>\d+)/practical_lesson/(?P<practical_lesson_id>\d+)/$', practical_lesson_detail, name='practical_lesson_detail'),
url(r'^courses/(?P<course_id>\d+)/practical_lesson/(?P<practical_lesson_id>\d+)/vote/$', vote, name='vote'),
url(r'^(?P<practical_lesson_id>\d+)/result/$', result, name='result'),
)
