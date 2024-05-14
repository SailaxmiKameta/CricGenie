# forms.py
from django import forms
from .models import PlayerForm

class PlayerSearchForm(forms.ModelForm):
    class Meta:
        model = PlayerForm
        fields = ['player_name']