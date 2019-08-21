from django import forms

from files.models import FileHolder, UrlHolder


class FileHolderCreateForm(forms.ModelForm):
    class Meta:
        model = FileHolder
        fields = ['password', 'file']


class UrlHolderCreateForm(forms.ModelForm):
    class Meta:
        model = UrlHolder
        fields = ['password', 'url']
