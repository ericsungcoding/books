from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, "books/index.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/")
    user = User.objects.get(email=request.POST["email"])
    request.session["user_id"] = user.id
    return redirect("/books")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/")
    user = User.objects.create(
        first_name = request.POST["first_name"],
        last_name = request.POST["last_name"],
        email = request.POST["email"],
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    )
    request.session["user_id"] = user.id
    return redirect("/books")

def logout(request):
    request.session.flush()
    return redirect("/")

def books(request):
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "all_books": Book.objects.all()
    }
    return render(request, "books/books.html", context)

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/books")
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.create(
        title = request.POST["title"],
        desc = request.POST["desc"],
        uploader = user
    )
    user.liked_books.add(book)
    return redirect("/books")

def book(request, book_id):
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "book": Book.objects.get(id=book_id)
    }
    return render(request, "books/book.html", context)

def update(request, book_id):
    errors = Book.objects.book_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect(f"/books/{book_id}")
    book = Book.objects.get(id=book_id)
    book.title = request.POST["title"]
    book.desc = request.POST["desc"]
    book.save()
    return redirect(f"/books/{book_id}")

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("/books")

def like(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    book.users_who_like.add(user)
    return redirect(f"/books/{book_id}")

def unlike(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    book.users_who_like.remove(user)
    return redirect(f"/books/{book_id}")