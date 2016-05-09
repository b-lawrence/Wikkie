from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Page, PageVersion


class PageForm(forms.ModelForm):

    class Meta:
        model = PageVersion
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
    slug = forms.SlugField(max_length=50,
                           widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Slug'})
                           )

    class Meta(PageForm.Meta):
        fields = ['slug', 'title', 'content']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        page_exists = Page.objects.filter(slug=slug).exists()
        if page_exists:
            raise forms.ValidationError("Page with this slug already exists!")
        return slug


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Desired username'}),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'Your email'}),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'})
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'username'}
                               ))
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'password'}
                               ))
