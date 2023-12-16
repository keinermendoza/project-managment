from django.db import models
from account.models import User

class Project(models.Model):
    class Importance(models.IntegerChoices):
        LOW = (1, 'Low')
        INTERESTIG = (2, 'Interesting')
        NORMAL = (3, 'Normal')
        IMPORTANT = (4, 'Importat')
        URGENT = (5, 'Urgent')       

    class Status(models.IntegerChoices):
        IDEA = (1, 'Proccessing the business model')
        DESING = (2, 'Desiging the user interaction')
        MODELS = (3, 'Creating prototipe app')
        GROW = (4, 'Adjusting details')
        IMPLEMENTIG = (5, 'Deploying version 1')
        ITERATING = (6, 'Improving Performance and adding new Features')
        FINISHED = (7, 'Completed')


    name = models.CharField(max_length=120)
    description = models.TextField()
    importance = models.IntegerField(choices=Importance.choices, default=Importance.NORMAL)
    status = models.IntegerField(choices=Status.choices, default=Status.IDEA)
    image = models.FileField(upload_to='projects', null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-importance', '-status', '-created']
        indexes = [models.Index(
            fields=['-importance', '-status', '-created']
        )]

    def __str__(self):
        return self.name
    

class Task(models.Model):
    class Importance(models.IntegerChoices):
        LOW = (1, 'Low')
        INTERESTIG = (2, 'Interesting')
        NORMAL = (3, 'Normal')
        IMPORTANT = (4, 'Importat')
        URGENT = (5, 'Urgent')       

    class Status(models.IntegerChoices):
        PENDING = (1, 'Not started yet')
        WORKING = (2, 'Working on it')
        WAITING = (3, 'Waiting feed back')
        FINISHED = (4, 'Completed')
    
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    importance = models.IntegerField(choices=Importance.choices, default=Importance.NORMAL)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-importance', '-status',]
        indexes = [models.Index(
            fields=['-created', '-importance', '-status']
        )]

    def __str__(self):
        return f'{self.name} from Proyect: {self.project}'
    
class AbstractNote(models.Model):
    """for use as base of ProjectNote and TaskNote"""
    message = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'writed on {self.created.strftime("%d/%m/%Y %I:%M%p")}'

class ProjectNote(AbstractNote):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_notes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="project_notes",
                             blank=True)
    
    def was_updated(self):
        """for show the updated date only when it was updated"""
        created = self.created.replace(second=0, microsecond=0)
        updated = self.updated.replace(second=0, microsecond=0)

        return created != updated
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(
            fields=['created']
        )]

class TaskNote(AbstractNote):
    task = models.ForeignKey(Task,
                                on_delete=models.CASCADE,
                                related_name='task_notes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="task_notes",
                             blank=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(
            fields=['created']
        )]
