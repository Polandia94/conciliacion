
from CBR.models import Cbrbod, Cbrbcoe, Cbrbcod, Cbrbode, Cbrerpe, Cbrerpd, Cbrgal, Cbterr, Cbrenc,Cbrgale
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
        sobreescribir=request.POST['sobreescribir']
        for i in range( len( dataBco ) ):
            if pd.isnull(dataBco.loc[i, dataBco.columns[0]]) == False:
                mes = int(aCbrenc.mes)
                ano = int(aCbrenc.ano)
                try:
                    aCbrbod = Cbrbod()
                    errores = []
                    aCbrbod.idrenc = aCbrenc
                    dia = dataBco.loc[i, dataBco.columns[0]]
                    try:
                        dia = int(dia)
                        if FueradeCalendario(dia,mes,ano):
                            errores.append(1)
                    except:
                        errores.append(1)
                        dia = 0
                    aCbrbod.diatra = dia
                    #Si el día esta fuera del calendario o no es un numero devuelve errores 1
                    aCbrbod.oficina = dataBco.loc[i, dataBco.columns[1]]
                    #Si la oficina está en blanco devuelve errores 2
                    if aCbrbod.oficina == "" or pd.isnull(dataBco.loc[i, dataBco.columns[1]]):
                        errores.append(2)
                    aCbrbod.desctra = dataBco.loc[i, dataBco.columns[2]]
                    try:
                        debe = dataBco.loc[i, dataBco.columns[3]].replace(".","").replace(",","")
                    except:
                        debe = 0
                        if pd.isnull(dataBco.loc[i, dataBco.columns[3]]) == False:
                            errores.append(3)
                        # Si el debe no está vacio ni es un numero devuelve errores 3
                    if debe[-1]=="-":
                        debe = debe[0:-1]
                    if es_decimal(debe) == False:
                        debe = 0
                        errores.append(3)
                        # si el debe no es un numero devuelve errores 3
                    aCbrbod.debe = float(debe)/100
                    try:
                        haber = dataBco.loc[i, dataBco.columns[4]].replace(".","").replace(",","")
                    except:
                        if pd.isnull(dataBco.loc[i, dataBco.columns[4]]) == False:
                            errores.append(4)
                            # Si el haber no está vacio ni es un numero devuelve errores 4
                        haber = 0
                    if es_decimal(haber) == False:
                        haber = 0
                        errores.append(4)
                        # si el haber no es un numero devuelve errores 4
                    aCbrbod.haber = float(haber)/100
                    try:
                        saldo = dataBco.loc[i, dataBco.columns[5]].replace(".","").replace(",","")
                    except:
                        pass
                    try:
                        if saldo[-1]=="-":
                            saldo = float(saldo[0:-1])*-1
                    except:
                        errores.append(5)
                        saldo = 0
                    if es_decimal(saldo) == False:
                        errores.append(5)
                        saldo = 0
                    # si el saldo no es un numero devuelve errores 5
                    aCbrbod.saldo = float(saldo)/100
                    aCbrbod.fechact = dt.datetime.now(tz=timezone.utc)
                    aCbrbod.idusu=request.user.username
                    aCbrbod.save(aCbrbod)                
                    for error in errores:
                        fallo = True
                        aCbrbod.idrenc = None
                        aCbrbod.save(aCbrbod)
                        aCbrbode = Cbrbode(idrbod=aCbrbod ,idterr = Cbterr(error))
                        aCbrbode.save()
                except Exception as e:
                    print(e)
                    fallo = True
                    try:
                        aCbrbod.save(aCbrbod) 
                        aCbrbode = Cbrbode(idrbod=aCbrbod ,idterr = Cbterr(99))
                        aCbrbode.save()
                    except Exception as e:
                        aCbrbode = Cbrbode(idterr = Cbterr(99))
                        aCbrbode.save()
                        print(e)

                #En caso de errores deja solo los errores en la tabla
        if fallo:
            data["error"] = 'Existieron problemas en la carga de archivo BCO. Verifique el formulario CBF10 en <a href=" ../../cbrbode"> la Tabla de errores</a> '
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
        print(e)
        data["error"] = "errores desconocido en el archivo del Banco"
        try:
            for registro in Cbrbod.objects.filter(idrenc = aCbrbod.idrenc):
                registro.idrenc = None
                registro.save()
        except:
            pass        

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
                    errores = []
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
                        errores.append(1)
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
                        errores.append(3)
                        debe = 0
                    aCbrgal.debe = debe
                    debeTotal = float(debe) + debeTotal
                    try:
                        float(dataErp.loc[i, dataErp.columns[6]].replace(",",""))
                        haber = dataErp.loc[i, dataErp.columns[6]].replace(",","")
                    except:
                        errores.append(4)
                        haber = 0
                    aCbrgal.haber = haber
                    haberTotal = float(haber) + haberTotal
                    try:
                        float(dataErp.loc[i, dataErp.columns[7]].replace(",",""))
                        saldo = dataErp.loc[i, dataErp.columns[7]].replace(",","")
                    except:
                        errores.append(5)
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
                    aCbrgal.save(aCbrgal)
                    for error in errores:
                        print(error)
                        fallo = True
                        aCbrgal.idrenc = None
                        aCbrgal.save(aCbrgal)
                        aCbrgale = Cbrgale(idrgal=aCbrgal ,idterr = Cbterr(error))
                        aCbrgale.save()
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
            try:
                data["error"] = 'Existieron problemas en la carga de archivo ERP. Verifique el formulario CBF11 en <a href=" ../../cbrgale"> la Tabla de errores</a> '+ data["error"] 
            except:
                data["error"] = 'Existieron problemas en la carga de archivo ERP. Verifique el formulario CBF11 en <a href=" ../../cbrgale"> la Tabla de errores</a> '
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
    except Exception as e:
        print(e)
        data["error"] = "Problema desconocido en el archivo del ERP"


