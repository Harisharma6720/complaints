"""from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Profile,Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import requests

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=('Subject','Type_of_complaint','Description')
        

class UserProfileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('contactnumber',)
    

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def clean_email(self):
            # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

'''class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location',)'''
    
class ProfileUpdateForm(forms.ModelForm):
    email =forms.EmailField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    first_name=forms.CharField( max_length=30, required=True)
    last_name=forms.CharField( max_length=30, required=True)

    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
    def clean_email(self):
            # Get the email
        username = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.exclude(pk=self.instance.pk).get(username=username)
            
            
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class UserProfileUpdateform(forms.ModelForm):
    
    
    Branch=forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model=Profile
        fields=('contactnumber',)

class statusupdate(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=('status',)  
        help_texts = {
            'status': None,
          
        }      """

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Profile, Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('Subject', 'Type_of_complaint', 'address', 'Description','latitude', 'longitude', 'image')
        def clean_image(self):
            image = self.cleaned_data.get('image')
            if not image:
                raise forms.ValidationError("This field is required.")
            return image
        widgets = {
            
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(),  # Hidden field for latitude
            'longitude': forms.HiddenInput(),  # Hidden field for longitude
            'address': forms.TextInput(attrs={'placeholder': 'Enter the address'}),

        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('contactnumber',)

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField()
    address = forms.CharField(max_length=100)  # Add this line


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address' )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[a-zA-Z]+$", first_name):
            raise forms.ValidationError('First name should contain only alphabetic characters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[a-zA-Z]+$", last_name):
            raise forms.ValidationError('Last name should contain only alphabetic characters.')
        return last_name
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email != email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class UserProfileUpdateForm(forms.ModelForm):
    #Statusss = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Profile
        fields = ('contactnumber',)

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('status',)
        help_texts = {
            'status': None,
        }
