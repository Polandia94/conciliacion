# -*- coding: utf-8 -*-



#from typing_extensions import TypeGuard
from django.contrib.auth.models import User
from django.db import models, connection
from django.db.models import CheckConstraint, Q, F
from django.db.models.fields import NullBooleanField
from django.forms import model_to_dict
import datetime as dt
import os
from django.contrib.auth.hashers import make_password

def get_path(instance, filename):
    ahora = dt.datetime.now()
    filename = filename.encode("ascii", "ignore")
    filename = filename.decode("ascii", "ignore")
    path = "upload_files/"+str(ahora.year)+"/"+ str(ahora.month)+ "/" + str(ahora.day) + "/" + filename
    return path

def get_path_temp(instance, filename):
    filename = filename.encode("ascii", "ignore")
    filename = filename.decode("ascii", "ignore")
    path = "temp/"+ filename
    return path

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
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    nrocta = models.CharField(verbose_name='Numero de Cuenta', db_column='nrocta', max_length=30)
    descta = models.CharField(verbose_name='Descripcion de la cuenta', db_column='descta', max_length=50)
    monbasebco = models.CharField(verbose_name='Moneda', db_column='monbasebco', max_length=3)
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
    indtco = models.CharField(verbose_name='Tipo de conciliación', db_column='indtco', max_length=1)
    codtco = models.CharField(verbose_name='Codtco', db_column='codtco', max_length=4)
    destco = models.CharField(verbose_name='Descripcion tipo de conciliacion', db_column='destco', max_length=50)
    ordtco = models.SmallIntegerField(db_column='ordtco', blank=True, null=True)
    erpbco = models.SmallIntegerField(db_column='erpbco', blank=True, null=True)
    inddebhab = models.CharField(db_column='inddebhab', blank=True, null=True, max_length=1)
    indsuma = models.SmallIntegerField(db_column='indsuma', blank=True, null=True)
    indpend = models.SmallIntegerField(db_column='indpend', blank=True, null=True)
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

class Cbrbod(models.Model):
    idrbod = models.AutoField(db_column='idrbod', primary_key=True)
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0, null=True )
    diatra = models.TextField(verbose_name='Dia de Transaccion', db_column='diatra')
    oficina = models.TextField(verbose_name='Oficina', db_column='oficina')
    desctra = models.TextField(verbose_name='Descripcion de la transaccion', db_column='desctra')
    debe = models.TextField(db_column='debe')
    haber = models.TextField(db_column='haber')
    saldo = models.TextField(db_column='saldo')
    fechact = models.DateTimeField(verbose_name='Fecha de carga', db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrbod'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item


        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#

class Cbrgal(models.Model):
    idrgal = models.AutoField(db_column='idrgal', primary_key=True)
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0, null=True )
    fechatra = models.TextField(db_column='fechatra', null=True)
    nrocomp = models.TextField(verbose_name='Numero de Comprobante', db_column='nrocomp', null=True)
    aux = models.TextField(verbose_name='Auxiliar', db_column='aux', null=True)
    ref = models.TextField(verbose_name='Referencia', db_column='ref', null=True)
    glosa = models.TextField(verbose_name='Glosa', db_column='glosa', null=True)
    debe = models.TextField(db_column='debe', null=True)
    haber = models.TextField(db_column='haber', null=True)
    saldo = models.TextField(db_column='saldo', null=True)
    fechacon = models.TextField(verbose_name='Fecha de contabilizacion', db_column='fechacon', blank=True, null=True)
    fechact = models.DateField(verbose_name='Fecha de carga', db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16, null=True )
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrgal'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrgal, self ).save( *args, **kwargs )

    def actualizar(self, *args, **kwargs):
        if Cbrgal.objects.filter(idrgal=self.idrgal).first().idrenc != None and Cbrgal.objects.filter(idrgal=self.idrgal).first().idrenc != "null":
            Cbrgal.objects.filter(idrgal=self.idrgal).delete()
            try:
                self.idrgal = Cbrgal.objects.order_by('-idrgal')[0].idrgal + 1
            except:
                self.idrgal=1
            super( Cbrgal, self ).save( *args, **kwargs )


        # - - - - - - - - - - - - - - - - - - - - - - - - #


#**********************************************************************************************************************#
#**********************************************************************************************************************#


