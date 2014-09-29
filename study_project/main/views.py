from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from study_project.main.forms import *

def index(request):
    user = request.user    
    return render(request, 'index.html', {'user' : user})

def thanks(request):
    return render(request, 'thanks.html')

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['evilejik@yandex.ru']
            if cc_myself:
                recipients.append(sender)
            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render(request, 'contact.html', {'form': form,})
