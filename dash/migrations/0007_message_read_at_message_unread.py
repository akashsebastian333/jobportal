# Generated by Django 4.0.2 on 2023-02-19 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0006_remove_message_read_at_message_parent_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]