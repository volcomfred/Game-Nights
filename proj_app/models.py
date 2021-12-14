import datetime
from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"

        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characers long"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(postData['password']) < 8:
            errors['password'] = "An eight character password must be entered"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['mismatch'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class GameManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['game']) == 0:
            errors["game"] = "no empty entries"
        if len(postData['location']) == 0:
            errors["location"] = "no empty entries"
        
        return errors

class Game(models.Model):
    game = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    creator = models.ForeignKey(User, related_name="made_game", on_delete=models.CASCADE)
    joined = models.ManyToManyField(User, related_name="joined_game")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GameManager()
