from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Card

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password') 
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm



class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('title', 'description')



