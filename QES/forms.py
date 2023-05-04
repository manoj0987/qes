from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('detail',)

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields=('title','detail','tags')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})