from django.contrib.auth.models import User
from django.db import models, connection
from django.forms import model_to_dict
import datetime as dt
from db_file_storage.storage import DatabaseFileStorage

class Cbrerpe(models.Model):
    idrerpe = models.AutoField(db_column='idrerpe', primary_key=True)
    idrenc=models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    fechact = models.DateTimeField( verbose_name='Fecha de actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario de actualizacion', db_column='idusu', max_length=16, null=True )

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrerpe'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrerpe, self ).save( *args, **kwargs )
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        # args[0].idusubco = User.username
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#


class Cbrbcoe(models.Model):
    idrbcoe = models.AutoField(db_column='idrbcoe', primary_key=True)
    fechact1 = models.DateTimeField( verbose_name='Fecha de actualizacion de archivo BCO', db_column='fechact1', null=True)
    idusu1 = models.CharField( verbose_name='Usuario de actualizacion de archivo BCO', db_column='idusu1', max_length=16, null=True )
    fechact2 = models.DateTimeField( verbose_name='Fecha de actualizacion de archivo ERP', db_column='fechact2', null=True)
    idusu2 = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu2', max_length=16, null=True )
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrbcoe'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrbcoe, self ).save( *args, **kwargs )
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        # args[0].idusubco = User.username
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbtcta(models.Model):
    idtcta = models.IntegerField(verbose_name='ID', db_column='idtcta', primary_key=True)
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=3)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=3)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    nrocta = models.CharField(verbose_name='Numero de Cuenta', db_column='nrocta', max_length=30)
    descta = models.CharField(verbose_name='Descripcion de la cuenta', db_column='descta', max_length=50)
    monbasebco = models.CharField(verbose_name='Moneda de base de banco', db_column='monbasebco', max_length=3)
    monbaseerp = models.CharField(verbose_name='Moneda de base de erp', db_column='monbaseerp', max_length=3)
    ano = models.SmallIntegerField(verbose_name='Año',db_column='ano', blank=True, null=True)
    mes = models.SmallIntegerField(db_column='mes', blank=True, null=True)
    saldoinibco = models.DecimalField(verbose_name='Saldo Inicial Banco', db_column='saldoinibco', max_digits=16, decimal_places=2)
    saldoinierp = models.DecimalField(verbose_name='Saldo Inicial ERP',db_column='saldoinierp', max_digits=16, decimal_places=2)
    fechact = models.DateTimeField(verbose_name='Fecha de carga', db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbtcta'  # Para que en la migracion no ponga el prefijo de la app
        unique_together=(('empresa', 'cliente', 'codbco', 'nrocta'),)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbtcta, self ).save( *args, **kwargs )

        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbttco(models.Model):
    idttco = models.AutoField(db_column='idttco', primary_key=True)
    indtco = models.CharField(verbose_name='Tipo de conciliación', db_column='indtc', max_length=1)
    codtco = models.CharField(verbose_name='Codtco', db_column='codtco', max_length=4)
    destco = models.CharField(verbose_name='Descripcion tipo de conciliacion', db_column='destco', max_length=80)
    masmenos = models.SmallIntegerField(db_column='masmenos', blank=True, null=True)
    ordencb010 = models.SmallIntegerField(db_column='ordencbo10', blank=True, null=True)
    fechact = models.DateTimeField(verbose_name='Fecha de carga', db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbttco'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbttco, self ).save( *args, **kwargs )

        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#


class Cbtbco(models.Model):
    idtbco = models.AutoField(db_column='idtbco', primary_key=True)
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=3)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=3)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    desbco = models.CharField(verbose_name='Desbco', db_column='desbco', max_length=50)
    fechactbco = models.DateTimeField(verbose_name='Fecha de carga Banco', db_column='fechactbco', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbtbco'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbtbco, self ).save( *args, **kwargs )

        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrbcod(models.Model):
    idrbcod = models.AutoField(db_column='idrbcod', primary_key=True)
    idrbcoe = models.ForeignKey( 'Cbrbcoe', models.DO_NOTHING, db_column='idrbcoe', default=0 )
    fechatra = models.DateField(db_column='fechatra', blank=True, null=True)
    horatra = models.TimeField(db_column='horatra', blank=True, null=True)
    oficina = models.TextField(db_column='oficina')
    desctra = models.TextField(db_column='desctra')
    reftra = models.TextField(db_column='reftra')
    codtra = models.TextField(db_column='codtra')
    debe = models.DecimalField(db_column='debe', max_digits=16, decimal_places=2)
    haber = models.DecimalField(db_column='haber', max_digits=16, decimal_places=2)
    saldo = models.DecimalField(db_column='saldo', max_digits=16, decimal_places=2)
    idrerpd = models.ForeignKey('Cbrerpd', models.DO_NOTHING, db_column='idrerpd', null=True)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrbcod'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrbcod, self ).save( *args, **kwargs )
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        # args[0].idusubco = User.username

        args[0].fechactbco=dt.datetime.today()
        #args[0].recordbco = Cbrbcod.objects.filter( idrenc=self.idrenc_id).count()
        #args[0].save()
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrerpd(models.Model):
    idrerpd = models.AutoField(db_column='idrerpd', primary_key=True)
    idrerpe = models.ForeignKey( 'Cbrerpe', models.DO_NOTHING, db_column='idrerpe', default=0 )
    nrotra = models.TextField(db_column='nrotra', null=True)
    fechatra = models.DateField(db_column='fechatra', blank=True, null=True)
    nrocomp = models.TextField(db_column='nrocomp', null=True)
    aux = models.SmallIntegerField(db_column='aux', blank=True, null=True)
    ref = models.TextField(db_column='ref')
    glosa = models.TextField(db_column='glosa')
    debe = models.DecimalField(db_column='debe', max_digits=16, decimal_places=2)
    haber = models.DecimalField(db_column='haber', max_digits=16, decimal_places=2)
    saldo = models.DecimalField(db_column='saldo', max_digits=16, decimal_places=2)
    fechacon = models.DateField(db_column='fechacon', blank=True, null=True)
    fechact = models.DateField(db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )


    class Meta:
        managed = True
        db_table = 'cbrerpd'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super(Cbrerpd, self).save(*args, **kwargs)
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        args[0].fechacterp = dt.datetime.today()
        args[0].recorderp = Cbrerpd.objects.filter(idrerpe=self.idrerpe_id).count()
        args[0].save()
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#


class Cbrenc(models.Model):
    idrenc = models.AutoField(verbose_name='ID', db_column='idrenc', primary_key=True)
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=3)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=3)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    nrocta = models.CharField(verbose_name='Cuenta', db_column='nrocta', max_length=30)
    ano = models.SmallIntegerField(verbose_name='Año', db_column='ano', blank=True, null=True)
    mes = models.SmallIntegerField(verbose_name='Mes', db_column='mes', blank=True, null=True)
    estado = models.CharField(verbose_name='Estado', db_column='estado', max_length=2)
    corr = models.SmallIntegerField(verbose_name='Correlativo', db_column='corr', default=0)
    # status_desc=models.SmallIntegerField( verbose_name='Status', db_column='STATUS', default=0 )
    #fechalt =models.DateTimeField( verbose_name='Fecha de creación', db_column='FECHALT', null=True )
    #idusualt =models.CharField(verbose_name='Usuario alta', db_column='IDUSUALT', max_length=16, null=True )
    #fechmod=models.DateTimeField( verbose_name='Fecha de Modificado', db_column='FECHMOD', null=True )
    #idusumod =models.CharField(verbose_name='Usuario modificó', db_column='IDUSUMOD', max_length=16, null=True )
    archivobco = models.FileField(verbose_name='Archivo del Banco', db_column='archivobco', upload_to='upload_files/%Y/%m/%d', null=True, blank=True)
    #fechactbco = models.DateTimeField(verbose_name='Fecha de carga Banco', db_column='FECHACTBCO', blank=True, null=True)
    #idusubco = models.CharField(verbose_name='Usuario carga Banco', db_column='IDUSUBCO', max_length=16, blank=True, null=True)
    recordbco = models.IntegerField(verbose_name='Registros de Banco', db_column='recordbco', default=0, blank=True, null=True)
    archivoerp = models.FileField(verbose_name='Archivo del ERP', db_column='archivoerp', upload_to='upload_files/%Y/%m/%d', null=True, blank=True)
    #fechacterp = models.DateTimeField(verbose_name='Fecha de carga ERP', db_column='FECHACTERP', blank=True, null=True)
    #idusuerp = models.CharField(verbose_name='Usuario carga ERP', db_column='IDUSUERP', max_length=16, blank=True, null=True)
    recorderp = models.IntegerField(verbose_name='Registros de ERP', db_column='recorderp', default=0, blank=True, null=True)
    imgbcoroute = models.FileField(verbose_name='Imagen del Banco', storage= DatabaseFileStorage,upload_to='CBR.Cbrenci/imgbco/imgbconame/imgbcomime',blank=True, null=True)
    saldobco =models.DecimalField( db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoerp =models.DecimalField( db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True )
    difbcoerp =models.DecimalField( db_column='difbcoerp', max_digits=16, decimal_places=2, blank=True, null=True )    
    fechacons=models.DateTimeField( verbose_name='Fecha de conciliación', db_column='fechact', null=True)
    idusucons=models.CharField( verbose_name='Usuario que realizó la última operación', db_column='idusu', max_length=16, null=True )
    def toJSON(self):
        item = model_to_dict(self)
        return item

    # def __str__(self):
    #     return str(self.idrenc)
    def save(self, *args, **kwargs):

        # if self:
        #     self.fechalt = dt.datetime.today()
        #     self.idusualt = User.username
        # else:
        #     self.fechmod = dt.datetime.today()
        #     self.idusumod = User.username
        
        self.cliente = "PMA"

        super( Cbrenc, self ).save( *args, **kwargs )


    class Meta:
        managed = True
        db_table = 'cbrenc'  # Para que en la migracion no ponga el prefijo de la app
        unique_together=(('empresa', 'cliente', 'codbco', 'nrocta', 'ano', 'mes', 'corr'),)
       # ordening = ['codbco']

#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrenci(models.Model):
    idrenc = models.IntegerField( db_column='idrenc', primary_key=True, default = 1005)
    imgbconame = models.CharField(max_length=255,null=True)
    imgbcomime = models.CharField(max_length=50,null=True)
    imgbco = models.BinaryField( verbose_name='Imagen de banco', db_column = "imgbco", editable=True, null=True)
    def save(self, *args, **kwargs):
        super( Cbrenci, self ).save( *args, **kwargs )
    class Meta:
        managed = True
        db_table = 'cbrenci'  # Para que en la migracion no ponga el prefijo de la app

#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrencl(models.Model):

    idrencl = models.AutoField(verbose_name='ID', db_column='idrencl', primary_key=True)
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    status = models.SmallIntegerField(verbose_name='Status', db_column='status', default=0)
    saldobco = models.DecimalField( db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoerp = models.DecimalField( db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True )
    difbcoerp = models.DecimalField( db_column='difbcoerp', max_digits=16, decimal_places=2, blank=True, null=True )
    glosa = models.CharField( verbose_name='Explica la Eliminación', db_column='glosa', max_length=60, null=True )
    fechact = models.DateTimeField( verbose_name='Fecha de actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    def toJSON(self):
        item = model_to_dict(self)
        return item

    # def __str__(self):
    #     return str(self.idrenc)
    def save(self, *args, **kwargs):
        super( Cbrencl, self ).save( *args, **kwargs )


    class Meta:
        managed = True
        db_table = 'cbrencl'  # Para que en la migracion no ponga el prefijo de la app
       # ordening = ['codbco']

#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrenct(models.Model):

    idrenct = models.AutoField(verbose_name='ID', db_column='idrenct', primary_key=True)
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    fechoraini = models.DateTimeField( verbose_name='Fecha de inicio', db_column='fechoraini', null=True)
    fechorafin = models.DateTimeField( verbose_name='Fecha del Fin', db_column='fechorafin', null=True)
    tiempodif = models.DurationField( verbose_name='Tiempo de Diferencia', db_column='tiempodif', null=True)
    formulario = models.CharField( verbose_name='Formulario', db_column='formulario', max_length=5 )
    accion = models.SmallIntegerField(db_column='accion', blank=True, null=True)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    def toJSON(self):
        item = model_to_dict(self)
        return item

    # def __str__(self):
    #     return str(self.idrenc)
    def save(self, *args, **kwargs):
        super( Cbrenct, self ).save( *args, **kwargs )


    class Meta:
        managed = True
        db_table = 'cbrenct'  # Para que en la migracion no ponga el prefijo de la app
       # ordening = ['codbco']

#**********************************************************************************************************************#
#**********************************************************************************************************************#
class Cbsres(models.Model):
    idsres = models.AutoField( verbose_name='ID', db_column='idsres', primary_key=True )
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=3)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=3)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    nrocta = models.CharField(verbose_name='Cuenta', db_column='nrocta', max_length=30)
    ano = models.SmallIntegerField(db_column='ano', blank=True, null=True)
    mes = models.SmallIntegerField(db_column='mes', blank=True, null=True)

    # -----------------------------------------------------------------------------------------------------------------
    fechatrabco = models.DateField(db_column='fechatrabco', blank=True, null=True)
    horatrabco = models.TimeField(db_column='horatrabco', blank=True, null=True)
    debebco = models.DecimalField(db_column='debebco', max_digits=16, decimal_places=2, blank=True, null=True)
    haberbco = models.DecimalField(db_column='haberbco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldobco = models.DecimalField(db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumesbco = models.DecimalField( db_column='saldoacumesbco', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiabco = models.DecimalField( db_column='saldoacumdiabco', max_digits=16, decimal_places=2, blank=True, null=True )
    oficinabco = models.CharField(db_column='oficinabco', max_length=30, blank=True, null=True)
    desctrabco = models.CharField(db_column='desctrabco', max_length=30, blank=True, null=True)
    reftrabco = models.CharField(db_column='reftrabco', max_length=30, blank=True, null=True)
    codtrabco = models.CharField(db_column='codtrabco', max_length=30, blank=True, null=True)
    idrbcod = models.IntegerField( db_column='idrbcod', blank=True, null=True, default=0 )
    # -----------------------------------------------------------------------------------------------------------------
    nrotraerp = models.IntegerField(db_column='nrotraerp', blank=True, null=True)
    fechatraerp = models.DateField(db_column='fechatraerp', blank=True, null=True)
    nrocomperp = models.IntegerField(db_column='nrocomperp', blank=True, null=True)
    auxerp = models.IntegerField(db_column='auxerp', blank=True, null=True)
    referp = models.CharField(db_column='referp', max_length=30, blank=True, null=True)
    glosaerp = models.CharField(db_column='glosaerp', max_length=30, blank=True, null=True)
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoerp = models.DecimalField(db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumeserp = models.DecimalField( db_column='saldoacumeserp', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiaerp = models.DecimalField( db_column='saldoacumdiaerp', max_digits=16, decimal_places=2, blank=True, null=True )       
    fechaconerp = models.DateField(db_column='fechaconerp', blank=True, null=True)
    idrerpd = models.IntegerField( db_column='idrerpd', blank=True, null=True, default=0  )
    isconciliado = models.BigIntegerField(db_column='isconciliado', blank=True, null=True)
    saldodiferencia = models.DecimalField( db_column='saldodiferencia', max_digits=16, decimal_places=2, blank=True, null=True )
    estado=models.CharField( verbose_name='Estado', db_column='estado', max_length=2 )
    historial=models.CharField( verbose_name='Historial', db_column='historial', max_length=1, default = "0" )
    linkconciliado = models.IntegerField(db_column='linkconciliado', blank=True, null=True)
    tipoconciliado = models.CharField(db_column='tipoconciliado', blank=True, null=True, max_length=4)
    blockcolor = models.IntegerField(db_column='blockcolor', blank=True, null=True)
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        managed = True
        db_table = 'cbsres'  # Para que en la migracion no ponga el prefijo de la app


class Cbwres(models.Model):
    idsres = models.IntegerField( verbose_name='ID', db_column='idsres', primary_key=True )
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=3)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=3)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    nrocta = models.CharField(verbose_name='Cuenta', db_column='nrocta', max_length=30)
    ano = models.SmallIntegerField(db_column='ano', blank=True, null=True)
    mes = models.SmallIntegerField(db_column='mes', blank=True, null=True)

    # -----------------------------------------------------------------------------------------------------------------
    fechatrabco = models.DateField(db_column='fechatrabco', blank=True, null=True)
    horatrabco = models.TimeField(db_column='horatrabco', blank=True, null=True)
    debebco = models.DecimalField(db_column='debebco', max_digits=16, decimal_places=2, blank=True, null=True)
    haberbco = models.DecimalField(db_column='haberbco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldobco = models.DecimalField(db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumesbco = models.DecimalField( db_column='saldoacumesbco', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiabco = models.DecimalField( db_column='saldoacumdiabco', max_digits=16, decimal_places=2, blank=True, null=True )
    oficinabco = models.CharField(db_column='oficinabco', max_length=30, blank=True, null=True)
    desctrabco = models.CharField(db_column='desctrabco', max_length=30, blank=True, null=True)
    reftrabco = models.CharField(db_column='reftrabco', max_length=30, blank=True, null=True)
    codtrabco = models.CharField(db_column='codtrabco', max_length=30, blank=True, null=True)
    idrbcod = models.IntegerField( db_column='idrbcod', blank=True, null=True, default=0 )
    # -----------------------------------------------------------------------------------------------------------------
    nrotraerp = models.IntegerField(db_column='nrotraerp', blank=True, null=True)
    fechatraerp = models.DateField(db_column='fechatraerp', blank=True, null=True)
    nrocomperp = models.IntegerField(db_column='nrocomperp', blank=True, null=True)
    auxerp = models.IntegerField(db_column='auxerp', blank=True, null=True)
    referp = models.CharField(db_column='referp', max_length=30, blank=True, null=True)
    glosaerp = models.CharField(db_column='glosaerp', max_length=30, blank=True, null=True)
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoerp = models.DecimalField(db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumeserp = models.DecimalField( db_column='saldoacumeserp', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiaerp = models.DecimalField( db_column='saldoacumdiaerp', max_digits=16, decimal_places=2, blank=True, null=True )       
    fechaconerp = models.DateField(db_column='fechaconerp', blank=True, null=True)
    idrerpd = models.IntegerField( db_column='idrerpd', blank=True, null=True, default=0  )

    isconciliado = models.BigIntegerField(db_column='isconciliado', blank=True, null=True)
    saldodiferencia = models.DecimalField( db_column='saldodiferencia', max_digits=16, decimal_places=2, blank=True, null=True )
    estado=models.CharField( verbose_name='Estado', db_column='estado', max_length=2 )
    historial=models.CharField( verbose_name='Historial', db_column='historial', max_length=1, default = "0" )
    linkconciliado = models.IntegerField(db_column='linkconciliado', blank=True, null=True)
    tipoconciliado = models.CharField(db_column='tipoconciliado', blank=True, null=True, max_length=4)
    blockcolor = models.IntegerField(db_column='blockcolor', blank=True, null=True)
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        managed = True
        db_table = 'cbwres'  # Para que en la migracion no ponga el prefijo de la app
#**********************************************************************************************************************#

