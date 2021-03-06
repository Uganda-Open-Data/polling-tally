# Generated by Django 3.1.5 on 2021-01-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_pollingstation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='county',
            name='code',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='district',
            name='code',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='parish',
            name='code',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='subcounty',
            name='code',
            field=models.CharField(max_length=64),
        ),
    ]
