# Generated by Django 5.0.2 on 2024-07-08 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetplan', '0005_alter_activity_options_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user_id',
            field=models.IntegerField(default=1),
        ),
    ]