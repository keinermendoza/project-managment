from django.utils import timezone as tz
from django.test import TestCase
from .models import Task, Project

class TaskTests(TestCase):
    def setUp(self):
        project_required_data = {
            'name': 'project test',
            'description': 'description of my project',
        }
        self.project = Project.objects.create(**project_required_data)

        task_required_data = {
            'name' : 'my task',
            'description' : '',
            'project' : self.project
        }

        task_working_status = {
            'name' : 'my task 2',
            'description' : 'this is my second task',
            'project' : self.project,
            'status' : Task.Status.WORKING,
            'estimated_time': 2,
        }
        self.task = Task.objects.create(**task_required_data)
        self.task2 = Task.objects.create(**task_working_status)

    def test_required_data(self):
        """checking the required data for create tasks and projects"""
        self.assertIsInstance(self.task, Task)
        self.assertIsInstance(self.project, Project)

    def test_task_default_values(self):
        """checks the expected value dates """
        self.assertIsNone(self.task.started)
        self.assertIsNone(self.task.finalized)
        self.assertIsNone(self.task.estimated_time)
        self.assertEqual(self.task.esitmated_unit_time, Task.UnitTime.HOUR)

        # get_time_to_finish is not None only when started exists and finalized is None
        self.assertIsNone(self.task.get_time_to_finish)

        
        # important default value of status is PENDING
        self.assertEqual(self.task.status, Task.Status.PENDING)
        self.assertEqual(self.task.importance, Task.Importance.NORMAL)
        self.assertEqual(self.task.created.replace(second=0, microsecond=0),
                          tz.now().replace(second=0, microsecond=0))

    def test_task_change_status_to_wroking(self):
        """change status of task to working must change the task.started value"""
        
        # by default started is None
        self.assertIsNone(self.task.started)

        
        self.task.status = Task.Status.WORKING
        self.task.save()
        
        # after save started has been "created"
        self.assertIsNotNone(self.task.started)

        self.assertEqual(self.task.started.replace(second=0, microsecond=0),
                          tz.now().replace(second=0, microsecond=0))
        
    def test_task2_change_status_working_to_finished(self):
        """change status of task2 must update the values of started and finalized"""
        # it has been created with status WORKING so created exists
        self.assertIsNotNone(self.task2.started)
        self.assertIsNone(self.task2.finalized)

        # when change status to FINISHED finalized is created
        self.task2.status = Task.Status.FINISHED
        self.task2.save()
        self.assertIsNotNone(self.task2.finalized)

        # if change status from FINISHED to WAITING started and finalized are set to None
        self.task2.status = Task.Status.PENDING
        self.task2.save()
        self.assertIsNone(self.task2.started)
        self.assertIsNone(self.task2.finalized)

    def test_task2_get_time_to_finish(self):
        """beacuse task2 was registred with status WORKING it must have a get_time_to_finish"""
        self.assertIsNotNone(self.task2.get_time_to_finish)