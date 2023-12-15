from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Project, Task, TaskNote, ProjectNote

def project_view(obj):
    url = reverse('progress:admin_project_view', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

class ProjectNoteAdmin(admin.StackedInline):
    """for see the projectNote form inside the ProjectAdmin"""

    model = ProjectNote
    extra = 1 

class TaskStackedAdmin(admin.StackedInline):
    """for see the task form inside the ProjectAdmin"""
    
    model = Task
    extra = 1

class TaskNoteStackedAdmin(admin.StackedInline):
    """for see the taskNoteStacked form inside the TaskAdmin"""

    model = TaskNote
    extra = 1



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskNoteStackedAdmin]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'importance', 'status', 'created', project_view]
    search_fields = ['name', 'description']
    inlines = [ProjectNoteAdmin, TaskStackedAdmin]
