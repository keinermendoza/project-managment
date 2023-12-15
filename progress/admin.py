from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from account.models import User
from .models import Project, Task, TaskNote, ProjectNote

from django import forms

class NoteTaskForm(forms.ModelForm):
    class Meta:
        model = TaskNote
        fields = ["message", "user"]
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(NoteTaskForm, self).__init__(*args, **kwargs)

    ### this is hardcodded
    ### works for a single admin user
    def save(self, commit=True):
        instance = super(NoteTaskForm, self).save(commit=False)
        
        if instance.user is None:
            instance.user =  User.objects.filter(is_staff=True).first()
        instance.save()
        return instance

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
    form = NoteTaskForm 
    readonly_fields = ["user"]
    model = TaskNote
    extra = 1

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["project"]
    inlines = [TaskNoteStackedAdmin]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'importance', 'status', 'created', project_view]
    search_fields = ['name', 'description']
    inlines = [ProjectNoteAdmin, TaskStackedAdmin]
