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
    # form = NoteTaskForm 
    readonly_fields = ["user"]
    model = TaskNote
    extra = 1

    ### this could be helpfull for single forms of admin.ModelAdmin
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["project"]
    inlines = [TaskNoteStackedAdmin]

    # Django Docs are Awesome
    # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_formset
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.user is None:
                instance.user = request.user
            instance.save()
        # formset.save_m2m()

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', project_view, 'importance', 'status', 'created', ]
    search_fields = ['name', 'description']
    inlines = [ProjectNoteAdmin, TaskStackedAdmin]
