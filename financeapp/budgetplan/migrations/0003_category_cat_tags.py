# Generated by Django 5.0.6 on 2024-06-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetplan', '0002_alter_activity_ac_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_tags',
            field=models.CharField(choices=[('Must', 'Must'), ('Need', 'Need'), ('Want', 'Want')], default='Want', max_length=10),
        ),
    ]
