# Generated by Django 3.2.6 on 2021-09-17 19:36

import CBR.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cbrbod',
            fields=[
                ('idrbod', models.IntegerField(db_column='idrbod', primary_key=True, serialize=False)),
                ('diatra', models.TextField(db_column='diatra', verbose_name='Dia de Transaccion')),
                ('oficina', models.TextField(db_column='oficina', verbose_name='Oficina')),
                ('desctra', models.TextField(db_column='desctra', verbose_name='Descripcion de la transaccion')),
                ('debe', models.TextField(db_column='debe')),
                ('haber', models.TextField(db_column='haber')),
                ('saldo', models.TextField(db_column='saldo')),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
            ],
            options={
                'db_table': 'cbrbod',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrenc',
            fields=[
                ('idrenc', models.AutoField(db_column='idrenc', primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(db_column='cliente', max_length=3, verbose_name='Cliente')),
                ('empresa', models.CharField(db_column='empresa', max_length=3, verbose_name='Empresa')),
                ('codbco', models.CharField(db_column='codbco', max_length=5, verbose_name='Banco')),
                ('nrocta', models.CharField(db_column='nrocta', max_length=30, verbose_name='Cuenta')),
                ('ano', models.SmallIntegerField(blank=True, db_column='ano', null=True, verbose_name='Año')),
                ('mes', models.SmallIntegerField(blank=True, db_column='mes', null=True, verbose_name='Mes')),
                ('estado', models.CharField(db_column='estado', max_length=2, verbose_name='Estado')),
                ('corr', models.SmallIntegerField(db_column='corr', default=0, verbose_name='Correlativo')),
                ('archivobco', models.FileField(blank=True, db_column='archivobco', null=True, upload_to=CBR.models.get_path, verbose_name='Archivo del Banco')),
                ('recordbco', models.IntegerField(blank=True, db_column='recordbco', default=0, null=True, verbose_name='Registros de Banco')),
                ('archivoerp', models.FileField(blank=True, db_column='archivoerp', null=True, upload_to=CBR.models.get_path, verbose_name='Archivo del ERP')),
                ('recorderp', models.IntegerField(blank=True, db_column='recorderp', default=0, null=True, verbose_name='Registros de ERP')),
                ('archivoimg', models.FileField(blank=True, db_column='archivoimg', null=True, upload_to=CBR.models.get_path_temp, verbose_name='Imagen del Banco')),
                ('saldobco', models.DecimalField(blank=True, db_column='saldobco', decimal_places=2, max_digits=16, null=True)),
                ('saldobcoori', models.DecimalField(blank=True, db_column='saldobcoori', decimal_places=2, max_digits=16, null=True)),
                ('saldoerp', models.DecimalField(blank=True, db_column='saldoerp', decimal_places=2, max_digits=16, null=True)),
                ('saldoerpori', models.DecimalField(blank=True, db_column='saldoerpori', decimal_places=2, max_digits=16, null=True)),
                ('difbcoerp', models.DecimalField(blank=True, db_column='difbcoerp', decimal_places=2, max_digits=16, null=True)),
                ('fechacons', models.DateTimeField(db_column='fechact', null=True, verbose_name='Fecha de conciliación')),
                ('idusucons', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario que realizó la última operación')),
            ],
            options={
                'db_table': 'cbrenc',
                'managed': True,
                'unique_together': {('empresa', 'cliente', 'codbco', 'nrocta', 'ano', 'mes', 'corr')},
            },
        ),
        migrations.CreateModel(
            name='Cbrenci',
            fields=[
                ('idrenci', models.AutoField(db_column='idrenci', primary_key=True, serialize=False, verbose_name='id')),
                ('idrenc', models.IntegerField(db_column='idrenc', verbose_name='idrenc')),
                ('imgbco', models.BinaryField(db_column='imgbco', editable=True, null=True, verbose_name='Imagen de banco')),
                ('archivotipo', models.CharField(db_column='archivotipo', default='PDF', max_length=4, verbose_name='Tipo de Archivo')),
            ],
            options={
                'db_table': 'cbrenci',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrgal',
            fields=[
                ('idrgal', models.IntegerField(db_column='idrgal', primary_key=True, serialize=False)),
                ('fechatra', models.TextField(db_column='fechatra', null=True)),
                ('nrocomp', models.TextField(db_column='nrocomp', null=True, verbose_name='Numero de Comprobante')),
                ('aux', models.TextField(db_column='aux', null=True, verbose_name='Auxiliar')),
                ('ref', models.TextField(db_column='ref', null=True, verbose_name='Referencia')),
                ('glosa', models.TextField(db_column='glosa', null=True, verbose_name='Glosa')),
                ('debe', models.TextField(db_column='debe', null=True)),
                ('haber', models.TextField(db_column='haber', null=True)),
                ('saldo', models.TextField(db_column='saldo', null=True)),
                ('fechacon', models.TextField(blank=True, db_column='fechacon', null=True, verbose_name='Fecha de contabilizacion')),
                ('fechact', models.DateField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrgal',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbsresc',
            fields=[
                ('idsresc', models.IntegerField(db_column='idsresc', primary_key=True, serialize=False, verbose_name='ID')),
                ('idsres', models.IntegerField(db_column='idsres', verbose_name='ID')),
                ('codtco', models.CharField(db_column='codtco', max_length=4, verbose_name='Codtco')),
                ('debebco', models.DecimalField(blank=True, db_column='debebco', decimal_places=2, max_digits=16, null=True)),
                ('haberbco', models.DecimalField(blank=True, db_column='haberbco', decimal_places=2, max_digits=16, null=True)),
                ('debeerp', models.DecimalField(blank=True, db_column='debeerp', decimal_places=2, max_digits=16, null=True)),
                ('habererp', models.DecimalField(blank=True, db_column='habererp', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumesbco', models.DecimalField(blank=True, db_column='saldoacumesbco', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumeserp', models.DecimalField(blank=True, db_column='saldoacumeserp', decimal_places=2, max_digits=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cbtbco',
            fields=[
                ('idtbco', models.AutoField(db_column='idtbco', primary_key=True, serialize=False)),
                ('cliente', models.CharField(db_column='cliente', max_length=3, verbose_name='Cliente')),
                ('empresa', models.CharField(db_column='empresa', max_length=3, verbose_name='Empresa')),
                ('codbco', models.CharField(db_column='codbco', max_length=5, verbose_name='Banco')),
                ('desbco', models.CharField(db_column='desbco', max_length=50, verbose_name='Desbco')),
                ('fechact', models.DateTimeField(db_column='fechact', verbose_name='Fecha de carga Banco')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, verbose_name='Usuario de archivo ERP')),
            ],
            options={
                'db_table': 'cbtbco',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbterr',
            fields=[
                ('idterr', models.AutoField(db_column='idterr', primary_key=True, serialize=False)),
                ('coderr', models.SmallIntegerField(db_column='coderr')),
                ('descerr', models.CharField(db_column='descerr', max_length=30, verbose_name='Descripcion')),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo')),
            ],
            options={
                'db_table': 'cbterr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbttco',
            fields=[
                ('idttco', models.AutoField(db_column='idttco', primary_key=True, serialize=False)),
                ('indtco', models.CharField(db_column='indtco', max_length=1, verbose_name='Tipo de conciliación')),
                ('codtco', models.CharField(db_column='codtco', max_length=4, verbose_name='Codtco')),
                ('destco', models.CharField(db_column='destco', max_length=50, verbose_name='Descripcion tipo de conciliacion')),
                ('ordtco', models.SmallIntegerField(blank=True, db_column='ordtco', null=True)),
                ('erpbco', models.SmallIntegerField(blank=True, db_column='erpbco', null=True)),
                ('inddebhab', models.CharField(blank=True, db_column='inddebhab', max_length=1, null=True)),
                ('indsuma', models.SmallIntegerField(blank=True, db_column='indsuma', null=True)),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
            ],
            options={
                'db_table': 'cbttco',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbwres',
            fields=[
                ('idsres', models.IntegerField(db_column='idsres', primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(db_column='cliente', max_length=3, verbose_name='Cliente')),
                ('empresa', models.CharField(db_column='empresa', max_length=3, verbose_name='Empresa')),
                ('codbco', models.CharField(db_column='codbco', max_length=5, verbose_name='Banco')),
                ('nrocta', models.CharField(db_column='nrocta', max_length=30, verbose_name='Cuenta')),
                ('ano', models.SmallIntegerField(blank=True, db_column='ano', null=True)),
                ('mes', models.SmallIntegerField(blank=True, db_column='mes', null=True)),
                ('fechatrabco', models.DateField(blank=True, db_column='fechatrabco', null=True)),
                ('horatrabco', models.TimeField(blank=True, db_column='horatrabco', null=True)),
                ('debebco', models.DecimalField(blank=True, db_column='debebco', decimal_places=2, max_digits=16, null=True)),
                ('haberbco', models.DecimalField(blank=True, db_column='haberbco', decimal_places=2, max_digits=16, null=True)),
                ('saldobco', models.DecimalField(blank=True, db_column='saldobco', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumesbco', models.DecimalField(blank=True, db_column='saldoacumesbco', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumdiabco', models.DecimalField(blank=True, db_column='saldoacumdiabco', decimal_places=2, max_digits=16, null=True)),
                ('oficina', models.TextField(blank=True, db_column='oficina', null=True)),
                ('desctra', models.TextField(blank=True, db_column='desctra', null=True)),
                ('reftra', models.TextField(blank=True, db_column='reftra', null=True)),
                ('codtra', models.TextField(blank=True, db_column='codtra', null=True)),
                ('idrbcod', models.IntegerField(blank=True, db_column='idrbcod', default=0, null=True)),
                ('nrotraerp', models.TextField(blank=True, db_column='nrotra', null=True)),
                ('fechatraerp', models.DateField(blank=True, db_column='fechatraerp', null=True)),
                ('nrocomperp', models.TextField(blank=True, db_column='nrocomp', null=True)),
                ('auxerp', models.SmallIntegerField(blank=True, db_column='auxerp', null=True)),
                ('referp', models.TextField(blank=True, db_column='referp', null=True)),
                ('glosaerp', models.TextField(blank=True, db_column='glosa', null=True)),
                ('debeerp', models.DecimalField(blank=True, db_column='debeerp', decimal_places=2, max_digits=16, null=True)),
                ('habererp', models.DecimalField(blank=True, db_column='habererp', decimal_places=2, max_digits=16, null=True)),
                ('saldoerp', models.DecimalField(blank=True, db_column='saldoerp', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumeserp', models.DecimalField(blank=True, db_column='saldoacumeserp', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumdiaerp', models.DecimalField(blank=True, db_column='saldoacumdiaerp', decimal_places=2, max_digits=16, null=True)),
                ('fechaconerp', models.DateField(blank=True, db_column='fechaconerp', null=True)),
                ('idrerpd', models.IntegerField(blank=True, db_column='idrerpd', default=0, null=True)),
                ('estadoerp', models.SmallIntegerField(db_column='estado', null=True, verbose_name='Estado Erp')),
                ('estadobco', models.SmallIntegerField(db_column='estadobco', null=True, verbose_name='Estado Banco')),
                ('codtcobco', models.CharField(blank=True, db_column='codtcobco', max_length=4, null=True)),
                ('codtcoerp', models.CharField(blank=True, db_column='codtcoerp', max_length=4, null=True)),
                ('idrbcodl', models.IntegerField(blank=True, db_column='idrbcodl', null=True)),
                ('linkconciliadoerp', models.IntegerField(blank=True, db_column='idrerpdl', null=True)),
                ('saldodiferencia', models.DecimalField(blank=True, db_column='saldodiferencia', decimal_places=2, max_digits=16, null=True)),
                ('historial', models.CharField(db_column='historial', default='0', max_length=1, verbose_name='Historial')),
                ('pautado', models.IntegerField(blank=True, db_column='pautado', null=True)),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbwres',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbtcta',
            fields=[
                ('idtcta', models.IntegerField(db_column='idtcta', primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(db_column='cliente', max_length=3, verbose_name='Cliente')),
                ('empresa', models.CharField(db_column='empresa', max_length=3, verbose_name='Empresa')),
                ('codbco', models.CharField(db_column='codbco', max_length=5, verbose_name='Banco')),
                ('nrocta', models.CharField(db_column='nrocta', max_length=30, verbose_name='Numero de Cuenta')),
                ('descta', models.CharField(db_column='descta', max_length=50, verbose_name='Descripcion de la cuenta')),
                ('monbasebco', models.CharField(db_column='monbasebco', max_length=3, verbose_name='Moneda de base de banco')),
                ('monbaseerp', models.CharField(db_column='monbaseerp', max_length=3, verbose_name='Moneda de base de erp')),
                ('ano', models.SmallIntegerField(blank=True, db_column='ano', null=True, verbose_name='Año')),
                ('mes', models.SmallIntegerField(blank=True, db_column='mes', null=True)),
                ('saldoinibco', models.DecimalField(db_column='saldoinibco', decimal_places=2, max_digits=16, verbose_name='Saldo Inicial Banco')),
                ('saldoinierp', models.DecimalField(db_column='saldoinierp', decimal_places=2, max_digits=16, verbose_name='Saldo Inicial ERP')),
                ('fechact', models.DateTimeField(blank=True, db_column='fechact', null=True, verbose_name='Fecha de carga')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
            ],
            options={
                'db_table': 'cbtcta',
                'managed': True,
                'unique_together': {('empresa', 'cliente', 'codbco', 'nrocta')},
            },
        ),
        migrations.CreateModel(
            name='Cbsres',
            fields=[
                ('idsres', models.AutoField(db_column='idsres', primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(db_column='cliente', max_length=3, verbose_name='Cliente')),
                ('empresa', models.CharField(db_column='empresa', max_length=3, verbose_name='Empresa')),
                ('codbco', models.CharField(db_column='codbco', max_length=5, verbose_name='Banco')),
                ('nrocta', models.CharField(db_column='nrocta', max_length=30, verbose_name='Cuenta')),
                ('ano', models.SmallIntegerField(blank=True, db_column='ano', null=True)),
                ('mes', models.SmallIntegerField(blank=True, db_column='mes', null=True)),
                ('fechatrabco', models.DateField(blank=True, db_column='fechatrabco', null=True)),
                ('horatrabco', models.TimeField(blank=True, db_column='horatrabco', null=True)),
                ('debebco', models.DecimalField(blank=True, db_column='debebco', decimal_places=2, max_digits=16, null=True)),
                ('haberbco', models.DecimalField(blank=True, db_column='haberbco', decimal_places=2, max_digits=16, null=True)),
                ('saldobco', models.DecimalField(blank=True, db_column='saldobco', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumesbco', models.DecimalField(blank=True, db_column='saldoacumesbco', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumdiabco', models.DecimalField(blank=True, db_column='saldoacumdiabco', decimal_places=2, max_digits=16, null=True)),
                ('oficina', models.TextField(blank=True, db_column='oficina', null=True)),
                ('desctra', models.TextField(blank=True, db_column='desctra', null=True)),
                ('reftra', models.TextField(blank=True, db_column='reftra', null=True)),
                ('codtra', models.TextField(blank=True, db_column='codtra', null=True)),
                ('idrbcod', models.IntegerField(blank=True, db_column='idrbcod', default=0, null=True)),
                ('nrotraerp', models.TextField(blank=True, db_column='nrotra', null=True)),
                ('fechatraerp', models.DateField(blank=True, db_column='fechatraerp', null=True)),
                ('nrocomperp', models.TextField(blank=True, db_column='nrocomp', null=True)),
                ('auxerp', models.SmallIntegerField(blank=True, db_column='auxerp', null=True)),
                ('referp', models.TextField(blank=True, db_column='referp', null=True)),
                ('glosaerp', models.TextField(blank=True, db_column='glosa', null=True)),
                ('debeerp', models.DecimalField(blank=True, db_column='debeerp', decimal_places=2, max_digits=16, null=True)),
                ('habererp', models.DecimalField(blank=True, db_column='habererp', decimal_places=2, max_digits=16, null=True)),
                ('saldoerp', models.DecimalField(blank=True, db_column='saldoerp', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumeserp', models.DecimalField(blank=True, db_column='saldoacumeserp', decimal_places=2, max_digits=16, null=True)),
                ('saldoacumdiaerp', models.DecimalField(blank=True, db_column='saldoacumdiaerp', decimal_places=2, max_digits=16, null=True)),
                ('fechaconerp', models.DateField(blank=True, db_column='fechaconerp', null=True)),
                ('idrerpd', models.IntegerField(blank=True, db_column='idrerpd', default=0, null=True)),
                ('estadoerp', models.SmallIntegerField(db_column='estado', null=True, verbose_name='Estado Erp')),
                ('estadobco', models.SmallIntegerField(db_column='estadobco', null=True, verbose_name='Estado Banco')),
                ('codtcobco', models.CharField(blank=True, db_column='codtcobco', max_length=4, null=True)),
                ('codtcoerp', models.CharField(blank=True, db_column='codtcoerp', max_length=4, null=True)),
                ('idrbcodl', models.IntegerField(blank=True, db_column='idrbcodl', null=True)),
                ('linkconciliadoerp', models.IntegerField(blank=True, db_column='idrerpdl', null=True)),
                ('saldodiferencia', models.DecimalField(blank=True, db_column='saldodiferencia', decimal_places=2, max_digits=16, null=True)),
                ('historial', models.CharField(db_column='historial', default='0', max_length=1, verbose_name='Historial')),
                ('pautado', models.IntegerField(blank=True, db_column='pautado', null=True)),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbsres',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrgale',
            fields=[
                ('idrgale', models.AutoField(db_column='idrgale', primary_key=True, serialize=False)),
                ('coderr', models.SmallIntegerField(db_column='coderr', default=0)),
                ('idrgal', models.ForeignKey(db_column='idrgal', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrgal')),
            ],
            options={
                'db_table': 'cbrgale',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrerpe',
            fields=[
                ('idrerpe', models.AutoField(db_column='idrerpe', primary_key=True, serialize=False)),
                ('fechact', models.DateTimeField(db_column='fechact', null=True, verbose_name='Fecha de actualizacion')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de actualizacion')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrerpe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrerpd',
            fields=[
                ('idrerpd', models.AutoField(db_column='idrerpd', primary_key=True, serialize=False)),
                ('nrotra', models.TextField(db_column='nrotra', null=True)),
                ('fechatra', models.DateField(blank=True, db_column='fechatra', null=True)),
                ('nrocomp', models.TextField(db_column='nrocomp', null=True)),
                ('aux', models.SmallIntegerField(blank=True, db_column='aux', null=True)),
                ('ref', models.TextField(db_column='ref')),
                ('glosa', models.TextField(db_column='glosa')),
                ('debe', models.DecimalField(db_column='debe', decimal_places=2, max_digits=16)),
                ('haber', models.DecimalField(db_column='haber', decimal_places=2, max_digits=16)),
                ('saldo', models.DecimalField(db_column='saldo', decimal_places=2, max_digits=16)),
                ('fechacon', models.DateField(blank=True, db_column='fechacon', null=True)),
                ('fechact', models.DateField(blank=True, db_column='fechact', null=True)),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
                ('idrerpe', models.ForeignKey(db_column='idrerpe', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrerpe')),
            ],
            options={
                'db_table': 'cbrerpd',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrenct',
            fields=[
                ('idrenct', models.AutoField(db_column='idrenct', primary_key=True, serialize=False, verbose_name='ID')),
                ('fechoraini', models.DateTimeField(db_column='fechoraini', null=True, verbose_name='Fecha de inicio')),
                ('fechorafin', models.DateTimeField(db_column='fechorafin', null=True, verbose_name='Fecha del Fin')),
                ('tiempodif', models.DurationField(db_column='tiempodif', null=True, verbose_name='Tiempo de Diferencia')),
                ('formulario', models.CharField(db_column='formulario', max_length=5, verbose_name='Formulario')),
                ('accion', models.SmallIntegerField(blank=True, db_column='accion', null=True)),
                ('fechact', models.DateTimeField(db_column='fechact', null=True, verbose_name='Fecha de Actualizacion')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrenct',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrencl',
            fields=[
                ('idrencl', models.AutoField(db_column='idrencl', primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(db_column='status', default=0, verbose_name='Status')),
                ('saldobco', models.DecimalField(blank=True, db_column='saldobco', decimal_places=2, max_digits=16, null=True)),
                ('saldoerp', models.DecimalField(blank=True, db_column='saldoerp', decimal_places=2, max_digits=16, null=True)),
                ('difbcoerp', models.DecimalField(blank=True, db_column='difbcoerp', decimal_places=2, max_digits=16, null=True)),
                ('glosa', models.CharField(db_column='glosa', max_length=60, null=True, verbose_name='Explica la Eliminación')),
                ('fechact', models.DateTimeField(db_column='fechact', null=True, verbose_name='Fecha de actualizacion')),
                ('idusu', models.CharField(db_column='idusu', max_length=16, null=True, verbose_name='Usuario')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrencl',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrbode',
            fields=[
                ('idrbode', models.AutoField(db_column='idrbode', primary_key=True, serialize=False)),
                ('coderr', models.SmallIntegerField(db_column='coderr', default=0)),
                ('idrbod', models.ForeignKey(db_column='idrbod', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrbod')),
            ],
            options={
                'db_table': 'cbrbode',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='cbrbod',
            name='idrenc',
            field=models.ForeignKey(db_column='idrenc', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc'),
        ),
        migrations.CreateModel(
            name='Cbrbcoe',
            fields=[
                ('idrbcoe', models.AutoField(db_column='idrbcoe', primary_key=True, serialize=False)),
                ('fechact1', models.DateTimeField(db_column='fechact1', null=True, verbose_name='Fecha de actualizacion de archivo BCO')),
                ('idusu1', models.CharField(db_column='idusu1', max_length=16, null=True, verbose_name='Usuario de actualizacion de archivo BCO')),
                ('fechact2', models.DateTimeField(db_column='fechact2', null=True, verbose_name='Fecha de actualizacion de archivo ERP')),
                ('idusu2', models.CharField(db_column='idusu2', max_length=16, null=True, verbose_name='Usuario de archivo ERP')),
                ('idrenc', models.ForeignKey(db_column='idrenc', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrenc')),
            ],
            options={
                'db_table': 'cbrbcoe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cbrbcod',
            fields=[
                ('idrbcod', models.AutoField(db_column='idrbcod', primary_key=True, serialize=False)),
                ('fechatra', models.DateField(blank=True, db_column='fechatra', null=True)),
                ('horatra', models.TimeField(blank=True, db_column='horatra', null=True)),
                ('oficina', models.TextField(db_column='oficina')),
                ('desctra', models.TextField(db_column='desctra')),
                ('reftra', models.TextField(db_column='reftra')),
                ('codtra', models.TextField(db_column='codtra')),
                ('debe', models.DecimalField(db_column='debe', decimal_places=2, max_digits=16)),
                ('haber', models.DecimalField(db_column='haber', decimal_places=2, max_digits=16)),
                ('saldo', models.DecimalField(db_column='saldo', decimal_places=2, max_digits=16)),
                ('idrbcoe', models.ForeignKey(db_column='idrbcoe', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrbcoe')),
                ('idrerpd', models.ForeignKey(db_column='idrerpd', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CBR.cbrerpd')),
            ],
            options={
                'db_table': 'cbrbcod',
                'managed': True,
            },
        ),
    ]
