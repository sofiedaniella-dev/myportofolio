from django.shortcuts import render, redirect, get_object_or_404
from main.models import Education
from main.models import Experience, Project
from main.forms import ProjectForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse



def show_main(request):
    context = {
        "name": "Sofie Daniella<br> Ang",
        "npm": "2506619562",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia interested "
            "in Product Management, Business Strategy, and Digital Innovation. I enjoy exploring how technology can solve real-world problems and create impactful user experiences."
        ),
    }
    return render(request, "index.html", context)

def show_education(request):
    education_list = Education.objects.all()
    context = {
        'name' : 'Sofie Daniella Ang',
        'education_list' : education_list,
    }
    return render(request, "education.html", context)

def show_experience(request):
    experience_list = Experience.objects.all()
    context = {
        'name' : 'Sofie Daniella Ang',
        'experience_list': experience_list,
    }
    return render(request, "experience.html", context)

def create_project(request):
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

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")
