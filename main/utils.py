from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

from .forms import UserRegistrationForm

header = [{'title': "О нас", 'url_name': 'home'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['header'] = header
        context['login_form'] = AuthenticationForm()
        context['registration_form'] = UserRegistrationForm()

        return context
