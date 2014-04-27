from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.urlresolvers import reverse
import datetime
import random

from study_project.practic_part.models import *
from study_project.accounts.models import Note

def practic_courses_list(request):
    courses = Course.objects.all()
    user = request.user
    c = Context({ 'courses' : courses, 'user' : user})
    return render(request, 'practic_courses_list.html', c)

def practic_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    courses_practical = PracticalLesson.objects.filter(course = course)
    user = request.user
    c = Context({ 'courses_practical' : courses_practical , 'course' : course, 'user' : user})
    return render(request, 'practic_course_detail.html', c)

def practical_lesson_detail(request, course_id, practical_lesson_id):
    polls_choices_list = []
    polls_open_list = []
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    cour_pract, cour_pract_f = CourseResult.objects.get_or_create(practical_course=course, user = user,
                  defaults={'date': datetime.datetime.now(), 'success' : False})
    practical = get_object_or_404(PracticalLesson, id=practical_lesson_id)
    practical_list = PracticalLesson.objects.filter(course = practical.course)
    c = Context({'practical' : practical, 'course' : course, 'user' : user})
        
    for p in practical_list:
        if p.id < practical.id:
            try:
                pract = PracticalLessonResult.objects.get(practical_lesson=p, practical_course=cour_pract)
            except PracticalLessonResult.DoesNotExist:
                c.update({'perm' : False})
                return render(request, 'practical_lesson_detail.html', c)
            else:
                if pract.success != True:
                    c.update({'perm' : False})
                    return render(request, 'practical_lesson_detail.html', c)
        else: break
    
    res, res_f = PracticalLessonResult.objects.get_or_create(practical_lesson=practical, practical_course = cour_pract,
                  defaults={'date': datetime.datetime.now(), 'result' : 0, 'success' : False, 'max' : 0, 'polls' : ''})
                     
    polls_obl = Poll.objects.filter(practical_lesson=practical, is_obligatory=True)
    polls_obl_list = []
    for p in polls_obl:
        polls_obl_list.append(p)
                
    polls_not_obl = Poll.objects.filter(practical_lesson=practical, is_obligatory=False)
    polls_not_obl_index_arr = [x for x in range(len(polls_not_obl))]
    rnd_poll = []
    polls_index_list = []
    while len(polls_not_obl_index_arr) > len(polls_not_obl)/2:
        index = random.randrange(0, len(polls_not_obl_index_arr))
        rnd_poll.append(polls_not_obl[polls_not_obl_index_arr[index]])
        polls_index_list.append(polls_not_obl[polls_not_obl_index_arr[index]].id)
        polls_not_obl_index_arr.pop(index)  
    
    res.polls = ""
    for i in polls_index_list:
        res.polls += str(i) + "_"
    
    polls = polls_obl_list + rnd_poll
    
    res.max = 0
    for p in polls:
        res.max += p.value

    res.save()     
    polls_index_arr = [x for x in range(len(polls))]
    while polls_index_arr:
        index = random.randrange(0, len(polls_index_arr))
        cur_poll = polls[polls_index_arr[index]]

        if cur_poll.question_type == 'CH':
            choises = Choice.objects.filter(poll = cur_poll)
            polls_choices_index_arr = [x for x in range(len(choises))]
            cur_choice = []
            while polls_choices_index_arr:
                choices_index = random.randrange(0, len(polls_choices_index_arr))
                cur_choice.append(choises[polls_choices_index_arr[choices_index]])
                polls_choices_index_arr.pop(choices_index)
            polls_choices_list.append({ cur_poll : cur_choice})
        
        elif cur_poll.question_type == 'OPE':
            polls_choices_list.append({ cur_poll : Open.objects.filter(poll = cur_poll)})
        
        elif cur_poll.question_type == 'COM':
            choises = Compliance.objects.filter(poll = cur_poll)            
            polls_right_index_arr = [x for x in range(len(choises))]
            i=len(choises)-1
            cur_choice = []
            while polls_right_index_arr:                
                right_index = random.randrange(0, len(polls_right_index_arr))
                cur_choice.append([choises[i].choice_text, choises[polls_right_index_arr[right_index]].right_text])                
                polls_right_index_arr.pop(right_index)
                i-=1
            polls_choices_list.append({ cur_poll : cur_choice})

        elif cur_poll.question_type == 'SOR':
            choises = Sort.objects.filter(poll = cur_poll)            
            polls_choise_index_arr = [x for x in range(len(choises))]            
            i=len(choises)-1
            cur_choice = []
            while polls_choise_index_arr:                
                choise_index = random.randrange(0, len(polls_choise_index_arr))
                cur_choice.append(choises[polls_choise_index_arr[choise_index]].choice_text)
                polls_choise_index_arr.pop(choise_index)
                i-=1
            polls_choices_list.append({ cur_poll : cur_choice})

        polls_index_arr.pop(index)
   
    c.update({'polls_choices_list' : polls_choices_list, 
              'perm' : True})
    return render(request, 'practical_lesson_detail.html', c)


