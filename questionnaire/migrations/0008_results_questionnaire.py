# Generated by Django 4.0.4 on 2022-09-03 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='questionnaire',
            field=models.ForeignKey(default='s1', on_delete=django.db.models.deletion.CASCADE, related_name='results', to='questionnaire.questionnaires', to_field='name'),
        ),
    ]
