from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('catalog/', MainCatalog.as_view(), name='catalog'),
    path('payment/', payment, name='payment'),
    path('product/<slug:prod_slug>/', ShowProduct.as_view(), name='product'),
    path('product/<pk>/favorite/', login_required(FavoritesView.as_view()), name='favorite'),
    path('product/<pk>/cart/', login_required(CartView.as_view()), name='cart'),
    path('favorites/', login_required(FavoritesCatalog.as_view()), name='favorites'),
    path('cart/', login_required(CartPage.as_view()), name='cart_page'),
    path('exit/', views.LogoutView.as_view(), name='exit'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]
