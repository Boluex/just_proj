# Generated by Django 4.0.4 on 2024-02-02 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_delete_courseoffer'),
        ('accounts', '0019_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='student',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_dep_head',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_parent',
        ),
        migrations.DeleteModel(
            name='DepartmentHead',
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
    ]