from django import forms

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from userena.utils import get_profile_model
from captcha.fields import CaptchaField

from study_project.accounts.models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'text']

class AddNoteForm(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()


class EditProfileForm(forms.ModelForm):
    """ Base form used for fields that are always required """
    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=30,
                                 required=False)
    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    class Meta:
        model = get_profile_model()
        exclude = ['user', 'prepod']

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileForm, self).save(commit=commit)
        # Save first and last name
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return profile

from captcha.fields import CaptchaField

class AddNoteForm(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.ImageField(required=False)
    description = forms.CharField()
    captcha = CaptchaField()



