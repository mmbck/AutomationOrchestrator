# Generated by Django 3.0.4 on 2020-04-07 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0008_v031'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='emailimaptrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='emailoutlooktrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='filetrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='historicalapitrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='historicalemailimaptrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='historicalemailoutlooktrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='historicalfiletrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='historicalscheduletrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
        migrations.AddField(
            model_name='scheduletrigger',
            name='botflow_execution_custom_status',
            field=models.CharField(blank=True, help_text='Specify a custom text to set as the start note of the queued Botflow Execution.', max_length=255, verbose_name='Botflow Execution Note'),
        ),
    ]
