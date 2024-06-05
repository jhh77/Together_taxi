from django import forms
from .models import *


class BoardForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_content', 'route']


