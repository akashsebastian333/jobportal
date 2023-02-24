from django import forms
from .models import JobPost
from django import forms
from .models import Submission
from .models import Message
from django.contrib.auth.models import User


JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    )



class JobPostForm(forms.ModelForm):
    job_type = forms.ChoiceField(choices=JOB_TYPE_CHOICES)
    class Meta:
        model = JobPost
        fields = ['title','company', 'job_type','description']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('resume',)

class MessageForm(forms.ModelForm):
    recipient = forms.CharField()

    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')
    
    def __init__(self, *args, **kwargs):
        recipient_username = kwargs.pop('recipient_username', None)
        super().__init__(*args, **kwargs)
        if recipient_username:
            try:
                recipient = User.objects.get(username=recipient_username)
                self.initial['recipient'] = recipient.id
            except User.DoesNotExist:
                pass
    
    

    def clean_recipient(self):
        recipient = self.cleaned_data['recipient']
        try:
            recipient = User.objects.get(username=recipient)
        except User.DoesNotExist:
            raise forms.ValidationError("Recipient does not exist")
        return recipient

    def save(self, sender):
        message = super().save(commit=False)
        message.sender = sender
        message.recipient = self.cleaned_data['recipient']
        message.save()
        return message