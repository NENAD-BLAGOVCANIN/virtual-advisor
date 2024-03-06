from .views import getHome, login_view, registerView, logout_view, set_local_language, my_profile_view
from django.urls import path

urlpatterns = [

    path("", getHome, name='home'),
    path("login", login_view, name='login'),
    path("register", registerView, name='register'),
    path("logout", logout_view, name='logout'),
    path("my-profile", my_profile_view, name='my_profile'),
    path('set_local_language/', set_local_language, name='set_local_language'),

]