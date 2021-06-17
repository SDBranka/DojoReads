from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        if len(postData['name']) < 2 or not NAME_REGEX.match(postData['name']):
            errors['name'] = "Please enter a valid name"
        if len(postData['alias']) < 2 or not NAME_REGEX.match(postData['alias']):
            errors['alias'] = "Please enter a valid alias"
        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        email_in_db = self.filter(email = postData['email'])        #ensure no duplicate email exists
        if email_in_db:
            errors["email"] = "This email already exists in the database"
        if len(postData['password']) < 8:
            errors["password"] = "Please enter a valid password"
        if not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['lemail']) < 2 or not EMAIL_REGEX.match(postData['lemail']):
            errors["email"] = "Please enter a valid email"
        if len(postData['lpassword']) < 8:
            errors["password"] = "Please enter a valid password"

        email_in_db = self.filter(email = postData['lemail'])
        if not email_in_db:
            errors['email'] = "This email is not registered"
        else:
            user = User.objects.get(email=postData["lemail"])
            pw_to_hash = postData["lpassword"]
            if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
                errors['email'] = "Incorrect password entered"
        return errors


class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters"
        book_in_db = self.filter(title = postData['title'])        #ensure no duplicate email exists
        if book_in_db:
            errors['title'] = "This book already exists in the database"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=198)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors = {}

        if len(postData['author_name']) < 2:
            errors['author_name'] = "Name must be at least 2 characters"
        author_in_db = Author.objects.filter(name=postData['author_name'])
        if len(author_in_db) >= 1:
            errors['duplicate'] = "Author already exists."
        return errors


class Author(models.Model):
    name = models.CharField(max_length=75)
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()


class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        if len(postData['content']) < 10:
            errors['content'] = "Please leave review of at least 10 characters"
        return errors


class Review(models.Model):
    reviewed_by = models.ForeignKey(
        User, 
        related_name="user_reviews",
        on_delete = models.CASCADE
    )
    book_reviewed = models.ForeignKey(
        Book, 
        related_name="book_reviews",
        on_delete = models.CASCADE
    )
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