class Cbtbco(models.Model):
    idtbco = models.AutoField(db_column='idtbco', primary_key=True)
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    codbco = models.CharField(verbose_name='Banco', db_column='codbco', max_length=5)
    actpas = models.CharField(verbose_name='Activo o Pasivo', db_column='actpas', max_length=1)
    fechact = models.DateTimeField(verbose_name='Fecha de carga Banco', db_column='fechact')
    idusu = models.CharField( verbose_name='Usuario de archivo ERP', db_column='idusu', max_length=16 )
    
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

class Cbrgale(models.Model):
    idrgale = models.AutoField(db_column='idrgale', primary_key=True)
    idrgal = models.ForeignKey( 'Cbrgal', models.DO_NOTHING, db_column='idrgal', default=0, null=True )
    coderr = models.SmallIntegerField( db_column='coderr', default=0 )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrgale'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrgale, self ).save( *args, **kwargs )

        # 
#**********************************************************************************************************************#
#**********************************************************************************************************************#
class Cbrbode(models.Model):
    idrbode = models.AutoField(db_column='idrbode', primary_key=True)
    idrbod = models.ForeignKey( 'Cbrbod', models.DO_NOTHING, db_column='idrbod', default=0, null=True )
    coderr = models.SmallIntegerField( db_column='coderr', default=0 )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbrbode'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbrbode, self ).save( *args, **kwargs )

        # 
#**********************************************************************************************************************#
#**********************************************************************************************************************#


