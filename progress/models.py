from django.db import models

class Project(models.Model):
    class Importance(models.IntegerChoices):
        LOW = (1, 'Low')
        INTERESTIG = (2, 'Interesting')
        GOOD = (3, 'Good')
        IMPORTANT = (4, 'Importat')
        URGENT = (5, 'Urgent')       

    class Status(models.IntegerChoices):
        IDEA = (1, 'Proccessing the business model')
        DESING = (2, 'Desiging the user interaction')
        MODELS = (3, 'Creating prototipe app')
        GROW = (4, 'Adjusting details')
        IMPLEMENTIG = (5, 'Deploying version 1')
        ITERATING = (6, 'Improving Performance and adding new Features')

    name = models.CharField(max_length=120)
    description = models.TextField()
    importance = models.IntegerField(choices=Importance.choices, default=Importance.GOOD)
    status = models.IntegerField(choices=Status.choices, default=Status.IDEA)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        ordering = ['-importance', '-status', '-created']
        indexes = [models.Index(
            fields=['-importance', '-status', '-created']
        )]

    def __str__(self):
        return f'Proyect: {self.name}'
    

class Task(models.Model):
    class Status(models.IntegerChoices):
        PENDING = (1, 'Not started yet')
        WORKING = (2, 'Working on it')
        WAITING = (3, 'Waiting feed back')
        FINISHED = (4, 'Completed')
    
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-status',]
        indexes = [models.Index(
            fields=['-created', '-status']
        )]

    def __str__(self):
        return f'Task: {self.name} from {self.project}'
    
class AbstractNote(models.Model):
    message = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ProjectNote(AbstractNote):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_notes')
    
    def was_updated(self):
        created = self.created.replace(second=0, microsecond=0)
        updated = self.updated.replace(second=0, microsecond=0)

        return created != updated
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(
            fields=['-created']
        )]

class TaskNote(AbstractNote):
    task = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='task_notes')
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(
            fields=['-created']
        )]
