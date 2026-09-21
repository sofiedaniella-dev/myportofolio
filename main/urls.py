from django.urls import path
from main.views import ( show_main, show_experience, create_experience, update_experience, delete_experience, get_experience_json,
show_education, show_projects, create_project, get_projects_json, delete_project )


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('experience/create/', create_experience, name='create_experience'),
    path('experience/update/<uuid:id>/', update_experience, name='update_experience'),
    path('experience/delete/<uuid:id>/', delete_experience, name='delete_experience'),
    path('api/experience/', get_experience_json, name='get_experience_json'),
    path("education/", show_education, name="show_education"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project,name="delete_project")
]