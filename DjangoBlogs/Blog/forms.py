from django import forms
from . models import BlogPost

class BlogPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))  # added mb-3 class here
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content']