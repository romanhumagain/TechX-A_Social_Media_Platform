from django import forms
from . models import BlogPost

class BlogPostForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
  class Meta:
    model = BlogPost
    fields = ['title' , 'content']