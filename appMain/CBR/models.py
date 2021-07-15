from django.contrib.auth.models import User
from django.db import models, connection
from django.forms import model_to_dict
import datetime as dt

class Cbrbcod(models.Model):
    idrbcod = models.AutoField(db_column='IDRBCOD', primary_key=True)
    fechatra = models.DateField(db_column='FECHATRA', blank=True, null=True)
    horatra = models.TimeField(db_column='HORATRA', blank=True, null=True)
    oficina = models.CharField(db_column='OFICINA', max_length=30)
    desctra = models.CharField(db_column='DESCTRA', max_length=30)
    reftra = models.CharField(db_column='REFTRA', max_length=30)
    codtra = models.CharField(db_column='CODTRA', max_length=30)
    debe = models.DecimalField(db_column='DEBE', max_digits=16, decimal_places=2)
    haber = models.DecimalField(db_column='HABER', max_digits=16, decimal_places=2)
    saldo = models.DecimalField(db_column='SALDO', max_digits=16, decimal_places=2)
    idrenc = models.ForeignKey('Cbrenc', models.DO_NOTHING, db_column='IDRENC', default=0)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'CBRBCOD'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrbcod, self ).save( *args, **kwargs )
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        # args[0].idusubco = User.username

        args[0].fechactbco=dt.datetime.today()
        args[0].recordbco = Cbrbcod.objects.filter( idrenc=self.idrenc_id).count()
        args[0].save()
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrerpd(models.Model):
    idrerpd = models.AutoField(db_column='IDRERPD', primary_key=True)
    nrotra = models.IntegerField(db_column='NROTRA', blank=True, null=True)
    fechatra = models.DateField(db_column='FECHATRA', blank=True, null=True)
    nrocomp = models.IntegerField(db_column='NROCOMP', blank=True, null=True)
    aux = models.SmallIntegerField(db_column='AUX', blank=True, null=True)
    ref = models.CharField(db_column='REF', max_length=30)
    glosa = models.CharField(db_column='GLOSA', max_length=30)
    debe = models.DecimalField(db_column='DEBE', max_digits=16, decimal_places=2)
    haber = models.DecimalField(db_column='HABER', max_digits=16, decimal_places=2)
    saldo = models.DecimalField(db_column='SALDO', max_digits=16, decimal_places=2)
    fechacon = models.DateField(db_column='FECHACON', blank=True, null=True)
    idrenc=models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='IDRENC', default=0 )

    class Meta:
        managed = True
        db_table = 'CBRERPD'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super(Cbrerpd, self).save(*args, **kwargs)
        # ACTUALIZA NUMERO DE REGISTROS DE LA CARGA EN EL ENCABEZADO #
        args[0].fechacterp = dt.datetime.today()
        args[0].recorderp = Cbrerpd.objects.filter(idrenc=self.idrenc_id).count()
        args[0].save()
        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrenc(models.Model):

    idrenc = models.AutoField(verbose_name='ID', db_column='IDRENC', primary_key=True)
    codbanco = models.CharField(verbose_name='Banco', db_column='CODBANCO', max_length=5)
    nrocta = models.CharField(verbose_name='Cuenta', db_column='nrocta', max_length=30)
    ano = models.SmallIntegerField(verbose_name='Año', db_column='ANO', blank=True, null=True)
    mes = models.SmallIntegerField(verbose_name='Mes', db_column='MES', blank=True, null=True)
    status = models.SmallIntegerField(verbose_name='Status', db_column='STATUS', default=0)
    # status_desc=models.SmallIntegerField( verbose_name='Status', db_column='STATUS', default=0 )
    fechalt =models.DateTimeField( verbose_name='Fecha de creación', db_column='FECHALT', null=True )
    idusualt =models.CharField(verbose_name='Usuario alta', db_column='IDUSUALT', max_length=16, null=True )
    fechmod=models.DateTimeField( verbose_name='Fecha de Modificado', db_column='FECHMOD', null=True )
    idusumod =models.CharField(verbose_name='Usuario modificó', db_column='IDUSUMOD', max_length=16, null=True )

    archivobco = models.FileField(verbose_name='Archivo del Banco', db_column='ARCHIVOBCO', upload_to='upload_files/%Y/%m/%d', null=True, blank=True)
    fechactbco = models.DateTimeField(verbose_name='Fecha de carga Banco', db_column='FECHACTBCO', blank=True, null=True)
    idusubco = models.CharField(verbose_name='Usuario carga Banco', db_column='IDUSUBCO', max_length=16, blank=True, null=True)
    recordbco = models.IntegerField(verbose_name='Registros de Banco', db_column='RECORDBCO', default=0, blank=True, null=True)

    archivoerp = models.FileField(verbose_name='Archivo del ERP', db_column='ARCHIVOERP', upload_to='upload_files/%Y/%m/%d', null=True, blank=True)
    fechacterp = models.DateTimeField(verbose_name='Fecha de carga ERP', db_column='FECHACTERP', blank=True, null=True)
    idusuerp = models.CharField(verbose_name='Usuario carga ERP', db_column='IDUSUERP', max_length=16, blank=True, null=True)
    recorderp = models.IntegerField(verbose_name='Registros de ERP', db_column='RECORDERP', default=0, blank=True, null=True)

    fechacons=models.DateTimeField( verbose_name='Fecha de conciliación', db_column='FECHACONS', null=True)
    idusucons=models.CharField( verbose_name='Usuario que ejecutó la conciliación', db_column='IDUSUCONS', max_length=16, null=True )

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
        if (self.status != 4):
            if (self.recorderp == 0 and self.recordbco == 0):
                self.status=0
            if (self.recorderp > 0 and self.recordbco > 0 ):
                if (self.recorderp != self.recordbco ):
                    self.status=1
                else:
                    if (self.fechacons):
                        self.status=3
                    else:
                        self.status=2
        super( Cbrenc, self ).save( *args, **kwargs )


    class Meta:
        managed = True
        db_table = 'CBRENC'  # Para que en la migracion no ponga el prefijo de la app
        unique_together=(('codbanco', 'nrocta', 'ano', 'mes'),)
       # ordening = ['codbanco']

