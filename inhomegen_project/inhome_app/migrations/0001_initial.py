# Generated by Django 4.2.2 on 2024-01-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('api_key', models.CharField(max_length=200)),
                ('pub_date', models.DateField()),
            ],
        ),
    ]
