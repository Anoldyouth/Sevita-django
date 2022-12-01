from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    slug = models.SlugField(max_length=64, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(verbose_name='Описание')

    preview = models.ImageField(upload_to=f"images/preview/", verbose_name='Главное фото')
    on_hover = models.ImageField(upload_to=f"images/on_hover/", verbose_name='Фото при наведении')
    additional = models.ImageField(upload_to=f"images/additional/", verbose_name='Дополнительное фото', blank=True)

    low_price = models.CharField(max_length=32, default='', verbose_name='Цена за 2,5 мл')
    medium_price = models.CharField(max_length=32, default='', verbose_name='Цена за 5 мл')
    high_price = models.CharField(max_length=32, default='', verbose_name='Цена за 10 мл')

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Каталог'
        ordering = ['-time_create', 'title']


class Favorites(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    obj = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return f'Парфюм "{self.obj}" в избранном пользователя {self.user}'

    class Meta:
        db_table = "favorites"
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    obj = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return f'Парфюм "{self.obj}" в корзине пользователя {self.user}'

    class Meta:
        db_table = "cart"
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
