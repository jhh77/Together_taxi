from django import forms
from .models import *

#게시글 생성 폼
class BoardForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_content', 'route']


#댓글 생성 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']