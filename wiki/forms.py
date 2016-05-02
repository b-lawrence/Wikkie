from django import forms
from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'content']
        widgets = {
                  'title': forms.TextInput(attrs={'class': 'form-control'}),
                  'content': forms.Textarea(attrs={
                                            'cols': 80,
                                            'rows': 20,
                                            'class': 'form-control'})}
