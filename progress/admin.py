from django.contrib import admin
from .models import Project, Task

class TaskAdmin(admin.StackedInline):
    model = Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'importance', 'status', 'created']
    search_fields = ['name', 'description']
    inlines = [TaskAdmin]
