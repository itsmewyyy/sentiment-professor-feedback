# Generated by Django 5.0.7 on 2024-10-09 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SET', '0009_alter_feedbacks_feedback_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_enrolled_subjs',
            name='student_enrolled_subj_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
