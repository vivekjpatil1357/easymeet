# Generated by Django 4.1.2 on 2023-07-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcall', '0006_delete_activenames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='isactive',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]