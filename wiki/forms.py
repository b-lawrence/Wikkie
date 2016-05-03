from django import forms
from django.contrib.auth.models import User
from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Page title'}),
            'content': forms.Textarea(attrs={
                'cols': 80,
                'rows': 20,
                'class': 'form-control',
                'placeholder': 'Content goes here ...'})
            }


class NewPageForm(PageForm):

    class Meta(PageForm.Meta):
        fields = ['slug', 'title', 'content']
        widgets = {
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Page title'}),
            'content': forms.Textarea(attrs={
                'cols': 80,
                'rows': 20,
                'class': 'form-control',
                'placeholder': 'Content goes here ...'})
            }


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
