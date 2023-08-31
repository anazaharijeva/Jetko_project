"""Zadaca5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jetkoSilver.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('',jewellery, name="jewellery"),
                  path('jewellery/', jewellery, name="jewelries"),
                  path('jewellery_details/<int:jewellery_id>/', jewellery_details, name="jewellery_details"),
                  path('cart_items/', cart_items, name="cart_items"),
                  path('checkout/', checkout, name="checkout"),
                  path('final_site/', final_site, name="final_site"),
                  path('register/', register, name='register'),
                  path('login/', user_login, name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('item/delete/<int:item_id>/', delete_item, name='delete_item'),
                  path('item/add/', add_item, name='add_item'),
                  path('edit_item/<int:item_id>/', edit_item, name='edit_item'),
                  path('cart/item/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
