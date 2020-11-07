# Generated by Django 3.1.3 on 2020-11-07 19:54

import api.models.fields
import api.models.validators
import api.std_lib.lawm.general_parameters
import api.std_lib.lawm.regional_parameters
import api.std_lib.lawm.variables
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LAWMGeneralParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simulation_stop', api.models.fields.ParameterIntegerField(blank=True, default=2000, model_parameter=api.std_lib.lawm.general_parameters.SimulationStop, validators=[api.models.validators.MaxValueParameterValidator(2050), api.models.validators.MinValueParameterValidator(1990)])),
                ('optimization_start', api.models.fields.ParameterIntegerField(blank=True, default=1980, model_parameter=api.std_lib.lawm.general_parameters.OptimizationStart, validators=[api.models.validators.MaxValueParameterValidator(2050), api.models.validators.MinValueParameterValidator(1980)])),
                ('payments_equilibrium', api.models.fields.ParameterIntegerField(blank=True, default=2000, model_parameter=api.std_lib.lawm.general_parameters.PaymentsEquilibrium, validators=[api.models.validators.MaxValueParameterValidator(2050), api.models.validators.MinValueParameterValidator(1990)])),
                ('fertilizer_cost', api.models.fields.ParameterFloatField(blank=True, default=769230.8, model_parameter=api.std_lib.lawm.general_parameters.FertilizerCost, validators=[api.models.validators.MinValueParameterValidator(1)])),
                ('weight_constraint_1', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint1, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_2', api.models.fields.ParameterFloatField(blank=True, default=8.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint2, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_3', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint3, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_4', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint4, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_5', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint5, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_6', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint6, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_7', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint7, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_8', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint8, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_9', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint9, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_10', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint10, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_11', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint11, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_12', api.models.fields.ParameterFloatField(blank=True, default=2.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint12, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_13', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint13, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_14', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint14, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_15', api.models.fields.ParameterFloatField(blank=True, default=7.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint15, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_16', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint16, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_17', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint17, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_18', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint18, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_19', api.models.fields.ParameterFloatField(blank=True, default=8.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint19, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_20', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint20, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_21', api.models.fields.ParameterFloatField(blank=True, default=4.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint21, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_22', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint22, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_23', api.models.fields.ParameterFloatField(blank=True, default=8.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint23, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_24', api.models.fields.ParameterFloatField(blank=True, default=6.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint24, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_25', api.models.fields.ParameterFloatField(blank=True, default=2.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint25, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
                ('weight_constraint_26', api.models.fields.ParameterFloatField(blank=True, default=1.0, model_parameter=api.std_lib.lawm.general_parameters.WeightConstraint26, validators=[api.models.validators.MaxValueParameterValidator(14), api.models.validators.MinValueParameterValidator(2)])),
            ],
        ),
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
            name='LAWMRunParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_parameters', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='run_parameters', to='api.lawmgeneralparameters')),
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='run_parameters', to='api.lawmsimulation')),
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
        migrations.CreateModel(
            name='LAWMRegionalParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_calories', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.MaxCalories, validators=[api.models.validators.MaxValueParameterValidator(3200.0), api.models.validators.MinValueParameterValidator(2600.0)])),
                ('max_build_cost', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.MaxBuildCost, validators=[api.models.validators.MaxValueParameterValidator(20.0), api.models.validators.MinValueParameterValidator(5.0)])),
                ('tech_prog_coeff_1', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressCoefficient1, validators=[api.models.validators.MaxValueParameterValidator(1.1), api.models.validators.MinValueParameterValidator(1.0)])),
                ('tech_prog_coeff_2', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressCoefficient2, validators=[api.models.validators.MaxValueParameterValidator(1.1), api.models.validators.MinValueParameterValidator(1.0)])),
                ('tech_prog_coeff_3', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressCoefficient3, validators=[api.models.validators.MaxValueParameterValidator(1.1), api.models.validators.MinValueParameterValidator(1.0)])),
                ('tech_prog_coeff_4', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressCoefficient4, validators=[api.models.validators.MaxValueParameterValidator(1.1), api.models.validators.MinValueParameterValidator(1.0)])),
                ('tech_prog_coeff_5', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressCoefficient5, validators=[api.models.validators.MaxValueParameterValidator(1.1), api.models.validators.MinValueParameterValidator(1.0)])),
                ('tech_prog_stop', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.TechProgressStop, validators=[api.models.validators.MaxValueParameterValidator(3000.0), api.models.validators.MinValueParameterValidator(1990.0)])),
                ('years_building_cost_eq', api.models.fields.ParameterIntegerField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.YearsForBuildingCostEquality, validators=[api.models.validators.MaxValueParameterValidator(100.0), api.models.validators.MinValueParameterValidator(20.0)])),
                ('years_housing_level_eq', api.models.fields.ParameterIntegerField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.YearsForHousingLevelEquality, validators=[api.models.validators.MaxValueParameterValidator(50.0), api.models.validators.MinValueParameterValidator(10.0)])),
                ('desired_food_stock', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.DesiredFoodStock, validators=[api.models.validators.MaxValueParameterValidator(730.0), api.models.validators.MinValueParameterValidator(100.0)])),
                ('years_space_p_person_eq', api.models.fields.ParameterIntegerField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.YearsForSpacePerPersonEquality, validators=[api.models.validators.MaxValueParameterValidator(100.0), api.models.validators.MinValueParameterValidator(10.0)])),
                ('max_space_p_person', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.MaxSpacePerPerson, validators=[api.models.validators.MaxValueParameterValidator(100.0), api.models.validators.MinValueParameterValidator(10.0)])),
                ('desired_space_p_person', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.DesiredSpacePerPerson, validators=[api.models.validators.MaxValueParameterValidator(50.0), api.models.validators.MinValueParameterValidator(5.0)])),
                ('max_sec_5_gnp_propor', api.models.fields.ParameterFloatField(blank=True, model_parameter=api.std_lib.lawm.regional_parameters.MaxCapitalGoodsGNPProportion, validators=[api.models.validators.MaxValueParameterValidator(0.35), api.models.validators.MinValueParameterValidator(0.1)])),
                ('region', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_parameters', to='api.lawmregion')),
                ('run_parameters', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_parameters', to='api.lawmrunparameters')),
            ],
            options={
                'unique_together': {('run_parameters', 'region')},
            },
        ),
    ]
