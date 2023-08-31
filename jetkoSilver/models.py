from django.contrib.auth.models import User
from django.db import models


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    class Meta:
        verbose_name_plural = "User's information"

    def __str__(self) -> str:
        return f"({self.user!r})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    material = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    jewelry_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product informations"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} ({self.quantity}) in Cart"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=50)
    city_postal = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    pay_with_card = models.BooleanField(default=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"

    def calculate_total_amount(self):
        total = 0
        cart_items = self.cart.items.all()
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        return total

