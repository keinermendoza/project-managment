# Generated by Django 5.0 on 2023-12-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0016_alter_project_image_alter_project_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='importance',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Normal'), (3, 'Importat'), (4, 'Urgent')], default=2),
        ),
    ]
