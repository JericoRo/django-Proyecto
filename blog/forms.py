from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields =['tittle', 'description', 'important']
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write a title' }),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            }