def result_set(Type, p, res, result, request):
    
    if Type == Choice:
        c = request.POST.get(str(p.id))
        if c:
            selected_choice = get_object_or_404(Type, id = c).choice_text
        else:
            selected_choice = ''

    elif Type == Open:
        selected_choice = request.POST.get(str(p.id))

    elif Type == Compliance:
        selected_choice = ""
        l = Compliance.objects.filter(poll=p)        
        for i in range(1, len(l)+1):
            c = str(p.id) + "-" + str(i)
            selected_choice += request.POST.get(c) + '_'

    elif Type == Sort:
        selected_choice = ""
        l = Sort.objects.filter(poll=p)        
        for i in range(1, len(l)+1):
            c = str(p.id) + "-" + str(i)
            selected_choice += request.POST.get(c) + '_'

    a, a_f = Answer.objects.get_or_create(poll=p, pr_res = res,
                                          defaults={'answer_text': selected_choice})
    if not a_f:
        a.answer_text = selected_choice
        a.save()        
    
    if Type == Compliance:
        f = 0
        res = selected_choice.split('_')
        for i in range(0, len(l)):
            if res[i] != l[len(l)-i-1].right_text:
                f = 0
                break
            else:
                f = 1
        if f == 1:
            result += p.value

    elif Type == Sort:
        f = 0
        res = selected_choice.split('_')
        for i in range(0, len(l)):

            if res[i] != l[i].choice_text:
                f = 0
                break
            else:
                f = 1
        if f == 1:
            result += p.value

    else:
        text_list = []
        if Type == Choice:
            choice_list = Choice.objects.filter(poll=p.id, is_true=1)
        elif Type == Open:
            choice_list = Open.objects.filter(poll=p.id)

        for i in choice_list:
            text_list.append(i.choice_text)
        if selected_choice in text_list:
            result += p.value

    return result

def get_polls_pract_res(res, practical_lesson_id):
    poll_not_obl_index = res.polls.split('_')[0:-1]

    polls = get_list_or_404(Poll, practical_lesson = practical_lesson_id, is_obligatory=True)    
    polls_obl_list = []
    for p in polls:
        polls_obl_list.append(p)
    polls = polls_obl_list

    for i in poll_not_obl_index:
        polls.append(get_object_or_404(Poll, id=i))

    return polls

def vote(request, course_id, practical_lesson_id):
    course = get_object_or_404(Course, id=course_id)
    practical = get_object_or_404(PracticalLesson, id=practical_lesson_id)
    user = request.user

    cour_pract = CourseResult.objects.get(practical_course=course, user = user)
    
    if cour_pract.success == True:
        if cour_pract.achievement == True:
            cour_pract.achievement = False

    res = get_object_or_404(PracticalLessonResult, practical_lesson=practical, practical_course = cour_pract)
    polls = get_polls_pract_res(res, practical_lesson_id)

    result = 0
    
    for p in polls:
        if p.question_type == 'CH':
            result = result_set(Choice, p, res, result, request)
        elif p.question_type == 'OPE':
            result = result_set(Open, p, res, result, request)
        elif p.question_type == 'COM':
            result = result_set(Compliance, p, res, result, request)
        elif p.question_type == 'SOR':
            result = result_set(Sort, p, res, result, request)

    res.result = result
    res.date = datetime.datetime.now()

    if practical.threshold*res.max/100 > result:
       res.success = False       
    else:
       res.success = True
                  
    res.save()

    practical_list = PracticalLesson.objects.filter(course = practical.course)
    for p in practical_list:        
        try:
            pract = PracticalLessonResult.objects.get(practical_lesson=p, practical_course=cour_pract)
        except PracticalLessonResult.DoesNotExist:
            cour_pract.success = False
            break
        else:
            if pract.success == False:
                cour_pract.success = False
                break
            else:
               cour_pract.success = True

    cour_pract.save()

    if cour_pract.success == True:
        if cour_pract.achievement == True:
            name = 'Заработано достижение по курсу ' + course.name + '!'
            des = 'Мной получено достижение по курсу ' + course.name + ' с результатом ' + str(result) +'!'
            note = Note(user=user, name=name, date=datetime.datetime.now(), image=course.image, description=des)
            note.save()

    return HttpResponseRedirect(reverse('result', args=(str(practical_lesson_id))))

