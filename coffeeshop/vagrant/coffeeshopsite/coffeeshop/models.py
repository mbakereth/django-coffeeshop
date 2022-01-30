from django.db import models
from django_countries.fields import CountryField
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, default="", null=True,
                                blank=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    postcode = models.CharField(max_length=16)
    country = CountryField()

    def __str__(self):
        return self.address1[:min(20, len(self.address1))] + "..."


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)
    expire_month = models.IntegerField(default=1,
                                       validators=[MinValueValidator(1),
                                                   MaxValueValidator(12)])
    expire_year = models.IntegerField(default=20,
                                      validators=[MinValueValidator(20),
                                                  MaxValueValidator(99)])
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return "*-" + self.number[-4:]


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    unit_price = models.FloatField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total(self):
        ret = 0.0
        for item in self.cartitem_set.all():
            ret += item.subtotal()
        return ret

    def __str__(self):
        return self.user.first_name + ":" + str(self.pk)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(0)])

    def subtotal(self):
        return self.quantity * self.product.unit_price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()

    def total(self):
        ret = 0.0
        for item in self.orderitem_set.all():
            ret += item.subtotal()
        return ret


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(0)])

    def subtotal(self):
        return self.quantity * self.product.unit_price


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    comment = models.TextField()


class StockLevel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=1,
                                             validators=[MinValueValidator(0)])
