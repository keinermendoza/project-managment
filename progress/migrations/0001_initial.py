# Generated by Django 5.0 on 2023-12-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('importance', models.IntegerField(choices=[('1', 'Low'), ('2', 'Interesting'), ('3', 'Good'), ('4', 'Importat'), ('5', 'Urgent')], default='3')),
                ('status', models.IntegerField(choices=[('1', 'Proccessing the business model'), ('2', 'Desiging the user interaction'), ('3', 'Creating prototipe app'), ('4', 'Adjusting details'), ('5', 'Deploying version 1'), ('6', 'Improving Performance and adding new Features')], default='1')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-importance', '-status', '-created'],
                'indexes': [models.Index(fields=['-importance', '-status', '-created'], name='progress_pr_importa_f37562_idx')],
            },
        ),
    ]
