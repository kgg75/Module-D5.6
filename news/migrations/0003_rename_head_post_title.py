# Generated by Django 4.0.3 on 2022-04-12 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_head'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='head',
            new_name='title',
        ),
    ]