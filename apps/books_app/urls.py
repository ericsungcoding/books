from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("register", views.register),
    path("logout", views.logout),
    path("books", views.books),
    path("books/add", views.add_book),
    path("books/<int:book_id>", views.book),
    path("books/<int:book_id>/update", views.update),
    path("books/<int:book_id>/delete", views.delete),
    path("books/<int:book_id>/like", views.like),
    path("books/<int:book_id>/unlike", views.unlike),
]