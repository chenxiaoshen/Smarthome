# Generated by Django 3.0.5 on 2020-04-26 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TH_FORM',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('timeval', models.CharField(max_length=20)),
                ('temperature', models.IntegerField()),
                ('humidity', models.IntegerField()),
            ],
        ),
    ]
