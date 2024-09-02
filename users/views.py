from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


class LoginPageView(View):
    def get(self,request):
        return render(request, "users/login.html")
    
    def post(self,request):
        user_form = AuthenticationForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            login(request,user)
            return redirect("library")
        return redirect("login")



class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect("home")