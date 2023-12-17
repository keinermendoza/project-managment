from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .models import Project

def home(request):
   return render(request, 'progress/home.html', {'active_section':'home'})

def projects_all(request):
    """return the public projects and the private if the 
    user is authenticated and has projects"""

    projects = Project.objects.filter(public=True)
    
    # get the private projects of this user
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(user=request.user)
        if user_projects is not None:
            projects = projects | user_projects

    return render(request, 'progress/project_list.html', {'projects':projects,
                                                  'active_section':'all'})

def projects_public(request):
    """return only the public projects"""
    projects = Project.objects.filter(public=True)

    return render(request, 'progress/project_list.html', {'projects':projects,
                                                  'active_section':'public'})

@login_required
def projects_private(request):
    """return the user private projects"""
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)

    return render(request, 'progress/project_list.html', {'projects':projects,
                                                  'active_section':'private'})

def project_detail(request, project_id):
    pass

@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})
