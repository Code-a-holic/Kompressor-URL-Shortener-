from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("landing_page", views.landing_page, name="landing_page"),
    path("signup", views.signup, name="signup"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("logout", views.logout, name="logout"),
    path("delete_urls", views.delete_multiple, name="delete_urls"),
    path("<str:hash_value>", views.re_routing, name="re_routing")
]