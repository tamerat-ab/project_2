from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing , name="create_listing"),
    path("<int:id>/delete_listing", views.delete_listing, name="delete_listing"),
    path("<int:id>/add_to_list", views.add_to_list, name="add_to_list"),
    path("<int:id>/add_to_list", views.add_to_list, name="add_to_list"),
    path("<int:id>/update_bid", views.update_bid, name="update_bid"),
    path("<int:id>/update_bid", views.update_bid, name="update_bid"),
    path("<int:id>/close_bid", views.close_bid, name="close_bid"),
    path("<int:id>/comment", views.comment, name="comment"),
]
