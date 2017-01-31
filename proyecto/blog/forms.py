from django import forms

class loginForm(forms.Form):
    user_name = forms.CharField(maxlength=50);
    user_pass = forms.CharField(maxlength=50);
