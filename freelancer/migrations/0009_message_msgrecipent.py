# Generated by Django 4.2 on 2023-04-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0008_project_profileproj_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='msgrecipent',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
