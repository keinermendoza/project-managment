# Generated by Django 4.2 on 2023-12-22 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0015_rename_finalized_task_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='projects'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(choices=[(1, 'Proccessing the requirements'), (2, 'Desiging the user interaction'), (3, 'Developing first version'), (4, 'Deploying first version'), (5, 'Adding more requirements'), (6, 'Completed')], default=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='started',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
