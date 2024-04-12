from django import forms
from .models import *


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Название поста'}
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': 'Описание поста'}
    ))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Slug поста'}
    ))
    comments_allowed = forms.BooleanField(label='Разрешить комментарии', required=False)

    class Meta:
        fields = ['title', 'content', 'slug', 'comments_allowed']
        model = Post


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Оставьте свой комментарий'}
    ))

    class Meta:
        fields = ['body']
        model = Comment
