# Generated by Django 3.2.3 on 2021-07-27 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CBR', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cbrbod',
            fields=[
                ('idrbod', models.AutoField(db_column='idrbod', primary_key=True, serialize=False)),
                ('diatra', models.SmallIntegerField(db_column='diatra', verbose_name='Dia de Transaccion')),
                ('oficina', models.TextField(db_column='oficina', verbose_name='Oficina')),
                ('desctra', models.TextField(db_column='desctra', verbose_name='Descripcion de la transaccion')),
                ('debe', models.DecimalField(db_column='debe', decimal_places=2, max_digits=16)),
                ('haber', models.DecimalField(db_column='haber', decimal_places=2, max_digits=16)),
                ('saldo', models.DecimalField(db_column='saldo', decimal_places=2, max_digits=16)),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
                ('error', models.SmallIntegerField(db_column='error', default=0, verbose_name='Codigo de Error')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrbod',
                'managed': True,
            },
        ),
    ]
