# Generated by Django 3.2.6 on 2021-08-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0003_alter_cbrenc_imgbcoroute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbrenc',
            name='imgbcoroute',
            field=models.TextField(blank=True, null=True, verbose_name='Imagen del Banco'),
        ),
    ]