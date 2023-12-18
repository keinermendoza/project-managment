from datetime import timedelta
from django.db import models
from django.utils import timezone as tz
from django.core.exceptions import ValidationError

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
    user = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE, null=True)

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

    class UnitTime(models.TextChoices):
        HOUR = ('H', 'Hour')
        DAY = ('D', 'Day')

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    importance = models.IntegerField(choices=Importance.choices, default=Importance.NORMAL)

    estimated_time = models.PositiveIntegerField(null=True)
    esitmated_unit_time = models.CharField(max_length=1, choices=UnitTime.choices,
                                           default=UnitTime.HOUR)
    
    started = models.DateTimeField(null=True)
    finalized = models.DateTimeField(null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    __original_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        
        # new taks
        if not self.id:
            # marked as worked
            if self.status == self.Status.WORKING:
                self.started = tz.now()
        
            # marked as finalized
            if self.status == self.Status.FINISHED:
                self.started = tz.now()
                self.finalized = tz.now() + timedelta(seconds=1)

        # Task registred previously
        else:
            # if it was stoped
            if self.__original_status == self.Status.WAITING\
                or self.__original_status == self.Status.PENDING:
                
                print("dentro del else")
                if self.status == self.Status.WORKING:
                    print("working")
                    self.started = tz.now()
                    self.finalized = None

                elif self.status == self.Status.FINISHED:
                    print("finished")
                    
                    self.started = tz.now()
                    self.finalized = tz.now() + timedelta(seconds=1)

            elif self.__original_status == self.Status.WORKING:
                if self.status == self.Status.FINISHED:
                    self.finalized = tz.now()



        super(Task, self).save(*args, **kwargs)
        self.__original_status = self.status


    # def start_task(self):
    #     """writes the task start time 
    #     returns the current server time if write None otherwise"""
        
    #     if not self.started:
    #         self.started = tz.now()
    #         self.save()
    #         return self.started
    #     return None


    # def finish_task(self):
    #     """writes the task finish
    #     returns the current server time if write None otherwise"""

    #     if self.started:
    #         self.finalized = tz.now()
    #         self.save()
    #         return self.finalized
    #     return None

    @property
    def get_time_to_finish(self):
        if not self.started or not self.estimated_time or not self.estimated_unit_time:
            print('first')
            return None
        if self.started and self.finalized:
            print('second')
            return None
        if self.stimated_unit_time == self.UnitTime.HOUR:
            estimated_finish = tz.now() + timedelta(hours=self.estimated_time)
        else:
            estimated_finish = tz.now() + timedelta(days=self.estimated_time)
        print('final')

        estimated_finish = self.started + estimated_finish 
        return estimated_finish.replace(second=0, microsecond=0)

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
    public = models.BooleanField(default=False)

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
