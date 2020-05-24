from django.conf import settings
from django.db import models

# Create your models here.
class Topping(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"

class Pizza(models.Model):
    type = models.CharField(max_length=64)
    topping_num = models.IntegerField()
    size = models.CharField(max_length=2)
    price = price = models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    bill = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.bill}"

class CustomisedPizza(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizzas")

class SubmittedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default="Working on it")
