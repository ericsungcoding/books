from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData["email"])
        if not user:
            errors["login"] = "Account does not exist"
        else:
            if not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
                errors["password"] = "Invalid email or password"
        return errors
    def register_validator(self, postData):
        errors = {}
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "First name must be at least 1 character"
        if len(postData["last_name"]) < 1:
            errors["last_name"] = "Last name must be at least 1 character"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData["email"]):
            errors["regex"] = "Invalid email format"
        user = User.objects.filter(email=postData["email"])
        if user:
            errors["duplicate"] = "An account with this email already exists"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData["password"] != postData["password_conf"]:
            errors["match"] = "Passwords must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 1:
            errors["title"] = "Title is required"
        if len(postData["desc"]) < 5:
            errors["desc"] = "Description must be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploader = models.ForeignKey(User, related_name="uploaded_books", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()