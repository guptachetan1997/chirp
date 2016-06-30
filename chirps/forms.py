from django import forms
from django.forms import ModelForm
from models import chirp

class ChirpForm(forms.ModelForm):
    class Meta:
        model = chirp
        exclude = ['timestamp', 'like', 'user', 'rechirp_status', 'origin_chirp_user', 'parent']
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class' : "form-control", 'maxlength' : 140, 'required': '', 'autofocus':'', 'placeholder' : 'Whats Happening?'}),
        }

class ChirpReplyForm(forms.ModelForm):
    class Meta:
        model = chirp
        exclude = ['timestamp', 'like', 'user', 'rechirp_status', 'origin_chirp_user', 'parent', 'content']
