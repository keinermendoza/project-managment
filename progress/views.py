from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


from .models import Project


def home(request):
    return render(request, 'progress/home.html')


@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})
