# Generated by Django 3.0.3 on 2020-06-03 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=30)),
                ('calc_nr', models.CharField(max_length=30)),
                ('search_str', models.CharField(max_length=30)),
                ('result', models.CharField(max_length=4096)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
    ]
