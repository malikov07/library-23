from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.LoginPageView.as_view(), name="login"),
    path("logout/",views.LogOutView.as_view(), name="logout"),
]