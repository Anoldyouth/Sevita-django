import json

from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *
from .telegram import send_contacts


class MainHome(DataMixin, ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="SEVITA exclusive", page="home")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Функция выводит только те объекты из базы данных, которые отмечены, как видимые и, так как это неполный каталог
        (каталог главной страницы), то устанавливает ограничение на количество выводимых объектов (count).
        """
        count = 8
        return Product.objects.filter(is_visible=True, pk__gte=Product.objects.count() - count + 1)


class MainCatalog(DataMixin, ListView):
    paginate_by = 12
    model = Product
    template_name = "main/catalog.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Каталог", page="catalog")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(is_visible=True)


def payment(request):
    return HttpResponse('payment')


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'main/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['prod'], page="product", form=self.get_form(self.request))

        return dict(list(context.items()) + list(c_def.items()))

    # Сделать класс представления для этой формы и через {% include %} её подключить
    def get_form(self, request):
        if request.method == 'POST':
            form = FeedBack(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                message_to_send = f"Товар: {data['product']}\nОбъём флакончика: {CHOICES[int(data['volume'])][1]}\n" \
                                  f"E-mail: {data['contacts']}\n"

                if data['description']:
                    message_to_send += f"Сообщение от отправителя: {data['description']}"
                try:
                    send_contacts(message_to_send)
                    return redirect('home')
                except:
                    form.add_error(None, "Ошибка отправки формы. Попробуйте позднее.")
        else:
            form = FeedBack()

        return form


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация", page="register", form=self.reg(self.request))

        return dict(list(context.items()) + list(c_def.items()))

    def reg(self, request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])

                new_user.save()
                return redirect('home')
        else:
            user_form = UserRegistrationForm()

        return user_form


# Добавление (удаление) в избранное
class FavoritesView(View):
    # В данную переменную будет устанавливаться модель избранного, которую необходимо обработать
    model = Favorites

    def post(self, request, pk):
        user = auth.get_user(request)

        # Пытаемся получить избранное из таблицы, или создать новую
        favorite, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        # Если новый товар не добавлен в избранное, значит, он там уже есть, следовательно,
        # клик по этому товару будем считать запросом на удаление его из избранного
        if not created:
            favorite.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
            }),
            content_type="application/json"
        )


# Добавление (удаление) в избранное
class CartView(View):
    # В данную переменную будет устанавливаться модель избранного, которую необходимо обработать
    model = Cart

    def post(self, request, pk):
        user = auth.get_user(request)

        # Пытаемся получить избранное из таблицы, или создать новую
        cart_item, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        # Если новый товар не добавлен в избранное, значит, он там уже есть, следовательно,
        # клик по этому товару будем считать запросом на удаление его из избранного
        if not created:
            cart_item.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
            }),
            content_type="application/json"
        )


class FavoritesCatalog(DataMixin, ListView):
    paginate_by = 12
    model = Product
    template_name = "main/favorites.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Избранные", page="favorites")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # Получаем текущего пользователя
        user = auth.get_user(self.request)

        # Получаем pk всех избранных
        fav_id = [i.obj.pk for i in Favorites.objects.filter(user=user)]
        return Product.objects.filter(pk__in=fav_id)


class CartPage(DataMixin, ListView):
    paginate_by = 12
    model = Product
    template_name = "main/cart.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Корзина", page="cart_page")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # Получаем текущего пользователя
        user = auth.get_user(self.request)

        # Получаем pk всех избранных
        cart_id = [i.obj.pk for i in Cart.objects.filter(user=user)]
        return Product.objects.filter(pk__in=cart_id)
