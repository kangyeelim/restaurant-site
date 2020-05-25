from django.contrib import admin

from .models import Topping, Pizza, CustomisedPizza, Order, SubmittedOrder, CustomisedSteak, Steak, Steakside, Pasta
# Register your models here.

class CustomisedPizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ("toppings",)

class CustomisedPizzaInline(admin.TabularInline):
    model = CustomisedPizza

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        CustomisedPizzaInline,
    ]
    filter_horizontal = ("pastas",)

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(CustomisedPizza, CustomisedPizzaAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SubmittedOrder)
admin.site.register(CustomisedSteak)
admin.site.register(Steak)
admin.site.register(Steakside)
admin.site.register(Pasta)
