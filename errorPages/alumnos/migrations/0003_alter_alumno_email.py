# Generated by Django 5.1.4 on 2025-02-25 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_alter_alumno_matricula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
