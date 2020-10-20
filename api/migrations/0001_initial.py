# Generated by Django 3.1.2 on 2020-10-21 01:41

import api.models.fields
import api.std_lib.lawm.variables
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LAWMSimulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LAWMResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pop', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Population)),
                ('popr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.PopulationGrowth)),
                ('simulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='api.lawmsimulation')),
            ],
        ),
    ]
