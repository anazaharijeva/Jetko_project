from django.contrib import admin
from django.http.request import HttpRequest

from . import models


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ["email", "user"]
    search_fields = ["user__username", "user__email"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_change_permission(
            self, request: HttpRequest, obj: models.UserInformation | None = None
    ) -> bool:
        return (
                (obj is not None and obj.user == request.user)
                or request.user.is_staff
                or request.user.is_superuser
        )

    def has_delete_permission(
            self, request: HttpRequest, obj: models.UserInformation | None = None
    ) -> bool:
        return self.has_change_permission(request, obj)

    def has_view_permission(
            self, request: HttpRequest, _: models.UserInformation | None = None
    ) -> bool:
        return request.user.is_authenticated


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['color', 'jewelry_type', 'material', ]
    search_fields = ['name', 'description']

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_change_permission(
            self, request: HttpRequest, _: models.Product | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_delete_permission(
            self, request: HttpRequest, _: models.Product | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_view_permission(
            self, request: HttpRequest, _: models.Product | None = None
    ) -> bool:
        return request.user.is_authenticated


class CartAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_change_permission(
            self, request: HttpRequest, _: models.Cart | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_delete_permission(
            self, request: HttpRequest, _: models.Cart | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_view_permission(
            self, request: HttpRequest, _: models.Cart | None = None
    ) -> bool:
        return request.user.is_authenticated


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
    search_fields = ["cart__user__username", "product__name"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_change_permission(
            self, request: HttpRequest, _: models.CartItem | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_delete_permission(
            self, request: HttpRequest, _: models.CartItem | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_view_permission(
            self, request: HttpRequest, _: models.CartItem | None = None
    ) -> bool:
        return request.user.is_authenticated


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username", "products__name"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_change_permission(
            self, request: HttpRequest, _: models.Order | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_delete_permission(
            self, request: HttpRequest, _: models.Order | None = None
    ) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_view_permission(
            self, request: HttpRequest, _: models.Order | None = None
    ) -> bool:
        return request.user.is_authenticated


admin.site.register(models.UserInformation, UserInformationAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Order, OrderAdmin)
