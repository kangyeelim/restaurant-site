from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<type>/alltoppings", views.alltoppings, name="alltoppings"),
    path("<type>/addpizza", views.addpizza, name="addpizza"),
    path("signupinput", views.signup, name="signup"),
    path("login", views.signin, name="login"),
    path("signup", views.signup_view, name="signup_view"),
    path("account", views.account, name="account"),
    path("logout", views.signout, name="logout"),
    path("cart", views.cart, name="cart"),
    path("submitorder", views.submitorder, name="submitorder"),
    path("adminsite", views.adminsite, name="adminsite"),
    path("adminview", views.adminlogin, name="adminlogin"),
    path("<int:id>/orderdetails", views.orderdetails, name="orderdetails"),
    path("<int:id>/removePizza", views.removePizza, name="removePizza"),
    path("<int:id>/updatestatus", views.updateStatus, name="updateStatus"),
    path("adminsignout", views.adminsignout, name="adminsignout"),
    path("getprice", views.getprice, name="getprice"),
    path("steaksides", views.steaksides, name="steaksides"),
    path("addsteak", views.addsteak, name="addsteak"),
    path('getsteakprice', views.getsteakprice, name="getsteakprice"),
    path("<int:id>/removesteak", views.removesteak, name="removeSteak"),
    path("location", views.location, name="location"),
    #path("<type>/addpasta", views.addpasta, name="addpasta"),
    #path("<int:id>/removepasta", views.removePasta, name="removepasta")
]
