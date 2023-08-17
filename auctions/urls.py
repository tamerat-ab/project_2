from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing , name="create_listing"),
    path("<int:id>/delete_listing", views.delete_listing, name="delete_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/update_bid", views.update_bid, name="update_bid"),
    path("<int:id>/close_bid", views.close_bid, name="close_bid"),
    path("<int:id>/comment", views.comment, name="comment"),
    path("<int:id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("category", views.category, name="category"),
    path("list_form", views.list_form, name="list_form"),
    path("<int:id>/listing_page", views.listing_page, name="listing_page"),

]