class Cbterr(models.Model):
    idterr = models.AutoField(db_column='idterr', primary_key=True)
    coderr = models.SmallIntegerField(db_column="coderr")
    descerr = models.CharField(verbose_name='Descripcion', db_column='descerr', max_length=30)
    fechact = models.DateTimeField(verbose_name='Fecha de carga', db_column='fechact', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario de archivo', db_column='idusu', max_length=16, null=True )
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        # self.fields['names'].widget.attrs['autofocus']=True

    class Meta:
        managed = True
        db_table = 'cbterr'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        super( Cbterr, self ).save( *args, **kwargs )

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
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
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
    archivobco = models.FileField(verbose_name='Archivo del Banco', db_column='archivobco', upload_to=get_path, null=True, blank=True)
    #fechactbco = models.DateTimeField(verbose_name='Fecha de carga Banco', db_column='FECHACTBCO', blank=True, null=True)
    #idusubco = models.CharField(verbose_name='Usuario carga Banco', db_column='IDUSUBCO', max_length=16, blank=True, null=True)
    recordbco = models.IntegerField(verbose_name='Registros de Banco', db_column='recordbco', default=0, blank=True, null=True)
    archivoerp = models.FileField(verbose_name='Archivo del ERP', db_column='archivoerp', upload_to=get_path, null=True, blank=True)
    #fechacterp = models.DateTimeField(verbose_name='Fecha de carga ERP', db_column='FECHACTERP', blank=True, null=True)
    #idusuerp = models.CharField(verbose_name='Usuario carga ERP', db_column='IDUSUERP', max_length=16, blank=True, null=True)
    recorderp = models.IntegerField(verbose_name='Registros de ERP', db_column='recorderp', default=0, blank=True, null=True)
    #archivoimgerp = models.FileField(verbose_name='Imagen del ERP', upload_to=get_path_temp,db_column="archivoimgerp", blank=True, null=True)
    archivoimgbco = models.FileField(verbose_name='Imagen del Banco', upload_to=get_path_temp,db_column="archivoimgbco", blank=True, null=True)
    
    saldobco = models.DecimalField( db_column='saldobco', max_digits=16, decimal_places=2, blank=True, null=True )
    saldobcoori = models.DecimalField( db_column='saldobcoori', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoerp =models.DecimalField( db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoerpori =models.DecimalField( db_column='saldoerpori', max_digits=16, decimal_places=2, blank=True, null=True )
    difbcoerp =models.DecimalField( db_column='difbcoerp', max_digits=16, decimal_places=2, blank=True, null=True )    
    fechacons=models.DateTimeField( verbose_name='Fecha de conciliación', db_column='fechact', null=True)
    idusucons=models.CharField( verbose_name='Usuario que realizó la última operación', db_column='idusu', max_length=16, null=True )
    def toJSON(self):
        item = model_to_dict(self,exclude=["imgbco", "archivoimgerp", "archivoimgbco"])
        return item
    def delete(self):
        Cbrbod.objects.filter(idrenc=self.idrenc).delete()
        super( Cbrenc, self ).delete()
    # def __str__(self):
    #     return str(self.idrenc)
    def save(self, *args, **kwargs):
        try:
            self.corr = Cbrenc.objects.filter(codbco=self.codbco,nrocta=self.nrocta,ano=self.ano, mes=self.mes,empresa=self.empresa).order_by('-corr')[0].corr + 1
        except:
            self.corr = 0
        super( Cbrenc, self ).save( *args, **kwargs )


    class Meta:
        managed = True
        db_table = 'cbrenc'  # Para que en la migracion no ponga el prefijo de la app
        unique_together=(('empresa', 'cliente', 'codbco', 'nrocta', 'ano', 'mes', 'corr'),)
       # ordening = ['codbco']

#**********************************************************************************************************************#
#**********************************************************************************************************************#
#class Cbrencierp(models.Model):
#    idrenci = models.AutoField(verbose_name='id', db_column='idrenci', primary_key=True)
#    idrenc = models.IntegerField(verbose_name='idrenc', db_column='idrenc')
#    imgerp = models.BinaryField( verbose_name='Imagen de banco', db_column = "imgbco", editable=True, null=True)
#    archivotipo = models.CharField(verbose_name='Tipo de Archivo', db_column = "archivotipo", default="PDF", max_length=4)
#    class Meta:
#        managed = True
#        db_table = 'cbrencierp'
#**********************************************************************************************************************#
#**********************************************************************************************************************#
class Cbrencibco(models.Model):
    idrencibco = models.AutoField(verbose_name='id', db_column='idrencibco', primary_key=True)
    idrenc = models.IntegerField(verbose_name='idrenc', db_column='idrenc')
    imgbco = models.BinaryField( verbose_name='Imagen de banco', db_column = "imgbco", editable=True, null=True)
    archivotipo = models.CharField(verbose_name='Tipo de Archivo', db_column = "archivotipo", default="PDF", max_length=4)
    class Meta:
        managed = True
        db_table = 'cbrencibco'
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
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
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
    oficina = models.TextField(db_column='oficina', blank=True, null=True)
    desctra = models.TextField(db_column='desctra', blank=True, null=True)
    reftra = models.TextField(db_column='reftra', blank=True, null=True)
    codtra = models.TextField(db_column='codtra', blank=True, null=True)
    idrbcod = models.IntegerField( db_column='idrbcod', blank=True, null=True, default=0 )
    
    # -----------------------------------------------------------------------------------------------------------------
    nrotraerp = models.TextField(db_column='nrotra', blank=True, null=True)
    fechatraerp = models.DateField(db_column='fechatraerp', blank=True, null=True)
    nrocomperp = models.TextField(db_column='nrocomp', blank=True, null=True)
    auxerp = models.SmallIntegerField(db_column='auxerp', blank=True, null=True)
    referp = models.TextField(db_column='referp', blank=True, null=True)
    glosaerp = models.TextField(db_column='glosa', blank=True, null=True)
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoerp = models.DecimalField(db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumeserp = models.DecimalField( db_column='saldoacumeserp', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiaerp = models.DecimalField( db_column='saldoacumdiaerp', max_digits=16, decimal_places=2, blank=True, null=True )       
    fechaconerp = models.DateField(db_column='fechaconerp', blank=True, null=True)
    idrerpd = models.IntegerField( db_column='idrerpd', blank=True, null=True, default=0  )

    estadoerp=models.SmallIntegerField( verbose_name='Estado Erp', db_column='estadoerp', null=True)

    estadobco=models.SmallIntegerField( verbose_name='Estado Banco', db_column='estadobco', null=True)
    codtcobco = models.CharField(db_column='codtcobco', blank=True, null=True, max_length=4)
    codtcoerp = models.CharField(db_column='codtcoerp', blank=True, null=True, max_length=4)
    idrbcodl = models.IntegerField(db_column='idrbcodl', blank=True, null=True)
    idrerpdl = models.IntegerField(db_column='idrerpdl', blank=True, null=True)    

    saldodiferencia = models.DecimalField( db_column='saldodiferencia', max_digits=16, decimal_places=2, blank=True, null=True )
    historial=models.CharField( verbose_name='Historial', db_column='historial', max_length=1, default = "0" )
    pautado = models.IntegerField(db_column='pautado', blank=True, null=True)
    
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        managed = True
        db_table = 'cbsres'  # Para que en la migracion no ponga el prefijo de la app


class Cbwres(models.Model):
    idsres = models.IntegerField( verbose_name='ID', db_column='idsres', primary_key=True )
    idrenc = models.ForeignKey( 'Cbrenc', models.DO_NOTHING, db_column='idrenc', default=0 )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
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
    oficina = models.TextField(db_column='oficina', blank=True, null=True)
    desctra = models.TextField(db_column='desctra', blank=True, null=True)
    reftra = models.TextField(db_column='reftra', blank=True, null=True)
    codtra = models.TextField(db_column='codtra', blank=True, null=True)
    idrbcod = models.IntegerField( db_column='idrbcod', blank=True, null=True, default=0 )
    
    # -----------------------------------------------------------------------------------------------------------------
    nrotraerp = models.TextField(db_column='nrotra', blank=True, null=True)
    fechatraerp = models.DateField(db_column='fechatraerp', blank=True, null=True)
    nrocomperp = models.TextField(db_column='nrocomp', blank=True, null=True)
    auxerp = models.SmallIntegerField(db_column='auxerp', blank=True, null=True)
    referp = models.TextField(db_column='referp', blank=True, null=True)
    glosaerp = models.TextField(db_column='glosa', blank=True, null=True)
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoerp = models.DecimalField(db_column='saldoerp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumeserp = models.DecimalField( db_column='saldoacumeserp', max_digits=16, decimal_places=2, blank=True, null=True )
    saldoacumdiaerp = models.DecimalField( db_column='saldoacumdiaerp', max_digits=16, decimal_places=2, blank=True, null=True )       
    fechaconerp = models.DateField(db_column='fechaconerp', blank=True, null=True)
    idrerpd = models.IntegerField( db_column='idrerpd', blank=True, null=True, default=0  )

    estadoerp=models.SmallIntegerField( verbose_name='Estado Erp', db_column='estadoerp', null=True)

    estadobco=models.SmallIntegerField( verbose_name='Estado Banco', db_column='estadobco', null=True)
    codtcobco = models.CharField(db_column='codtcobco', blank=True, null=True, max_length=4)
    codtcoerp = models.CharField(db_column='codtcoerp', blank=True, null=True, max_length=4)
    idrbcodl = models.IntegerField(db_column='idrbcodl', blank=True, null=True)
    idrerpdl = models.IntegerField(db_column='idrerpdl', blank=True, null=True)    

    saldodiferencia = models.DecimalField( db_column='saldodiferencia', max_digits=16, decimal_places=2, blank=True, null=True )
    historial=models.CharField( verbose_name='Historial', db_column='historial', max_length=1, default = "0" )
    pautado = models.IntegerField(db_column='pautado', blank=True, null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        managed = True
        db_table = 'cbwres'  # Para que en la migracion no ponga el prefijo de la app

#**********************************************************************************************************************#

class Cbsresc(models.Model):
    idsresc = models.AutoField( verbose_name='ID', db_column='idsresc', primary_key=True )
    idsres = models.IntegerField( verbose_name='ID', db_column='idsres')
    codtco = models.CharField(verbose_name='Codtco', db_column='codtco', max_length=4)
    debebco = models.DecimalField(db_column='debebco', max_digits=16, decimal_places=2, blank=True, null=True)
    haberbco = models.DecimalField(db_column='haberbco', max_digits=16, decimal_places=2, blank=True, null=True)
    debeerp = models.DecimalField(db_column='debeerp', max_digits=16, decimal_places=2, blank=True, null=True)
    habererp = models.DecimalField(db_column='habererp', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumesbco = models.DecimalField(db_column='saldoacumesbco', max_digits=16, decimal_places=2, blank=True, null=True)
    saldoacumeserp = models.DecimalField(db_column='saldoacumeserp', max_digits=16, decimal_places=2, blank=True, null=True)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    class Meta:
        managed = True
        db_table = 'cbsresc'

#**********************************************************************************************************************#

class Cbmbco(models.Model):
    idmbco = models.AutoField( verbose_name='ID', db_column='idmbco', primary_key=True )
    codbco = models.CharField( verbose_name='Codigo del Banco', db_column='codbco', max_length=5)
    desbco = models.CharField(verbose_name='Descripcion del Banco', db_column='desbco', max_length=50)
    codhombco = models.CharField(verbose_name='Codigo de homologador bco', db_column='codhombco', max_length=5, default="vebod")
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbmbco'

class Cbmbcoh(models.Model):
    idmbcoh = models.AutoField( verbose_name='ID', db_column='idmbcoh', primary_key=True )
    idmbco = models.ForeignKey( 'Cbmbco', models.DO_NOTHING, db_column='idmbco')
    tipohomo = models.SmallIntegerField( verbose_name='Tipo de Homologacion', db_column='tipohomo', default=0)
    deshomo = models.CharField(verbose_name='Descripcion de la homologacion', db_column='deshomo', max_length=50)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbmbcoh'

class Cbtpai(models.Model):
    idtpai = models.AutoField( verbose_name='ID', db_column='idtpai', primary_key=True )
    codpai = models.CharField(verbose_name='Código de Pais', db_column='codpai', max_length=2)
    despai = models.CharField(verbose_name='Descripcion de Pais', db_column='despai', max_length=30)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtpai'

class Cbtemp(models.Model):
    idtemp = models.AutoField( verbose_name='ID', db_column='idtemp', primary_key=True )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
    desemp = models.CharField(verbose_name='Descripcion de la empresa', db_column='desemp', max_length=60)
    actpas = models.CharField(verbose_name='Activo o Pasivo', db_column='actpas', max_length=1)
    codhomerp = models.CharField(verbose_name='Codigo de homologador erp', db_column='codhomerp', max_length=5, blank=True)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        managed = True
        db_table = 'cbtemp'

class Cbtcli(models.Model):
    idtcli = models.AutoField( verbose_name='ID', db_column='idtcli', primary_key=True )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    descli = models.CharField(verbose_name='Descripcion del cliente', db_column='descli', max_length=60)
    codhomerp = models.CharField(verbose_name='Codigo de homologador erp', db_column='codhomerp', max_length=5, default="vegal")
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtcli'
    
    def save(self, *args, **kwargs):
        if Cbtpai.objects.filter(codpai=self.cliente[0:2]).exists():
            if Cbtcli.objects.filter(idtcli=self.idtcli).exists()== False:
                Cbtcfg(cliente=self.cliente, codcfg=1,actpas="P", fechact=self.fechact, idusu=self.idusu).save()
                Cbtcfg(cliente=self.cliente, codcfg=2,actpas="P", fechact=self.fechact, idusu=self.idusu).save()
            super( Cbtcli, self ).save( *args, **kwargs )
        else:
            return False

class Cbtlic(models.Model):
    idtlic = models.AutoField( verbose_name='ID', db_column='idtlic', primary_key=True )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    licencia = models.CharField(verbose_name='Licencia', db_column='licencia', max_length=30)
    nrousuario = models.SmallIntegerField(verbose_name='Numero de Usuarios',db_column='nrousuario')
    nroempresa = models.SmallIntegerField(verbose_name='Numero de Empresa',db_column='nroempresa')
    nrocodbco = models.SmallIntegerField(verbose_name='Numero de Bancos',db_column='nrocodbco')
    nrocuenta = models.SmallIntegerField(verbose_name='Numero de Cuenta',db_column='nrocuenta')
    fechalic = models.DateTimeField( verbose_name='Fecha de Vencimiento', db_column='fechalic')
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtlic'

class Cbtfor(models.Model):
    idtfor = models.AutoField( verbose_name='ID', db_column='idtfor', primary_key=True )
    codfor = models.SmallIntegerField(verbose_name='Codigo de Formulario',db_column='codfor')
    descfor = models.CharField(verbose_name='Descripcion de Formulario', db_column='descfor', max_length=60)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtfor'

class Cbtusu(models.Model):
    idtusu = models.AutoField( verbose_name='ID', db_column='idtusu', primary_key=True )
    idusu1 = models.CharField(verbose_name='Login del usuario', db_column='idusu1', max_length=16)
    descusu = models.CharField(verbose_name='Descripcion del usuario', db_column='descusu', max_length=60)
    pasusu = models.BooleanField(verbose_name='Password Reseteable', db_column='pasusu', default=False)
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    tipousu = models.CharField(verbose_name='Tipo de usuario', db_column='tipousu', max_length=1, blank=True)
    superusu = models.CharField(verbose_name='Superusuario', db_column='superusu', max_length=1, blank=True)
    indconc = models.CharField(verbose_name='Puede Conciliar', db_column='indconc', max_length=1, blank=True)    
    actpas = models.CharField(verbose_name='Activo o Pasivo', db_column='actpas', max_length=1, blank=True)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        managed = True
        db_table = 'cbtusu'


    def save(self, *args, **kwargs):
        if User.objects.filter(username=self.idusu1).exists()==False:
            usuario = User(username=self.idusu1,
                               password=make_password("ninguno"))
            usuario.save()
        super( Cbtusu, self ).save( *args, **kwargs )


class Cbtusue(models.Model):
    idtusue = models.AutoField( verbose_name='ID', db_column='idtusue', primary_key=True )
    idtusu = models.ForeignKey( 'Cbtusu', models.DO_NOTHING, db_column='idtusu', default=0 )
    empresa = models.CharField(verbose_name='Empresa', db_column='empresa', max_length=5)
    actpas = models.CharField(verbose_name='Activo o Pasivo', db_column='actpas', max_length=1)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    def toJSON(self):
        item = model_to_dict(self)
        return item
        
    class Meta:
        managed = True
        db_table = 'cbtusue'
    

class Cbtusuc(models.Model):
    idtusuc = models.AutoField( verbose_name='ID', db_column='idtusuc', primary_key=True )
    idtusu = models.IntegerField(verbose_name='Login del usuario',db_column='idtusu')
    codcol = models.IntegerField(verbose_name='Código de Conciliacion',db_column='codcol')
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtusuc'

class Cbtcol(models.Model):
    idtcol = models.AutoField( verbose_name='ID', db_column='idtcol', primary_key=True )
    codcol = models.SmallIntegerField(verbose_name='Codigo de Columna',db_column='codcol', unique=True)
    descol = models.CharField( verbose_name='Descripción de la columna', db_column='descol', max_length=30, null=True )
    inddef = models.SmallIntegerField(verbose_name='Indicador de visibilidad de columna',db_column='inddef')
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    def toJSON(self):
        item = model_to_dict(self)
        return item
        
    class Meta:
        managed = True
        db_table = 'cbtcol'

class Cbsusu(models.Model):
    idsusu = models.AutoField( db_column='idsusu', primary_key=True )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    idusu1 = models.CharField(verbose_name='Login del usuario', db_column='idusu1', max_length=16)
    corrusu = models.SmallIntegerField(verbose_name='Correlativo de Usuario',db_column='corrusu')
    iniciologin = models.DateTimeField( verbose_name='Fecha de Inicio de Sesion', db_column='iniciologin', null=True)
    finlogin = models.DateTimeField( verbose_name='Fecha de Cierre de Sesión', db_column='finlogin', null=True)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
        
    class Meta:
        managed = True
        db_table = 'cbsusu'
    
    def guardar(self, *args, **kwargs):
        self.corrusu = Cbsusu.objects.filter(idusu1 = self.idusu1).count()+1
        super( Cbsusu, self ).save( *args, **kwargs )
    

class Cbthom(models.Model):
    idthom = models.AutoField( verbose_name='ID', db_column='idthom', primary_key=True )
    indhom = models.CharField(verbose_name='Indicador de Homologacion', db_column='indhom', max_length=1)
    codhom = models.CharField(verbose_name='Codigo de homologador', db_column='codhom', max_length=5)
    deschom = models.CharField(verbose_name='Descripcion del homologador', db_column='deschom', max_length=50)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )
    
    class Meta:
        managed = True
        db_table = 'cbthom'


class Cbtcfg(models.Model):
    idtcfg = models.AutoField( verbose_name='ID', db_column='idtcfg', primary_key=True )
    cliente = models.CharField(verbose_name='Cliente', db_column='cliente', max_length=5)
    codcfg = models.SmallIntegerField(verbose_name='Codigo de configuracion',db_column='codcfg')
    actpas = models.CharField(verbose_name='activo o pasivo',db_column='actpas', max_length=1)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtcfg'

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Cbtcfgc(models.Model):
    idtcfgc = models.AutoField( verbose_name='ID', db_column='idtcfgc', primary_key=True )
    idtcfg = models.ForeignKey( 'Cbtcfg', models.DO_NOTHING, db_column='idtcfg')
    ordencfg = models.SmallIntegerField(verbose_name='Orden de comparacion',db_column='ordencfg')
    campobco = models.CharField(verbose_name='Campo Banco',db_column='campobco', max_length=30)
    campoerp = models.CharField(verbose_name='Campo ERP',db_column='campoerp', max_length=30)
    fechact = models.DateTimeField( verbose_name='Fecha de Actualizacion', db_column='fechact', null=True)
    idusu = models.CharField( verbose_name='Usuario', db_column='idusu', max_length=16, null=True )

    class Meta:
        managed = True
        db_table = 'cbtcfgc'
        
    def toJSON(self):
        item = model_to_dict(self)
        return item