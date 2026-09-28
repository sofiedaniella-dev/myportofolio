import datetime
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Education, Experience, Project
from main.forms import ProjectForm, ExperienceForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied


# Helper function untuk mengecek peran Editor
def is_editor(user):
    return user.is_authenticated and user.groups.filter(name='Editor').exists()


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Sofie Daniella<br> Ang",
        "npm": "2506619562",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia interested "
            "in Product Management, Business Strategy, and Digital Innovation."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_education(request):
    education_list = Education.objects.all()
    context = {
        'name': 'Sofie Daniella Ang',
        'education_list': education_list,
    }
    return render(request, "education.html", context)


def show_experience(request):
    experience_list = Experience.objects.all()
    context = {
        'name': 'Sofie Daniella Ang',
        'experience_list': experience_list,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {"form": form}
    return render(request, "experience_form.html", context)


def update_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {"form": form}
    return render(request, "experience_form.html", context)


def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")


def get_experience_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# SHOW PROJECTS (Dapat dibaca oleh siapapun)
def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Sofie Daniella Ang",
        "projects": projects,  
        "title_query": title_query,
        "is_editor": is_editor(request.user), # Dikirim ke template untuk pengondisian tombol edit
    }
    return render(request, "projects.html", context)


# CREATE PROJECT (Hanya Superuser / Pemilik Portofolio)
@login_required(login_url="/login/")  
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied  # Menghasilkan HTTP 403 Forbidden
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Sofie Daniella Ang",
        "form": form,
    }
    return render(request, "projects_form.html", context)


# UPDATE PROJECT (Bisa diakses Superuser DAN Editor)
@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied  # Menghasilkan HTTP 403 Forbidden

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Sofie Daniella Ang",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


# DELETE PROJECT (Hanya Superuser / Pemilik Portofolio)
@login_required(login_url="/login/")  
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied  # Menghasilkan HTTP 403 Forbidden
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


# GET PROJECTS JSON (Dapat diakses siapapun)
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


# TOGGLE STAR (Bisa untuk Pengguna Biasa, Editor, Superuser / Wajib Login)
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Sofie Daniella Ang",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
      
    context = {
        "name": "Sofie Daniella Ang",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response