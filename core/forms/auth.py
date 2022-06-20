from django import forms
from django.contrib.auth.models import User


class SetUserForm(forms.Form):
    username =  forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).first():
            self.add_error('username', "This username is taken!")
            # raise forms.ValidationError("This username is taken!")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")