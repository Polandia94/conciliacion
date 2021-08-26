# Generated by Django 3.2.6 on 2021-08-25 19:05

import db_file_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0005_alter_cbrenc_imgbcoroute'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbrenc',
            name='imgbco',
            field=models.BinaryField(db_column='imgbco', editable=True, null=True, verbose_name='Imagen de banco'),
        ),
        migrations.AlterField(
            model_name='cbrenc',
            name='imgbcoroute',
            field=models.FileField(blank=True, null=True, storage=db_file_storage.storage.DatabaseFileStorage, upload_to='CBR.Cbrenci/imgbco/imgbconame/imgbcomime', verbose_name='Imagen del Banco'),
        ),
    ]
