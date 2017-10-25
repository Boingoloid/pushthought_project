from django import forms
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('zip', )

    def clean_zip(self):
        zip_str = self.cleaned_data['zip']
        try:
            assert len(zip_str) == 5
            int(zip_str)
        except (AssertionError, ValueError):
            raise forms.ValidationError(
                "ZIP should consist of 5 digits")
        return zip_str
