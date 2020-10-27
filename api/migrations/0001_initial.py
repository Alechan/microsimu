# Generated by Django 3.1.2 on 2020-10-27 23:57

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
            name='LAWMRegion',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='LAWMSimulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LAWMRegionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_result', to='api.lawmregion')),
                ('simulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_results', to='api.lawmsimulation')),
            ],
            options={
                'unique_together': {('simulation', 'region')},
            },
        ),
        migrations.CreateModel(
            name='LAWMYearResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('pop', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Population)),
                ('popr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.PopulationGrowth)),
                ('exlife', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LifeExpectancy)),
                ('grmor', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GrossMortality)),
                ('birthr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.BirthRate)),
                ('chmor', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.ChildMortalityRate)),
                ('calor', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Calories)),
                ('prot', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Proteins)),
                ('hsexfl', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.HousesPerFamily)),
                ('gnpxc', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPPerPerson)),
                ('enrol', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.EnrolmentPercentage)),
                ('educr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.MatriculationPercentage)),
                ('eapopr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Pop11To70LaborForcePercentage)),
                ('tlf', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.TotalLaborForce)),
                ('rlfd_1', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LaborForceFoodSectorProportion)),
                ('rlfd_2', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LaborForceHousingSectorProportion)),
                ('rlfd_3', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LaborForceEducationSectorProportion)),
                ('rlfd_4', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LaborForceOtherGoodsProportion)),
                ('rlfd_5', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.LaborForceCapitalGoodsSectorProportion)),
                ('capt', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.TotalCapital)),
                ('capd_1', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.CapitalFoodSectorProportion)),
                ('capd_2', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.CapitalHousingSectorProportion)),
                ('capd_3', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.CapitalEducationSectorProportion)),
                ('capd_4', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.CapitalOtherGoodsSectorProportion)),
                ('capd_5', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.CapitalCapitalGoodsSectorProportion)),
                ('_0_5', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Pop0to5Percentage)),
                ('_6_17', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Pop6to17Percentage)),
                ('_11_70', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.Pop11to70Percentage)),
                ('al', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.ArableLand)),
                ('excal', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.ExcessCalories)),
                ('fert', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.FertilizersProduction)),
                ('rend', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.AgricultureYield)),
                ('falu', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.PotentialArableLandProportion)),
                ('urbanr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.UrbanPopulationPercentage)),
                ('turbh', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.UrbanizationRate)),
                ('sepopr', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.SecondaryLaborForcePercentage)),
                ('houser', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.HousesPerPersonPercentage)),
                ('perxfl', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.PeoplePerFamily)),
                ('gnp', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNP)),
                ('gnpd_1', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPFoodSectorProportion)),
                ('gnpd_2', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPHousingSectorProportion)),
                ('gnpd_3', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPEducationSectorProportion)),
                ('gnpd_4', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPOtherGoodsSectorProportion)),
                ('gnpd_5', api.models.fields.VariableFloatField(model_variable=api.std_lib.lawm.variables.GNPCapitalGoodsSectorProportion)),
                ('region_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='year_results', to='api.lawmregionresult')),
            ],
            options={
                'unique_together': {('region_result', 'year')},
            },
        ),
    ]
