# Generated by Django 3.0.3 on 2020-02-22 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshtoken',
            name='aID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.AccessToken'),
        ),
    ]
