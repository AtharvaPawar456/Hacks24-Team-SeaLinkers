# Generated by Django 4.2.2 on 2024-01-31 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inhome_app', '0005_projectdetails_jsondata'),
    ]

    operations = [
        migrations.AddField(
            model_name='imgdetails',
            name='path',
            field=models.CharField(default='', max_length=120),
        ),
    ]
