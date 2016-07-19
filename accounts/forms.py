from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
        'username': forms.TextInput(attrs={'class' : "form-control", 'required': '', 'autofocus':'', 'placeholder' : 'Username'}),
        'first_name': forms.TextInput(attrs={'class' : "form-control", 'required': '', 'placeholder' : 'First Name'}),
        'last_name': forms.TextInput(attrs={'class' : "form-control", 'required': '', 'placeholder' : 'Last Name'}),
        'email': forms.TextInput(attrs={'class' : "form-control", 'required': '', 'placeholder' : 'Email'}),
        'password': forms.PasswordInput(attrs={'class' : "form-control", 'required': '', 'placeholder' : 'Password'}),
        }

    def save(self, commit=True):
        user = super(ModelForm,self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(2016,1939,-1), attrs={'class':"form-control", 'required':''}))
    class Meta:
        model = UserProfile
        fields = ('gender', 'bio', 'dob', 'location', 'display_pic')
        exclude = ('user', )
        widgets = {
            'gender' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':1, 'autofocus':'', 'placeholder': 'Gender'}),
            'bio' : forms.Textarea(attrs = {'class': "form-control", 'maxlength':160, 'placeholder': 'Bio'}),
            'location' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':50, 'placeholder': 'Location'}),
        }
