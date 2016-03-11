from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())