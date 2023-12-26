from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django_htmx.http import retarget, HttpResponseLocation
from .models import User

def login_view(request):

    if request.method == "GET":
        form = LoginForm()
        template = u"account/login.html"
        if request.htmx:
            template = "account/partials/login.html"
        return render(request, template, {"form":form, "title":request.htmx})


    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd["email"], password=cd["password"])
            if user:
                login(request, user)

                # trigering a boosted redirect
                # return HttpResponseLocation(reverse('progress:projects_home'), target="#main")
                return redirect(reverse('progress:projects_home'))
           
            # if no user add error message 
            form.add_error(None, "Sorry. Incorrect Email or Password")
        
        response = render(request, "account/partials/login.html", {"form":form})
        return retarget(response, "#main")
    
def register_view(request):

    if request.method == "GET":
        form = RegisterForm()

        template = "account/register.html"
        if request.htmx:
            template = "account/partials/register.html"
        return render(request, template, {"form":form, "title":request.htmx})
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            # if no user with this email exists add error message 
            if User.objects.filter(email=cd["email"]).exists():
                form.add_error("email", "Sorry. There is a user registred with this email")

            else:
                user = User.objects.create_user(email=cd["email"], password=cd["password"], username=cd["username"])   
                login(request, user)

                # trigering a boosted redirect

                # return HttpResponseLocation(reverse('progress:projects_home'), target="#main")
                return redirect(reverse('progress:projects_home'))
            
        return render(request, "account/register.html", {"form":form})
        # return retarget(response, "#main")

def logout_view(request):
    logout(request)
    return redirect(reverse('progress:projects_home'))