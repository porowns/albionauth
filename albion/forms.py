from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from models import AlbionCharacter

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)

    def clean(self):
        input = self.cleaned_data

        if authenticate(username=input.get('username'),
         password=input.get('password')) is not None:
            pass
        else:
            self.add_error('username', 'Invalid credentials.')

        return input

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32)
    email = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    vpassword = forms.CharField(max_length=32)

    def clean(self):
        input = self.cleaned_data
        password = input.get('password')

        if User.objects.filter(username=input.get('username')).exists():
            self.add_error('username', "Username is taken.")
        if password:
            if input.get('password') != input.get('vpassword'):
                self.add_error('password', 'Passwords do not match.')
            if len(password) < 8:
                self.add_error('password', 'Password must be 8 characters or more.')

        return input
class CharacterForm(forms.Form):
    class_choices = (
            ("Tank", "Tank"),
            ("Ranged DPS", "Ranged DPS"),
            ("Melee DPS", "Melee DPS"),
            ("Healer", "Healer"),
            )
    name = forms.CharField(max_length=32, required=True)
    role = forms.CharField(widget=forms.Select(choices=class_choices), max_length=32, required=True)
    secondary = forms.CharField(widget=forms.Select(choices=class_choices), max_length=32, required=False)
    discord = forms.CharField(max_length=32, required=True, help_text="e.g @Porowns")

    def clean(self):
        if AlbionCharacter.objects.filter(discord=self.cleaned_data.get('discord')).count() > 0:
            if AlbionCharacter.objects.get(discord=self.cleaned_data.get('discord')).name != self.cleaned_data.get('name'):
                raise forms.ValidationError(
                        "Discord name taken."
                        )
