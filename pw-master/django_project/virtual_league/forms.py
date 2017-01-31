from django import forms

class NewGame(forms.Form):
    name = forms.CharField(required=True)
    key = forms.CharField(required=True)
