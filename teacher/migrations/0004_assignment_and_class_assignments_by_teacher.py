# Generated by Django 2.1 on 2018-10-21 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_teacher_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='assignment_and_class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ass_title', models.CharField(max_length=10000)),
                ('ass_class', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='assignments_by_teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=200)),
                ('ass_title', models.CharField(max_length=10000)),
                ('ass_body', models.CharField(max_length=50000)),
                ('ass_sub_date', models.DateField()),
                ('ass_given_date', models.DateField()),
                ('ass_extra', models.CharField(max_length=50000)),
            ],
        ),
    ]