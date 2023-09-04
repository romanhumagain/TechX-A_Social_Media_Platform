from django import forms
from . models import BlogPost


class BlogPostForm(forms.ModelForm):
    title = forms.CharField(
        label="Title of the Post",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'style':'text-transform: capitalize'
                                      }))
    
    content = forms.CharField(
        label="Post Content",
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))
    image = forms.ImageField(required=False)
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content' , 'image']
