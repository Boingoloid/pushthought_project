
from django import forms
# from pushthought.models import Segment, MenuItem, UserProfile
from django.contrib.auth.models import User

# class SegmentForm(forms.ModelForm):
#     # name = forms.CharField(max_length=128, help_text="Please enter the category name.")
#     # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#
#     # An inline class to provide additional information on the form.
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Segment
#         fields = '__all__'
#
# class MenuForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = MenuItem
#
#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values, so we may not want to include them...
#         # Here, we are hiding the foreign key.
#         fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website', 'picture')