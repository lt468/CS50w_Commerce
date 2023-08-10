from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view_listing/item_<int:item_id>", views.view_listing, name="view_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
