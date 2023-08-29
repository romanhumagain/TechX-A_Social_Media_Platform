from django import forms
from . models import BlogPost

class BlogPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))
    image = forms.ImageField(required=False)
    class Meta:
        model = BlogPost
        fields = ['title', 'content' , 'image']
