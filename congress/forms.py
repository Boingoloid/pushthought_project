from django import forms

from . import models


class CongressForm(forms.ModelForm):
    class Meta:
        model = models.Congress
        fields = '__all__'
