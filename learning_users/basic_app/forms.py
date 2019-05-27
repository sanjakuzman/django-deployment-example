from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfoForm

class UseInfo(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    # whit this class we are getting the defaults fields from the user models
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):

    # just getting the fileds created in the UserProfileInfo model in models.py
    class Meta():
        model = UserProfileInfoForm
        fields = ('portfolio_site', 'profile_pic')
