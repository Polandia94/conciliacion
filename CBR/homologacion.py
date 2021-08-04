
from CBR.models import Cbrbod, Cbrbcoe, Cbrbcod, Cbrerpe, Cbrerpd, Cbrgal, Cbterr, Cbrenc
import pandas as pd
from django.utils import timezone
import datetime as dt
import math

def es_decimal(value):
        try:
            float( value )
            return True
        except:
            return False

def FueradeCalendario(dia,mes,ano):
    if dia > 31:
        return True
    if dia == 31 and (mes == 2 or mes == 4 or mes == 6 or mes == 9 or mes == 11):
        return True
    if dia == 30 and mes == 2:
        return True
    if dia == 29 and mes == 2 and ano % 4 != 0:
        return True
    return False

def HomologacionBcoBOD(request, aCbrenc, data, saldobcoanterior):
    #Lee el archivo del banco y cre al Cbrbod respectivo
    try:
        dataBco=pd.read_csv( str( aCbrenc.archivobco ), delimiter="|", header=0, index_col=False )
        fallo = False
        print(len( dataBco ))
        for i in range( len( dataBco ) ):
            if pd.isnull(dataBco.loc[i, dataBco.columns[0]]) == False:
                mes = int(aCbrenc.mes)
                ano = int(aCbrenc.ano)
                try:
                    aCbrbod = Cbrbod()
                    error = 0
                    aCbrbod.idrenc = aCbrenc
                    dia = dataBco.loc[i, dataBco.columns[0]]
                    try:
                        dia = int(dia)
                        if FueradeCalendario(dia,mes,ano):
                            error = 1
                    except:
                        error = 1
                        dia = 0
                    aCbrbod.diatra = dia
                    #Si el día esta fuera del calendario o no es un numero devuelve error 1
                    aCbrbod.oficina = dataBco.loc[i, dataBco.columns[1]]
                    #Si la oficina está en blanco devuelve error 2
                    if aCbrbod.oficina == "" or pd.isnull(dataBco.loc[i, dataBco.columns[1]]):
                        error = 2
                    aCbrbod.desctra = dataBco.loc[i, dataBco.columns[2]]
                    try:
                        debe = dataBco.loc[i, dataBco.columns[3]].replace(".","").replace(",","")
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
                    aCbrbod.debe = float(debe)/100
                    try:
                        haber = dataBco.loc[i, dataBco.columns[4]].replace(".","").replace(",","")
                    except:
                        if pd.isnull(dataBco.loc[i, dataBco.columns[4]]) == False:
                            error=4
                            # Si el haber no está vacio ni es un numero devuelve error 4
                        haber = 0
                    if es_decimal(haber) == False:
                        haber = 0
                        error = 4
                        # si el haber no es un numero devuelve error 4
                    aCbrbod.haber = float(haber)/100
                    try:
                        saldo = dataBco.loc[i, dataBco.columns[5]].replace(".","").replace(",","")
                    except:
                        pass
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
                    aCbrbod.saldo = float(saldo)/100
                    aCbrbod.fechact = dt.datetime.now(tz=timezone.utc)
                    aCbrbod.idusu=request.user.username
                    if error == 0:
                        aCbrbod.save(aCbrbod)                
                    else:
                        fallo = True
                        aCbterr = Cbterr(tabla="CBRBOD", coderr = error)
                        aCbterr.fechact = dt.datetime.now(tz=timezone.utc)
                        aCbterr.idusu=request.user.username
                        aCbterr.save()

                except Exception as e:
                    pass
                #En caso de errores deja solo los errores en la tabla
        if fallo:
            Cbrbod.objects.filter(idrenc=aCbrbod.idrenc).delete()
            data["error"] = 'Existieron problemas en la carga de archivo BCO. Verifique el formulario CBF10 en <a href=" ../../cbterr/?tabla=CBRBOD"> la Tabla de Errores</a> '
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
            for registro in Cbrbod.objects.filter(idrenc=aCbrbod.idrenc).all():
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
    except Exception as e:
         data["error"] = "Error desconocido en el archivo del Banco"

        

