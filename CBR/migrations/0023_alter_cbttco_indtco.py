# Generated by Django 3.2.6 on 2021-08-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0022_auto_20210822_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbttco',
            name='indtco',
            field=models.CharField(db_column='indtco', max_length=1, verbose_name='Tipo de conciliación'),
        ),
    ]
