from django.db import models
from django.contrib import admin

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()    
    image = models.ImageField(upload_to='courses_photos')
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    date = models.DateTimeField()

    class Meta:
        ordering = ['date']
        
    def  __str__(self):
        return self.name

class Lection(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lections_photos')
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    date = models.DateTimeField()
        
    class Meta:
        ordering = ['date']
        
    def  __str__(self):
        return self.name

class Text(models.Model):
    lection = models.ForeignKey(Lection)
    content = models.TextField()
                
    def  __str__(self):
        return self.content

class HtmlContent(models.Model):
    lection = models.ForeignKey(Lection)
    content = models.TextField()
                
    def  __str__(self):
        return self.content

class File(models.Model):
    lection = models.ForeignKey(Lection)
    name = models.CharField(max_length = 100)
    content = models.FileField(upload_to='lections_photos/files')
                
    def  __str__(self):
        return self.name

class Photo(models.Model):
    lection = models.ForeignKey(Lection)
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='lections_photos/photos')
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
                
    def  __str__(self):
        return self.name

class Video(models.Model):
    lection = models.ForeignKey(Lection)
    name = models.CharField(max_length = 100)
    content = models.FileField(upload_to='lections_photos/video')
                
    def  __str__(self):
        return self.name

class LectionInline(admin.TabularInline):
    model = Lection
    extra = 1

class TextInline(admin.StackedInline):
    model = Text
    extra = 1

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1

class HtmlContentInline(admin.StackedInline):
    model = HtmlContent
    extra = 1

class FileInline(admin.StackedInline):
    model = File
    extra = 1

class VideoInline(admin.StackedInline):
    model = Video
    extra = 1

class LectionAdmin(admin.ModelAdmin):
    inlines = [TextInline, PhotoInline, HtmlContentInline, FileInline, VideoInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [LectionInline]
    
admin.site.register(Course, CourseAdmin)    
admin.site.register(Lection, LectionAdmin)
