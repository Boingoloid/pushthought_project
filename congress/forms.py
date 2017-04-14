from django import forms

from . import models


class ZipForm(forms.ModelForm):
    class Meta:
        model = models.Zip
        fields = ['code']


class CongressForm(forms.ModelForm):
    class Meta:
        model = models.Congress
        fields = '__all__'