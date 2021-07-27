
from CBR.models import Cbrbod, Cbrbcoe, Cbrbcod
import pandas as pd
from django.utils import timezone
import datetime as dt

def es_decimal(value):
        try:
            float( value )
            return True
        except:
            return False

def FueradeCalendario(dia,mes):
    if dia > 31:
        return True
    if dia == 31 and (mes == 2 or mes == 4 or mes == 6 or mes == 9 or mes == 11):
        return True
    if dia == 30 and mes == 2:
        return True
    return False

def HomologacionBcoBOD(request, aCbrenc, data, saldobcoanterior):
    #Lee el archivo del banco y cre al Cbrbod respectivo
    dataBco=pd.read_csv( str( aCbrenc.archivobco ), delimiter="|", header=0, index_col=False )
    for i in range( len( dataBco ) ):
        mes = int(aCbrenc.mes)
        try:
            aCbrobod = Cbrbod()
            error = 0
            aCbrobod.idrenc = aCbrenc
            dia = dataBco.loc[i, dataBco.columns[0]]
            try:
                dia = int(dia)
                if FueradeCalendario(dia,mes):
                    error = 1
            except:
                error = 1
                dia = 0
            aCbrobod.diatra = dia
            #Si el día esta fuera del calendario o no es un numero devuelve error 1

            aCbrobod.oficina = dataBco.loc[i, dataBco.columns[1]]
            #Si la oficina está en blanco devuelve error 2
            if aCbrobod.oficina == "" or pd.isnull(dataBco.loc[i, dataBco.columns[1]]):
                error = 2
            aCbrobod.desctra = dataBco.loc[i, dataBco.columns[2]]
            try:
                debe = dataBco.loc[i, dataBco.columns[3]].replace(".","").replace(",",".")
            except:
                debe = 0
                if pd.isnull(dataBco.loc[i, dataBco.columns[3]]) == False:
                    error=3
                # Si el debe no está vacio ni es un numero devuelve error 3
            if debe[-1]=="-":
                debe = debe[0:-1]
            if es_decimal(debe) == False:
                debe = 0
                error = 3
                # si el debe no es un numero devuelve error 3
            aCbrobod.debe = debe
            try:
                haber = dataBco.loc[i, dataBco.columns[4]].replace(".","").replace(",",".")
            except:
                if pd.isnull(dataBco.loc[i, dataBco.columns[4]]) == False:
                    error=4
                    # Si el haber no está vacio ni es un numero devuelve error 4
                haber = 0
            if es_decimal(haber) == False:
                haber = 0
                error = 4
                # si el haber no es un numero devuelve error 4
            aCbrobod.haber = haber
            saldo = dataBco.loc[i, dataBco.columns[5]].replace(".","").replace(",",".")
            try:
                if saldo[-1]=="-":
                    saldo = float(saldo[0:-1])*-1
            except:
                error = 5
                saldo = 0
            if es_decimal(saldo) == False:
                error = 5
                saldo = 0
            # si el saldo no es un numero devuelve error 5
            aCbrobod.saldo = saldo
            aCbrobod.fechact = dt.datetime.now(tz=timezone.utc)
            aCbrobod.idusu=request.user.username
            aCbrobod.error = error
            aCbrobod.save(aCbrobod)
        except Exception as e:
            Cbrbod.objects.filter(idrenc=aCbrobod.idrenc).delete()
            data["error"] = e
        #En caso de errores deja solo los errores en la tabla
    if Cbrbod.objects.exclude(error=0).filter(idrenc=aCbrobod.idrenc).exists():
        Cbrbod.objects.filter(idrenc=aCbrobod.idrenc, error=0).delete()
        for registro in Cbrbod.objects.filter(idrenc=aCbrobod.idrenc).all():
            registro.idrenc = None
            registro.save(registro)
        data["error"] = "Existieron problemas en la carga de archivo. Verifique el formulario CBF10 en "
    #Caso contrario carga el cbrbcoe
    else:
        Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).delete()
        try:
            Cbrbcod.objects.filter(idrbcoe=Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).first().idrbcoe).delete()
        except Exception as e:
            print(e)
        tableBcoEnc = Cbrbcoe(
            idrbcoe=aCbrenc.idrenc,
            idrenc=aCbrenc,
            fechact1 = dt.datetime.now(tz=timezone.utc),
            idusu1 = request.user.username
            )
        Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).delete()
        tableBcoEnc.save()
        for registro in Cbrbod.objects.filter(idrenc=aCbrobod.idrenc).all():
            tableBco=Cbrbcod(
            fechatra=dt.datetime(aCbrenc.ano, aCbrenc.mes, registro.diatra),
            horatra="00:00:00",
            oficina=registro.oficina,
            desctra=registro.desctra,
            reftra="",
            codtra="",
            debe=registro.debe,
            haber=registro.haber,
            saldo=registro.saldo,
            idrbcoe=tableBcoEnc,
                )
            saldo = registro.saldo
            tableBco.save( aCbrenc )
        aCbrenc.recordbco = len( dataBco )
        aCbrenc.saldobco = saldo
        aCbrenc.idusubco=request.user.username
        return True

