# Generated by Django 3.0.3 on 2020-03-25 09:19

import django.core.validators
from django.db import migrations, models


def set_custom_progress(apps, schema_editor):
    BotflowExecution = apps.get_model('orchestrator', 'BotflowExecution')
    BotflowExecution.objects.filter(time_end__isnull=False).update(custom_progress=100)


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0006_v022_4'),
    ]

    operations = [
        migrations.AddField(
            model_name='botflowexecution',
            name='custom_progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.RunPython(set_custom_progress, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='botflowexecution',
            name='custom_progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='botflowexecution',
            name='custom_status',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='botflowexecution',
            name='time_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
