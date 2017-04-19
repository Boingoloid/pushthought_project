from django import forms

from . import models


class ProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = ['title', "plot_outline", 'image', 'runtime', 'type', 'imdb_id']


# class SeasonForm(forms.ModelForm):
#     class Meta:
#         model = models.Season
#         fields = ['program', 'number']
#
#
# class EpisodeForm(forms.ModelForm):
#     class Meta:
#         model = models.Episode
#
#
# class SegmentForm(forms.ModelForm):
#     class Meta:
#         model = models.Segment