from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .models import Project

def home(request):

    if request.htmx:
        template_name = 'progress/snippets/home.html'
        title = True
    else:
        template_name = 'progress/home.html'
        title = False

    return render(request, template_name, {'active_section':'home', 'title':title})

def projects_all(request):
    """return the public projects and the private if the 
    user is authenticated and has projects"""

    projects = Project.objects.filter(public=True)
    
    # get the private projects of this user
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(user=request.user)
        if user_projects is not None:
            projects = projects | user_projects

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True
    else:
        template_name = 'progress/project_list.html'
        title = False

    return render(request, template_name, {'projects':projects, 'title':title, 'active_section':'all'})

def projects_public(request):
    """return only the public projects"""
    projects = Project.objects.filter(public=True)

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True
    else:
        template_name = 'progress/project_list.html'
        title = False
    return render(request, template_name, {'projects':projects, 'active_section':'public', 'title':title})

@login_required
def projects_private(request):
    """return the user private projects"""
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True

    else:
        template_name = 'progress/project_list.html'
        title = False

    return render(request, template_name, {'projects':projects, 'active_section':'private', 'title':title})

def project_detail(request, project_id):
    pass

@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})
