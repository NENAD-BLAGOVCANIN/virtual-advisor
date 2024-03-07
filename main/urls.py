from .views import getHome, login_view, registerView, logout_view, set_local_language, my_profile_view, aboutUs, customerSupport, privacyPolicy, userAgreement
from django.urls import path

urlpatterns = [

    path("", getHome, name='home'),
    path("login", login_view, name='login'),
    path("register", registerView, name='register'),
    path("about-us", aboutUs, name='about_us'),
    path("customer-support", customerSupport, name='customer_support'),
    path("privacy-policy", privacyPolicy, name='privacy_policy'),
    path("user-agreement", userAgreement, name='user_agreement'),
    path("logout", logout_view, name='logout'),
    path("my-profile", my_profile_view, name='my_profile'),
    path('set_local_language/', set_local_language, name='set_local_language'),

]