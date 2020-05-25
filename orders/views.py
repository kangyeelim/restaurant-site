from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from decimal import *
from django.views.decorators.http import require_http_methods

from datetime import datetime
from .models import Pizza, Topping, CustomisedPizza, Order, SubmittedOrder, CustomisedSteak, Steak, Steakside, Pasta

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

def steaksides(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": 'Please sign in to order.'})
    steakSides = Steakside.objects.all()
    context = {
        "steakSides": steakSides
    }
    return render(request, "orders/steaksides.html", context)

def addsteak(request):
    size = request.POST["size"]
    quantity = int(request.POST["quantity"])
    choices = request.POST.getlist('choice[]')
    done = request.POST["done"]
    side_num = len(choices)
    steak_type = Steak.objects.all().filter(side_num=side_num).filter(size=size).get()

    for i in range(quantity):
        customisedSteak = CustomisedSteak()
        customisedSteak.steak_type = steak_type
        customisedSteak.order = Order.objects.get(id=request.session.get("order"))
        customisedSteak.done = done
        customisedSteak.save()
        for choice in choices:
            side = Steakside.objects.all().filter(side=choice).get()
            customisedSteak.sides.add(side)
        request.session.get("steaks").append(customisedSteak.id)
        return render(request, "orders/index.html")

"""
def addpasta(request, type):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": 'Please sign in to order.'})
    pasta = Pasta.objects.all().filter(type=type).get()
    pasta.order.add(Order.objects.get(id=request.session.get("order")))
    request.session.get("pastas").append(pasta.id)
    return render(request, "orders/index.html")
"""

def getsteakprice(request):
    if request.method == 'POST':
        side_num = request.POST.get("side_num")
        size = request.POST.get("size")
        steak = Steak.objects.all().filter(size=size).filter(side_num=side_num).get()
        return JsonResponse({'price':steak.price})

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

"""
def calculatePastaTotal(request):
    total = Decimal(0)
    for pasta_id in request.session.get("pastas"):
        pasta = Pasta.objects.get(id=pasta_id)
        total = total + pasta.price
    return total
"""

def getFoodsAndTotal(request):
    pizzas = []
    if request.session.get("pizzas") is None:
        initialiseSession(request) #quick fix to a bug that happens occassionally but need another feasible solution
    for customisedPizza_id in request.session.get("pizzas"):
        pizza = CustomisedPizza.objects.get(id=customisedPizza_id)
        pizzas.append(pizza)
    steaks = []
    for steak_id in request.session.get("steaks"):
        steak = CustomisedSteak.objects.get(id=steak_id)
        steaks.append(steak)
    """
    pastas = []
    for pasta_id in request.session.get('pastas'):
        pasta = Pasta.objects.get(id=pasta_id)
        pastas.append(pasta)
    """
    total = calculateTotal(request) + calculateSteakTotal(request) #+ calculatePastaTotal(request)
    context = {
        "pizzas": pizzas,
        "total": total,
        "steaks": steaks#,
        #"pastas": pastas
    }
    return context

def removePizza(request, id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    request.session.get("pizzas").remove(id)
    CustomisedPizza.objects.filter(id=id).delete()
    context = getFoodsAndTotal(request)
    return render(request, "orders/cart.html", context, {"message": "Removed from cart."})


def removesteak(request, id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    request.session.get("steaks").remove(id)
    CustomisedSteak.objects.filter(id=id).delete()
    context = getFoodsAndTotal(request)
    return render(request, "orders/cart.html", context, {"message": "Removed from cart."})

"""
def removePasta(request, id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None}) #done
    pasta = Pasta.objects.get(id=id)
    order_id = request.session.get("order")
    pasta.order.remove(Order.objects.get(id=order_id))
    request.session.get("pastas").remove(id)
    context = getFoodsAndTotal(request)
    return render(request, "orders/cart.html", context, {"message": "Removed from cart."})
"""

def submitorder(request):
    order = Order.objects.get(id=request.session.get("order"))
    order.order_time = datetime.now()
    order.bill = calculateTotal(request) + calculateSteakTotal(request) + calculatePastaTotal(request)
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
    request.session['steaks'] = []
    request.session['pastas'] = []

def calculateTotal(request):
    total = Decimal(0)
    for customisedPizza_id in request.session.get("pizzas"):
        pizza = CustomisedPizza.objects.get(id=customisedPizza_id)
        total = total + pizza.pizza_type.price
    return total

def calculateSteakTotal(request):
    total = Decimal(0)
    for steak_id in request.session.get("steaks"):
        steak = CustomisedSteak.objects.get(id=steak_id)
        total = total + steak.steak_type.price
    return total

def adminsite(request):
    return render(request, "orders/adminlogin.html", {"message": None})

def adminlogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if request.user.is_authenticated and request.user.is_superuser:
        submittedOrders = SubmittedOrder.objects.all()
        reverseOrder = []
        for order in submittedOrders:
            reverseOrder.append(order)
        reverseOrder.reverse()
        context = {
            "submittedOrders": reverseOrder
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
    reverseOrder = []
    for order in submittedOrders:
        reverseOrder.append(order)
    reverseOrder.reverse()
    context = {
        "submittedOrders": reverseOrder
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
        return JsonResponse({'price':pizza.price})

def location(request):
    return render(request, "orders/location.html")
