# Generated by Django 3.2.3 on 2021-07-27 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0003_alter_cbrbod_idrenc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cbterr',
            fields=[
                ('idterr', models.AutoField(db_column='idterr', primary_key=True, serialize=False)),
                ('coderr', models.IntegerField(db_column='coderr', verbose_name='codigo de error')),
                ('tabla', models.CharField(db_column='tabla', max_length=6, verbose_name='Tabla donde sucedió el error')),
                ('fechact', models.DateTimeField(blank=True, db_column='fechactbco', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo')),
            ],
            options={
                'db_table': 'cbterr',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='cbrbod',
            name='error',
        ),
        migrations.AlterField(
            model_name='cbrbod',
            name='idrbod',
            field=models.IntegerField(db_column='idrbod', primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Cbrgal',
            fields=[
                ('idrgal', models.IntegerField(db_column='idrgal', primary_key=True, serialize=False)),
                ('fechatra', models.DateField(blank=True, db_column='fechatra', null=True)),
                ('nrocomp', models.TextField(db_column='nrocomp', verbose_name='Numero de Comprobante')),
                ('aux', models.TextField(db_column='aux', verbose_name='Auxiliar')),
                ('ref', models.TextField(db_column='ref', verbose_name='Referencia')),
                ('glosa', models.TextField(db_column='glosa', verbose_name='Glosa')),
                ('debe', models.DecimalField(db_column='debe', decimal_places=2, max_digits=16)),
                ('haber', models.DecimalField(db_column='haber', decimal_places=2, max_digits=16)),
                ('saldo', models.DecimalField(db_column='saldo', decimal_places=2, max_digits=16)),
                ('fechacon', models.DateTimeField(blank=True, db_column='fechacon', null=True, verbose_name='Fecha de contabilizacion')),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrgal',
                'managed': True,
            },
        ),
    ]