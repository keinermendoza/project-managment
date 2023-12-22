from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseForbidden
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
    """returns all the public projects and the
    current user private projects"""

    projects = Project.objects.filter(public=True)
    
    # get the private projects of this user
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(user=request.user, public=False)
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
    """returns all the public projects"""
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
    """returns the user private projects"""

    projects = Project.objects.filter(user=request.user, public=False)

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True

    else:
        template_name = 'progress/project_list.html'
        title = False

    return render(request, template_name, {'projects':projects, 'active_section':'private', 'title':title})

def project_detail(request, project_id):
    """returns the detail project is it's public or if the 
    request user is the owner"""
    
    project = get_object_or_404(Project, id=project_id)

    if project.public:
        pass
    else: 
        if not request.user.is_authenticated or request.user != project.user:
            return HttpResponseForbidden
    return render(request, "progress/project_detail.html", {'project':project, 'active_section':''})



@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})