def get_obj_or_list(Type, p, res_id, polls_answers):
    if Type == Compliance:
        c = Compliance.objects.filter(poll=p.id)
        res = ""
        for ch in c:
            res += ch.choice_text + " - " + ch.right_text + " | "
        my_res = ""
        r = get_object_or_404(Answer, poll=p.id, pr_res = res_id).answer_text        
        r = r.split('_')
        r = r[0:-1]
        r.reverse()
        for t in range(0, len(r)):
            my_res += c[t].choice_text + " - " + r[t] + " | "

        polls_answers.update({ p : [res, my_res]})
    elif Type == Sort:
        c = Sort.objects.filter(poll=p.id)
        res = ""
        for ch in c:
            res += ch.choice_text + " | "
        my_res = ""
        r = get_object_or_404(Answer, poll=p.id, pr_res = res_id).answer_text        
        r = r.split('_')
        r = r[0:-1]
        r.reverse()
        for t in range(0, len(r)):
            my_res += c[t].choice_text + " - " + r[t] + " | "
            my_res += c[t].choice_text + " | "


        polls_answers.update({ p : [res, my_res]})

    elif Type == Sort:
        c = Sort.objects.filter(poll=p.id)
        res = ""
        for ch in c:
            res += ch.choice_text + " | "
        my_res = ""
        r = get_object_or_404(Answer, poll=p.id, pr_res = res_id).answer_text        
        r = r.split('_')
        r = r[0:-1]
        r.reverse()
        for t in range(0, len(r)):
            my_res += c[t].choice_text + " | "

        polls_answers.update({ p : [res, my_res]})

    else:
        if Type == Choice:
            c = Choice.objects.filter(poll=p.id, is_true=1)
        elif Type == Open:
            c = Open.objects.filter(poll=p.id)    
        res = ""
        for ch in c:
            res += ch.choice_text + " "

        polls_answers.update({ p : [res, 
                                       get_object_or_404(Answer, poll=p.id, pr_res = res_id).answer_text]})       

def result(request, practical_lesson_id):
    polls_answers = {}
    practical = get_object_or_404(PracticalLesson, id = practical_lesson_id)
    user = request.user
    course_res = get_object_or_404(CourseResult, practical_course=practical.course, user = user)
    course = get_object_or_404(Course, id=practical.course.id)
    res = get_object_or_404(PracticalLessonResult, practical_lesson=practical, practical_course=course_res)
    polls = get_polls_pract_res(res, practical_lesson_id)

    for p in polls:
       if p.question_type == 'CH':
           get_obj_or_list(Choice, p, res.id, polls_answers)

       elif p.question_type == 'OPE':
           get_obj_or_list(Open, p, res.id, polls_answers)

       elif p.question_type == 'COM':
           get_obj_or_list(Compliance, p, res.id, polls_answers)

       elif p.question_type == 'SOR':
           get_obj_or_list(Sort, p, res.id, polls_answers) 

    return render(request, 'results.html', {'polls_answers': polls_answers, 'practical' : practical, 
                                            'res' : res, 'achievement' : course_res.achievement, 
                                            'curs_succ' : course_res.success, 'im_achiv' : course.image_small})
