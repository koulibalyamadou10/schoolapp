# Generated by Django 5.1.10 on 2025-06-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_student_options_student_academic_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', max_length=1, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_class',
            field=models.CharField(choices=[('6A', '6ème A'), ('6B', '6ème B'), ('5A', '5ème A'), ('5B', '5ème B'), ('4A', '4ème A'), ('4B', '4ème B'), ('3A', '3ème A'), ('3B', '3ème B'), ('2A', '2nde A'), ('2B', '2nde B'), ('1A', '1ère A'), ('1B', '1ère B'), ('TA', 'Terminale A'), ('TB', 'Terminale B')], default='6A', max_length=100, verbose_name='Classe'),
        ),
    ]
