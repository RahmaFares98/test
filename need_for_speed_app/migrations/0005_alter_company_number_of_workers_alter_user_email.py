# Generated by Django 5.1 on 2024-08-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('need_for_speed_app', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='number_of_workers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
