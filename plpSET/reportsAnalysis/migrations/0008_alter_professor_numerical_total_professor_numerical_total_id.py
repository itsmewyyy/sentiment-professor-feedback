# Generated by Django 3.2 on 2024-10-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportsAnalysis', '0007_alter_professor_feedback_total_professor_feedback_total_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor_numerical_total',
            name='professor_numerical_total_id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
