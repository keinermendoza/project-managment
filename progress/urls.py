from django.urls import path 
from . import views

app_name = 'progress'
urlpatterns = [
    path('progress/admin/project/<int:project_id>/', views.admin_project_view, name="admin_project_view"),
    path('', views.home, name='home'),
]