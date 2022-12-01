from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

CHOICES = (
    ("0", '2.5 мл'),
    ("1", '5 мл'),
    ("2", '10 мл')
)


class FeedBack(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Выберите парфюм", initial=0,
                                     widget=forms.Select(attrs={'class': "form__select"}))
    volume = forms.ChoiceField(choices=CHOICES, label="Выберите объём",
                               widget=forms.Select(attrs={'class': "form__select"}))
    contacts = forms.EmailField(label='Оставьте e-mail для связи:',
                                widget=forms.EmailInput(attrs={'class': "form__text",
                                                               'placeholder': 'your-email@email.ru'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Поле необязательно', 'class': 'form__text'}),
        label="Оставьте свои пожелания",
        required=False)


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']
