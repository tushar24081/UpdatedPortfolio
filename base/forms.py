from django import forms
from django.forms import ModelForm
from .models import *


class CreatePost(ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		widgets = {
		'tags': forms.CheckboxSelectMultiple(),
		}

class CommentForm(ModelForm):
	body = forms.CharField(label='', 
                            widget=forms.Textarea(attrs={'placeholder': 'Add a comment...', 'cols':7, 'rows': 10}))
	user = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Enter Display Name:'}))
	email = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email:'}))
	class Meta:	
		model = Comment
		fields = ('user', 'body', 'email')