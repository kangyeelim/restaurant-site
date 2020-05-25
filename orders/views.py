from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from decimal import *
from django.views.decorators.http import require_http_methods

from datetime import datetime
from .models import Pizza, Topping, CustomisedPizza, Order, SubmittedOrder

# Create your views here.

def index(request):
    return render(request, "orders/index.html")

def alltoppings(request, type):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": 'Please sign in to order.'})
    pizzas = Pizza.objects.all()
    context = {
        "type": type,
        "pizzas": pizzas
    }
    return render(request, "orders/alltoppings.html", context)

def addpizza(request, type):
    size = request.POST["size"]
    quantity = int(request.POST["quantity"])
    choices = request.POST.getlist('choice[]')
    topping_num = len(choices)
    pizza_type = Pizza.objects.all().filter(type=type).filter(topping_num=topping_num).filter(size=size).get()

    for i in range(quantity):
        customisedPizza = CustomisedPizza()
        customisedPizza.pizza_type = pizza_type
        customisedPizza.order = Order.objects.get(id=request.session.get("order"))
        customisedPizza.save()
        for choice in choices:
            topping = Topping.objects.all().filter(topping=choice).get()
            customisedPizza.toppings.add(topping)
        request.session.get("pizzas").append(customisedPizza.id)
        #request.session.modified = True
        return render(request, "orders/index.html")

def signin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        initialiseSession(request)
        return HttpResponseRedirect(reverse("account")) #done
    else:
        return render(request, "orders/login.html", {"message": 'Incorrect credentials entered.'}) #done

def signout(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."}) #done

def signup_view(request):
    return render(request, "orders/signup.html")

def signup(request):
    try:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(request, username=username, password=password)
        initialiseSession(request)
        return HttpResponseRedirect(reverse("account")) #done
    except:
        return render(request, "orders/signup.html", {"message": "Username or Email already used."})

def account(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    orders = Order.objects.all().filter(customer=request.user)
    submittedOrders = []

    for order in orders:
        submittedorder = SubmittedOrder.objects.filter(order=order)
        if len(submittedorder) == 0:
            continue
        else:
            submittedOrders.append(submittedorder[0])
    submittedOrders.reverse()
    context = {
        "username": request.user.username,
        "email": request.user.email,
        "submittedOrders": submittedOrders
    }
    return render(request, "orders/account.html", context) #done

def orderdetails(request, id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    order = Order.objects.all().get(id=id)
    context = {
        "order": order
    }
    return render(request, "orders/orderdetails.html", context)

def cart(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done

    context = getFoodsAndTotal(request)
    return render(request, "orders/cart.html", context, {"message": None})

def getFoodsAndTotal(request):
    pizzas = []
    if request.session.get("pizzas") is None:
        initialiseSession(request) #quick fix to a bug that happens occassionally but need another feasible solution
    for customisedPizza_id in request.session.get("pizzas"):
        pizza = CustomisedPizza.objects.get(id=customisedPizza_id)
        pizzas.append(pizza)
    total = calculateTotal(request)
    context = {
        "pizzas": pizzas,
        "total": total
    }
    return context

def removePizza(request, id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    request.session.get("pizzas").remove(id)
    CustomisedPizza.objects.filter(id=id).delete()
    context = getFoodsAndTotal(request)
    return render(request, "orders/cart.html", context, {"message": "Removed from cart."})


def submitorder(request):
    order = Order.objects.get(id=request.session.get("order"))
    order.order_time = datetime.now()
    order.bill = calculateTotal(request)
    order.save()
    submittedOrder = SubmittedOrder(order = order)
    submittedOrder.save()
    initialiseSession(request)
    return HttpResponseRedirect(reverse("account"))

def initialiseSession(request):
    order = Order()
    order.customer = request.user
    order.save()
    request.session['order'] = order.id
    request.session['pizzas'] = []

def calculateTotal(request):
    total = Decimal(0)
    for customisedPizza_id in request.session.get("pizzas"):
        pizza = CustomisedPizza.objects.get(id=customisedPizza_id)
        total = total + pizza.pizza_type.price
    return total

def adminsite(request):
    return render(request, "orders/adminlogin.html", {"message": None})

def adminlogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if request.user.is_authenticated and request.user.is_superuser:
        submittedOrders = SubmittedOrder.objects.all()
        context = {
            "submittedOrders": submittedOrders
        }
        return render(request, "orders/adminview.html", context)
    else:
        return render(request, "orders/adminlogin.html", {"message": "Incorrect credentials."})

@require_http_methods(["POST"])
def updateStatus(request, id):
    status = request.POST["status"]
    submittedOrder = SubmittedOrder.objects.get(id=id)
    submittedOrder.status = status
    submittedOrder.save(update_fields=['status'])
    submittedOrders = SubmittedOrder.objects.all()
    context = {
        "submittedOrders": submittedOrders
    }
    return render(request, "orders/adminview.html", context)

def adminsignout(request):
    return render(request, "orders/adminlogin.html", {"message": "Logged out."})

def getprice(request):
    if request.method == 'POST':
        topping_num = request.POST.get("topping_num")
        size = request.POST.get("size")
        type = request.POST.get("type")
        pizza = Pizza.objects.all().filter(size=size).filter(type=type).filter(topping_num=topping_num).get()
        #data = serializers.serialize('json', pizza.price)
        #return HttpResponse(data, content_type='application/json')
        return JsonResponse({'price':pizza.price})
