from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Project, Task, TaskNote, ProjectNote

def project_view(obj):
    url = reverse('progress:admin_project_view', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

class ProjectNoteAdmin(admin.StackedInline):
    model = ProjectNote
    extra = 1 

class TaskAdmin(admin.StackedInline):
    model = Task
    extra = 1 


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'importance', 'status', 'created', project_view]
    search_fields = ['name', 'description']
    inlines = [ProjectNoteAdmin, TaskAdmin]
