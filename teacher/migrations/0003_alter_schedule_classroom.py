# Generated by Django 5.1.10 on 2025-06-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_schedule_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='classroom',
            field=models.CharField(choices=[('6A', '6ème A'), ('6B', '6ème B'), ('5A', '5ème A'), ('5B', '5ème B'), ('4A', '4ème A'), ('4B', '4ème B'), ('3A', '3ème A'), ('3B', '3ème B'), ('2A', '2nde A'), ('2B', '2nde B'), ('1A', '1ère A'), ('1B', '1ère B'), ('TA', 'Terminale A'), ('TB', 'Terminale B')], default='6A', max_length=50),
        ),
    ]
