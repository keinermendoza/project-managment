from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


from .models import Project


def home(request):
    projects = Project.objects.filter(public=True)
    
    # get the private projects of this user
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(user=request.user)
        if user_projects is not None:
            projects += user_projects

    return render(request, 'progress/home.html', {'projects':projects})


@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})
