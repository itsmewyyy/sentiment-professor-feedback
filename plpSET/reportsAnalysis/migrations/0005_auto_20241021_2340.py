# Generated by Django 3.2 on 2024-10-21 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SET', '0013_remove_feedbacks_pre_processed_text'),
        ('reportsAnalysis', '0004_feedback_summary_numerical_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='college_feedback_summary',
            fields=[
                ('college_feedback_summary_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_feedbacks', models.IntegerField()),
                ('total_positive', models.IntegerField()),
                ('total_negative', models.IntegerField()),
                ('total_neutral', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.department')),
                ('feedback_question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.feedback_questions')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='college_feedback_total',
            fields=[
                ('college_total_summary_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_feedbacks', models.IntegerField()),
                ('total_positive', models.IntegerField()),
                ('total_negative', models.IntegerField()),
                ('total_neutral', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.department')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='college_numerical_summary',
            fields=[
                ('college_numerical_summary_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('college_average', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.categories')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.department')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='college_numerical_total',
            fields=[
                ('college_numerical_total_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_average', models.FloatField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.department')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='professor_feedback_summary',
            fields=[
                ('professor_feedback_summary_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_feedbacks', models.IntegerField()),
                ('total_positive', models.IntegerField()),
                ('total_negative', models.IntegerField()),
                ('total_neutral', models.IntegerField()),
                ('feedback_question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.feedback_questions')),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.professor_info')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='professor_feedback_total',
            fields=[
                ('professor_feedback_total_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_feedbacks', models.IntegerField()),
                ('total_positive', models.IntegerField()),
                ('total_negative', models.IntegerField()),
                ('total_neutral', models.IntegerField()),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.professor_info')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='professor_numerical_summary_category',
            fields=[
                ('professor_numerical_summary_category_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('category_average', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.categories')),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.professor_info')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='professor_numerical_summary_questions',
            fields=[
                ('professor_numerical_summary_question_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('question_average', models.FloatField()),
                ('numerical_questions_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.numerical_questions')),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.professor_info')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.CreateModel(
            name='professor_numerical_total',
            fields=[
                ('professor_numerical_total_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('total_average', models.FloatField()),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.professor_info')),
                ('year_sem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SET.academic_yearsem')),
            ],
        ),
        migrations.RemoveField(
            model_name='numerical_summary',
            name='numerical_questions_id',
        ),
        migrations.RemoveField(
            model_name='numerical_summary',
            name='prof_id',
        ),
        migrations.RemoveField(
            model_name='numerical_summary',
            name='year_sem_id',
        ),
        migrations.DeleteModel(
            name='feedback_summary',
        ),
        migrations.DeleteModel(
            name='numerical_summary',
        ),
    ]
