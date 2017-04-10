from django import forms
from pagedown.widgets import PagedownWidget
from .models import Note 

''' form Class 
	Using PageDown Api in Pypi	
'''
class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model=Note
		fields=[
			"title",
			"content",
			"publish",
			]
