# Generated by Django 3.2 on 2024-11-02 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userLogin', '0011_student_acc_is_counted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_acc',
            name='is_counted',
        ),
    ]
