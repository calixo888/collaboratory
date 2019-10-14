from django.db import models
from django.contrib.auth.models import User

class LoginModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    projects = models.CharField(max_length=1000000, default="", blank=True)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    project_id = models.CharField(max_length=10)
    project_name = models.CharField(max_length=20)
    project_description = models.CharField(max_length=50, default="", blank=True)
    members = models.CharField(max_length=1000000, default="", blank=True)

    def __str__(self):
        return self.project_name

class ToDoListItem(models.Model):
    project_id = models.CharField(max_length=10)
    item_name = models.CharField(max_length=20)
    item_description = models.CharField(max_length=20)
    assigned_to = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.item_name
