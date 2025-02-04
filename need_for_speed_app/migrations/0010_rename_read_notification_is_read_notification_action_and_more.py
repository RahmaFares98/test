# Generated by Django 5.1 on 2024-08-24 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('need_for_speed_app', '0009_rename_link_notification_message_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='is_read',
        ),
        migrations.AddField(
            model_name='notification',
            name='action',
            field=models.CharField(default='created', max_length=50),
        ),
        migrations.AddField(
            model_name='notification',
            name='content_type',
            field=models.CharField(default='Post', max_length=100),
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(default='/', max_length=255),
        ),
        migrations.AddField(
            model_name='notification',
            name='object_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
