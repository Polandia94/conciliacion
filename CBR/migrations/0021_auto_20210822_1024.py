# Generated by Django 3.2.6 on 2021-08-22 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0020_auto_20210811_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbrenc',
            name='saldobcoori',
            field=models.DecimalField(blank=True, db_column='saldobcoori', decimal_places=2, max_digits=16, null=True),
        ),
        migrations.AddField(
            model_name='cbrenc',
            name='saldoerpori',
            field=models.DecimalField(blank=True, db_column='saldoerpori', decimal_places=2, max_digits=16, null=True),
        ),
    ]