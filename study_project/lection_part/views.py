from django.template import Context
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from study_project.lection_part.models import *

def get_content_paged_list(content_list, request):
    
    paginator = Paginator(content_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return list

def courses_list(request):
    user = request.user 
    courses_list = Course.objects.all()
    courses = get_content_paged_list(courses_list, request)
    return render_to_response('courses_list.html', {"courses": courses, 'user' : user})

def course_detail(request, course_id):
    user = request.user 
    course = get_object_or_404(Course, id=course_id)
    courses_lections = Lection.objects.filter(course = course)
    lections = get_content_paged_list(courses_lections, request)
    c = Context({ 'courses_lections' : lections , 'course' : course, 'user' : user})
    return render(request, 'course_detail.html', c)

def lection_detail(request, course_id, lection_id):
    user = request.user 
    course = get_object_or_404(Course, id=course_id)
    lection = get_object_or_404(Lection, id=lection_id)
    texts = Text.objects.filter(lection = lection)
    photos = Photo.objects.filter(lection = lection)
    htmls = HtmlContent.objects.filter(lection = lection)
    files = File.objects.filter(lection = lection)
    video = Video.objects.filter(lection = lection)
    c = Context({'texts' : texts, 'photos' : photos,'htmls' : htmls, 
                 'files' : files, 'video' : video, 'lection' : lection, 
                 'course' : course, 'user' : user})
    return render(request, 'lection_detail.html', c)