from django import forms
from .models import Post

class CounterForm(forms.ModelForm):

    counter = forms.IntegerField()
    
