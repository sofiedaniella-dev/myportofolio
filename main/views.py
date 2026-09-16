from django.shortcuts import render
from main.models import Education
from main.models import Experience


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