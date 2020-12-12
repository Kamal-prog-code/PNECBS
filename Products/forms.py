from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['User_Name','Email','Password']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Med_file
        fields = '__all__'