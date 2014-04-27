from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill


class Prepod(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,unique=True)
    
    PERM_TYPE = (
        ('SM', 'Send Message'),
        ('EP', 'Edit Profile')
    )

    perm_type = models.CharField(choices=PERM_TYPE, max_length=3)

    def  __str__(self):
        return self.name

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,unique=True,  
                        verbose_name=_('user'),related_name='my_profile')  
    number_of_group = models.CharField(max_length=100)
    prepod = models.ManyToManyField(Prepod, blank=True)

    def  __str__(self):
        return self.user.get_username()
    
   

class MyProfile(UserenaBaseProfile):  
    user = models.OneToOneField(User,unique=True,  
                        verbose_name=_('user'),related_name='my_profile')  
    favourite_snack = models.CharField(_('favourite snack'),max_length=5)  



class Note(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='user_blog_photos', blank=True)
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 100})
    description = models.TextField()
    class Meta:
        ordering = ['-date']
        
    def  __str__(self):
        return self.name


class Message(models.Model):
    prep = models.ForeignKey(Prepod)
    user = models.ForeignKey(User)
    from_to = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    text = models.TextField()

    class Meta:
        ordering = ['-date']

    def  __str__(self):
        return self.name

admin.site.register(Note)
admin.site.register(Prepod)
admin.site.register(Message)