# Generated by Django 4.2.2 on 2024-01-31 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inhome_app', '0003_projectdetails_pub_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('prompt', models.CharField(default='', max_length=50)),
                ('negprompt', models.CharField(default='', max_length=50)),
                ('style', models.CharField(default='', max_length=50)),
                ('pub_date', models.DateField()),
                ('pub_time', models.CharField(max_length=50)),
            ],
        ),
    ]
