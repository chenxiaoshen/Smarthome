from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LED_FORM',
            fields=[
                ('switch', models.CharField(max_length=30)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
