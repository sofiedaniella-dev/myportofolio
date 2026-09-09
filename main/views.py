from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Sofie Daniella Ang",
        "npm": "2506619562",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia interested "
            "in Product Management, Business Strategy, and Digital Innovation. I enjoy exploring how technology can solve real-world problems and create impactful user experiences."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Sofie Daniella Ang",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)