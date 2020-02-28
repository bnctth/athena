# Generated by Django 3.0.3 on 2020-02-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Yeelight',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
    ]
