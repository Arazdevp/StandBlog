# forms.py
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={
                'style': 'background-color: #fff;border: 1px solid #ced4da;border-radius: 0.25rem;padding: 0.375rem;font-size: 1rem;min-height: 150px;width: 100%;color: #495057;',
                "class": "form-control",}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }