# Generated by Django 5.0.4 on 2024-06-04 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.meetingstatus'),
        ),
    ]