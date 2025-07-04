# Generated by Django 5.2.1 on 2025-07-03 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logframe', '0004_remove_indicator_project_remove_outcome_project_and_more'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('budget_allocated', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('budget_spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='planned', max_length=50)),
                ('output', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='logframe.output')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='projects.project')),
            ],
        ),
    ]