#**********************************************************************************************************************#
#**********************************************************************************************************************#
class Cbsres(models.Model):
    idsres=models.AutoField( verbose_name='ID', db_column='IDSRES', primary_key=True )
    idrenc=models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='IDRENC', default=0 )
    idrbcod=models.IntegerField( db_column='IDRBCOD', blank=True, null=True, default=0 )
    idrerpd=models.IntegerField( db_column='IDRERPD', blank=True, null=True, default=0  )
    saldoacumesbco=models.DecimalField( db_column='SALDOACUMESBCO', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiabco=models.DecimalField( db_column='SALDOACUMDIABCO', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumeserp=models.DecimalField( db_column='SALDOACUMESERP', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiaerp=models.DecimalField( db_column='SALDOACUMDIAERP', max_digits=16, decimal_places=2, blank=True, null=True )
    saldodiferencia=models.DecimalField( db_column='SALDODIFERENCIA', max_digits=16, decimal_places=2, blank=True, null=True )
    isconciliado=models.BigIntegerField(db_column='ISCONCILIADO', blank=True, null=True)

    numrec=models.BigIntegerField( db_column='numrec', blank=True, null=True )
    estado=models.CharField( verbose_name='Estado', db_column='ESTADO', max_length=1 )
    historial=models.CharField( verbose_name='Historial', db_column='HISTORIAL', max_length=1 )
    # -----------------------------------------------------------------------------------------------------------------
    fechatrabco = models.DateField(db_column='fechatrabco', blank=True, null=True)
    horatrabco = models.TimeField(db_column='horatrabco', blank=True, null=True)
    debebco = models.DecimalField(db_column='debebco', max_digits=16, decimal_places=2, blank=True, null=True)
    haberbco = models.DecimalField(db_column='haberbco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldobco = models.DecimalField(db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True)
    oficinabco = models.CharField(db_column='oficinabco', max_length=30, blank=True, null=True)
    desctrabco = models.CharField(db_column='desctrabco', max_length=30, blank=True, null=True)
    reftrabco = models.CharField(db_column='reftrabco', max_length=30, blank=True, null=True)
    codtrabco = models.CharField(db_column='codtrabco', max_length=30, blank=True, null=True)
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
    fechacon_erp = models.DateField(db_column='FECHACON_ERP', blank=True, null=True)
    blockcolor=models.BigIntegerField( db_column='BLOCKCOLOR', blank=True, null=True )
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        managed = True
        db_table = 'CBSRES'  # Para que en la migracion no ponga el prefijo de la app

class VwConciliacion(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    idrenc = models.IntegerField(db_column='IDRENC', blank=True, null=True)  
    idrbcod_bco = models.IntegerField(db_column='IDRBCOD_BCO', blank=True, null=True)  
    fechatrabco = models.DateField(db_column='fechatrabco', blank=True, null=True)  
    horatrabco = models.TimeField(db_column='horatrabco', blank=True, null=True)  
    debebco = models.DecimalField(db_column='debebco', max_digits=16, decimal_places=2, blank=True, null=True)
    haberbco = models.DecimalField(db_column='haberbco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldobco = models.DecimalField(db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True)
    oficinabco = models.CharField(db_column='oficinabco', max_length=30, blank=True, null=True)  
    desctrabco = models.CharField(db_column='desctrabco', max_length=30, blank=True, null=True)  
    reftrabco = models.CharField(db_column='reftrabco', max_length=30, blank=True, null=True)  
    codtrabco = models.CharField(db_column='codtrabco', max_length=30, blank=True, null=True)  
    idrerpd_erp = models.IntegerField(db_column='IDRERPD_ERP', blank=True, null=True)  
    nrotraerp = models.IntegerField(db_column='nrotraerp', blank=True, null=True)  
    fechatraerp = models.DateField(db_column='fechatraerp', blank=True, null=True)  
    nrocomperp = models.IntegerField(db_column='nrocomperp', blank=True, null=True)  
    auxerp = models.IntegerField(db_column='auxerp', blank=True, null=True)  
    referp = models.CharField(db_column='referp', max_length=30, blank=True, null=True)  
    glosaerp = models.CharField(db_column='glosaerp', max_length=30, blank=True, null=True)  
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoerp = models.DecimalField(db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True)
    fechacon_erp = models.DateField(db_column='FECHACON_ERP', blank=True, null=True)  
    isconciliado = models.IntegerField(blank=True, null=True)
    numrec = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_conciliacion'
        # ordering=['-id']
        # ordering=['fechatrabco', 'horatrabco']

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def getDataSet(idrenc=0, first=False):
        qryDataSet = connection.cursor()
        try:
            qryDataSet.execute( ''' SELECT * FROM vw_conciliacion WHERE "IDRENC" = ''' + str( idrenc ) +
                                ' ORDER BY "fechatrabco", "horatrabco"')
            results=[dict( (qryDataSet.description[i][0], value) \
                           for i, value in enumerate( row ) ) for row in qryDataSet.fetchall()]
        finally:
            qryDataSet.connection.close()
        return (results[0] if results else None) if first else results

#**********************************************************************************************************************#