def HomologacionErpGAL(request, aCbrenc, data, saldoerpanterior):
    try:
        try:
            Cbrerpd.objects.filter(idrbcoe=Cbrerpe.objects.filter( idrerpe=aCbrenc.idrenc ).first().idrerpe).delete()
        except:
            pass
        Cbrerpd.objects.filter( idrerpe=aCbrenc.idrenc ).delete()
        dataErp=pd.read_csv( str( aCbrenc.archivoerp ), header=0, delimiter = "|", index_col=False )
        iniciado = False
        pausa = False
        fallo = False
        haberTotal = 0
        debeTotal = 0
        for i in range( len( dataErp ) ):
            try:
                if dataErp.loc[i, dataErp.columns[0]].find("/")>-1:
                    error = 0
                    pausa = False
                    iniciado = True
                    aCbrgal = Cbrgal()
                    aCbrgal.idrenc = aCbrenc
                    s_date=dataErp.loc[i, dataErp.columns[0]]
                    try:
                        fechatra=dt.datetime.strptime( s_date, '%d/%m/%Y' )
                    except:
                        print(s_date)
                    if fechatra.year != aCbrenc.ano or fechatra.month != aCbrenc.mes:
                        error = 1
                        print(str(fechatra.month) + "/" +str(fechatra.year)  + " distinto a " + str(aCbrenc.ano) + "/"+ str(aCbrenc.mes))
                    aCbrgal.fechatra = fechatra
                    aCbrgal.nrocomp = dataErp.loc[i, dataErp.columns[1]]
                    if pd.isnull(dataErp.loc[i, dataErp.columns[2]]):
                        aux = 0
                    else:
                        aux = dataErp.loc[i, dataErp.columns[2]]
                    aCbrgal.aux = aux
                    if pd.isnull(dataErp.loc[i, dataErp.columns[3]]):
                        ref = ""
                    else:
                        ref=dataErp.loc[i, dataErp.columns[3]]
                    aCbrgal.ref = ref
                    aCbrgal.glosa = dataErp.loc[i, dataErp.columns[4]]
                    try:
                        float(dataErp.loc[i, dataErp.columns[5]].replace(",",""))
                        debe = dataErp.loc[i, dataErp.columns[5]].replace(",","")
                    except:
                        error = 2
                        debe = 0
                    aCbrgal.debe = debe
                    debeTotal = float(debe) + debeTotal
                    try:
                        float(dataErp.loc[i, dataErp.columns[6]].replace(",",""))
                        haber = dataErp.loc[i, dataErp.columns[6]].replace(",","")
                    except:
                        error = 3
                        haber = 0
                    aCbrgal.haber = haber
                    haberTotal = float(haber) + haberTotal
                    try:
                        float(dataErp.loc[i, dataErp.columns[7]].replace(",",""))
                        saldo = dataErp.loc[i, dataErp.columns[7]].replace(",","")
                    except:
                        error = 4
                        saldo = 0
                    aCbrgal.saldo = saldo
                    s_date=dataErp.loc[i, dataErp.columns[8]]                
                    try:
                        fechacon = dt.datetime.strptime( s_date, '%d/%m/%Y' )
                    except:
                        pass
                    aCbrgal.fechacon = fechacon
                    aCbrgal.idusu=request.user.username
                    aCbrgal.fechact=dt.datetime.now(tz=timezone.utc)
                    if error == 0: 
                        aCbrgal.save(aCbrgal)
                    else:
                        fallo = True
                        aCbterr = Cbterr(tabla="CBRGAL", coderr = error)
                        aCbterr.fechact = dt.datetime.now(tz=timezone.utc)
                        aCbterr.idusu=request.user.username
                        aCbterr.save()
                else:
                    print(dataErp.loc[i, dataErp.columns[0]])
            except Exception as e:
                if dataErp.loc[i, dataErp.columns[4]] != " Van:" and dataErp.loc[i, dataErp.columns[4]] != "TOTALES . . . . . . . " and pausa == False and iniciado:
                    aCbrgal.glosa = str(aCbrgal.glosa) + " " +str(dataErp.loc[i, dataErp.columns[4]])
                    aCbrgal.actualizar(aCbrgal)
                    pausa = True
                if dataErp.loc[i, dataErp.columns[4]] != "Vienen:":
                    pausa = False
                if dataErp.loc[i, dataErp.columns[4]] == "TOTALES . . . . . . . ":
                    if(math.isclose(float(dataErp.loc[i, dataErp.columns[5]].replace(",","")),debeTotal) and math.isclose(float(dataErp.loc[i, dataErp.columns[6]].replace(",","")) , haberTotal)) == False:
                        data["error"] = "La suma de debes y la suma de haberes no coincide con los totales"   
                        return True
        if fallo:
            data["error"] = "Existieron problemas en la carga de archivo ERP. Verifique el formulario CBF11 en "    
        else:
            try:
                Cbrerpd.objects.filter(idrbcoe=Cbrerpe.objects.filter( idrerpe=aCbrenc.idrenc ).first().idrerpe).delete()
            except:
                pass
            Cbrerpd.objects.filter( idrerpe=aCbrenc.idrenc ).delete()
            tableErpEnc = Cbrerpe(
                idrerpe=aCbrenc.idrenc,
                idrenc=aCbrenc,
                fechact = dt.datetime.now(tz=timezone.utc),
                idusu = request.user.username
                )
            try:
                aCbrenc.corr = Cbrenc.objects.filter(codbco=aCbrenc.codbco,nrocta=aCbrenc.nrocta,ano=aCbrenc.ano, mes=aCbrenc.mes,empresa=aCbrenc.empresa).order_by('-corr')[0].corr + 1
            except:
                aCbrenc.corr = 1
            try:
                aCbrenc.save()
            except:
                aCbrenc.corr = 1
                aCbrenc.save()
            tableErpEnc.save()
            for registro in Cbrgal.objects.filter(idrenc=aCbrenc.idrenc).all():
                tableErp=Cbrerpd(
                nrotra = 0,
                fechatra=registro.fechatra,
                nrocomp=registro.nrocomp,
                aux = registro.aux,
                ref= registro.ref,
                glosa = registro.glosa, 
                debe=registro.debe,
                haber=registro.haber,
                saldo=registro.saldo,
                fechacon=registro.fechacon,
                idrerpe=tableErpEnc,
                    )
                saldo = registro.saldo
                tableErp.save( aCbrenc )
            aCbrenc.recorderp = len( dataErp )
            aCbrenc.saldoerp = saldo
            try:
                aCbrenc.difbcoerp = aCbrenc.saldobco - saldo
            except:
                aCbrenc.difbcoerp = 0
            aCbrenc.estado = "0"
            aCbrenc.fechacons=dt.datetime.now(tz=timezone.utc)
            aCbrenc.idusu=request.user.username
            aCbrenc.save()
            return True
    except:
        data["error"] = "Problema desconocido en el archivo del ERP"


