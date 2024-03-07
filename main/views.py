from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .models import User
from .forms import RegistrationForm
from .forms import UserAuthenticationForm
from django.contrib import messages
from django.utils.translation import activate
from django.conf import settings
from .models import Translation
from django.utils.translation import activate

def getHome(request):
    return render(request, 'home.html')


def registerView(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            
            messages.info(request, 'Account in review')

            return redirect("/")
        else:
            context['registration_form'] = form

    return render(request, 'register.html', context)


def login_view(request, *args, **kwargs):

    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    destination = get_redirect_if_exists(request)
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context["login_form"] = form

    return render(request, 'login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))


def logout_view(request):
    logout(request)
    return redirect("home")


def set_local_language(request):
    language = request.POST.get('language', 'fr')

    activate(language)
    
    request.session['django_language'] = language

    return HttpResponse('Language set successfully.')


def my_profile_view(request):
    return render(request, 'my-profile.html')


def aboutUs(request):
    return render(request, 'about-us.html')

def customerSupport(request):
    return render(request, 'customer-support.html')

def privacyPolicy(request):
    return render(request, 'privacy-policy.html')


def userAgreement(request):
    return render(request, 'user-agreement.html')
