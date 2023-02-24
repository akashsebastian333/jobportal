from django import forms
from .models import JobPost
from django import forms


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title','company', 'description']


