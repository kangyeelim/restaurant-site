from django.contrib import admin

from .models import Topping, Pizza, CustomisedPizza, Order, SubmittedOrder
# Register your models here.

class CustomisedPizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ("toppings",)

class CustomisedPizzaInline(admin.TabularInline):
    model = CustomisedPizza

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        CustomisedPizzaInline,
    ]

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(CustomisedPizza, CustomisedPizzaAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SubmittedOrder)
