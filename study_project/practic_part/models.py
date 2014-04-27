from django.db import models
from django.contrib import admin

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill

from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()    
    image = models.ImageField(upload_to='achievement_photos')
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(50, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Meta:
        ordering = ['date']
        
    def  __str__(self):
        return self.name

class CourseResult(models.Model):
    practical_course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    date = models.DateTimeField()    
    success = models.BooleanField(blank=True)
    achievement = models.BooleanField(default=True)
         
    def  __str__(self):
        return self.date

class PracticalLesson(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100)
    description = models.TextField()    
    date = models.DateTimeField()
    threshold = models.IntegerField(default = 100)
            
    class Meta:
        ordering = ['date']
        
    def  __str__(self):
        return self.name

class PracticalLessonResult(models.Model):    
    practical_course = models.ForeignKey(CourseResult)
    practical_lesson = models.ForeignKey(PracticalLesson)
    result = models.IntegerField()
    max = models.IntegerField(default = 0)
    success = models.BooleanField(blank=True)
    date = models.DateTimeField()
    polls = models.CharField(max_length=100)

    def  __str__(self):
        return self.date

class Poll(models.Model):
    practical_lesson = models.ForeignKey(PracticalLesson)
    question = models.CharField(max_length=200)
    is_obligatory = models.BooleanField(default = True)

    QUESTION_TYPE = (
        ('CH', 'Choise'),
        ('SOR', 'Sort'),
        ('COM', 'Compliance'),
        ('OPE', 'Open'),
    )

    question_type = models.CharField(choices=QUESTION_TYPE, max_length=3)
        
    date = models.DateTimeField()
    value = models.IntegerField(default=1)

    def  __str__(self):
        return self.question

    
class Sort(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

    def  __str__(self):
        return self.choice_text


class Sort(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

    def  __str__(self):
        return self.choice_text

class Compliance(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    right_text = models.CharField(max_length=200)

    def  __str__(self):
        return self.right_text
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    is_true = models.BooleanField(blank=True)

    def  __str__(self):
        return self.choice_text

class Open(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    
    def  __str__(self):
        return self.choice_text

class Answer(models.Model):
    poll = models.ForeignKey(Poll)
    pr_res = models.ForeignKey(PracticalLessonResult)    
    answer_text = models.CharField(max_length=200)

    def  __str__(self):
        return self.answer_text


class PracticalLessonInline(admin.TabularInline):
    model = PracticalLesson
    fields = ('course', 'name', 'description', 'date', 'threshold')
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [PracticalLessonInline]

class PollInline(admin.TabularInline):
    model = Poll
    fields = ('practical_lesson', 'question', 'is_obligatory', 'question_type','date', 'value')
    extra = 1

class PracticalLessonAdmin(admin.ModelAdmin):
    fields = ('course', 'name', 'description', 'date', 'threshold')
    inlines = [PollInline]

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class OpenInline(admin.TabularInline):
    model = Open
    extra = 1

class ComplianceInline(admin.TabularInline):
    model = Compliance
    extra = 1

class SortInline(admin.TabularInline):
    model = Sort
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline] + [OpenInline] + [ComplianceInline] + [SortInline]
    fields = ('practical_lesson', 'question', 'is_obligatory', 'question_type','date', 'value')

    def get_actions(self, request):
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Course, CourseAdmin)
admin.site.register(PracticalLesson, PracticalLessonAdmin)
admin.site.register(Poll, PollAdmin)