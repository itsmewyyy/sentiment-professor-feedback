# Generated by Django 5.0.7 on 2024-10-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SET', '0008_remove_numerical_ratings_numerical_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbacks',
            name='feedback_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numerical_ratings',
            name='numerical_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
