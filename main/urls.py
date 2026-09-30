from django.urls import path
from main.views import ( show_main, show_experience, create_experience, update_experience, delete_experience, get_experience_json,
show_education, show_projects, create_project, get_projects_json, delete_project, update_project, register, login_user, logout_user, toggle_star,
create_project_ajax)


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
    path('projects/update/<uuid:project_id>/', update_project, name='update_project'),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project,name="delete_project"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]