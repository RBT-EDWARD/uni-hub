from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control",'rows':3}), required=False)
    interests = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control",'rows':3}), required=False)
    username =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','bio','interests']
        
