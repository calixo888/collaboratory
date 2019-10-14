from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
import json
import random
import string
import os
import subprocess

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def index(request):
    if request.user.username:
        profile = models.UserProfile.objects.filter(user=request.user)[0]
        text_projects = profile.projects.split()
        projects = []
        for i in text_projects:
            try:
                projects.append(models.Project.objects.get(project_id=i))
            except:
                pass
    else:
        projects = None
    return render(request, 'collaborator_app/index.html', context={"projects": projects})

def user_login(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            print(user)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    login_form.add_error("username", "Account now inactive. Please register again.")
            else:
                login_form.add_error("username", "Username or password incorrect. Please try again.")

    else:
        login_form = forms.LoginForm()

    return render(request, "collaborator_app/login.html", context={"form": login_form})

def register(request):
    if request.method == "POST":
        user_form = forms.RegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = models.UserProfile(user=user)
            profile.save()

            login(request, user)
            return HttpResponseRedirect("/")

    else:
        user_form = forms.RegisterForm()

    context_dict = {
        "user_form": user_form,
    }

    return render(request, "collaborator_app/register.html", context=context_dict)

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def project(request, project_id):
    projects = models.Project.objects.filter(project_id=project_id)

    if projects:
        project = projects[0]
        files = [file for file in os.listdir(settings.MEDIA_ROOT + "/" + project.project_id)]
        items = models.ToDoListItem.objects.filter(project_id=project.project_id)

        profile = models.UserProfile.objects.filter(user=request.user)[0]
        profile_projects = profile.projects.split()

        if request.method == "POST" and request.POST.get("item_name", False):
            data = request.POST.dict()
            item_name = data.get("item_name")
            item_description = data.get("item_description")
            assigned_to = data.get("assigned_to")
            due_date = data.get("due_date")
            item = models.ToDoListItem(project_id=project.project_id, item_name=item_name, item_description=item_description,
                                        assigned_to=assigned_to, due_date=due_date)
            item.save()

        try:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(project.project_id + "/" + myfile.name, myfile)
        except:
            pass

        if project.project_id in profile_projects:
            return render(request, "collaborator_app/project.html", context={"project_name": project.project_name, "project_description": project.project_description, "members": project.members.split(), "url": settings.MEDIA_URL, "files": files, "items": items, "id": project_id, 'room_name_json': mark_safe(json.dumps(project_id))})
        else:
            return HttpResponse("<h1>You do not have permission to view this project.</h1>")
    else:
        return HttpResponse("<h1>Invalid project ID</h1>")

@login_required(login_url="/login/")
def create_project(request):
    if request.method == "POST":
        data = request.POST.dict()
        name = data.get("name")
        description = data.get("description")
        members = []
        counter = 0
        while True:
            if data.get("member" + str(counter)):
                members.append(data.get("member" + str(counter)))
                counter += 1
            else:
                break

        valid = True
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        profiles = []
        for member in members:
            user = User.objects.filter(username=member)
            if user:
                profile = models.UserProfile.objects.filter(user=user[0])[0]
                profiles.append(profile)
            else:
                messages.info(request, member + " is not a recognized user. That user has not been added to your project.")
                valid = False

        if valid:
            for profile in profiles:
                profile.projects = profile.projects + str(code) + " "
                profile.save()

            fs = FileSystemStorage()
            filename = fs.save(code + "/" + "test.txt", open("test.txt", "r"))

            project = models.Project(project_id=code, project_name=name, project_description=description, members=" ".join([i.user.username for i in profiles]))
            project.save()

            return render(request, "collaborator_app/create_project.html", context={"code": code, "link": "/project/" + code, "created": True})

    return render(request, "collaborator_app/create_project.html", context={"created": False})
