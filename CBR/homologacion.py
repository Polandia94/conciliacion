
from logging import exception
from CBR.models import Cbrbod, Cbrbcoe, Cbrbcod, Cbrbode, Cbrerpe, Cbrerpd, Cbrgal, Cbterr, Cbrenc,Cbrgale
import pandas as pd
from django.utils import timezone
import datetime as dt
import math
from pathlib import Path
import time



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
    if dia < 1:
        return True
    return False

def HomologacionBcoBOD(request, aCbrenc, data, saldobcoanterior):
    #Lee el archivo del banco y cre al Cbrbod respectivo
    print("a")
    try:
        Cbrbode.objects.all().delete()
        print("b")
        try:
            dataBco=pd.read_csv( str(Path(__file__).resolve().parent.parent)+ "/media/"+ str( aCbrenc.archivobco ), delimiter="|", header=None, index_col=False, names = list(range(0,11)) )
        except:
            try:
                dataBco=pd.read_csv( str(Path(__file__).resolve().parent.parent)+ "/media/"+ str( aCbrenc.archivobco ), delimiter="|", header=None, index_col=False, names = list(range(0,11)), encoding= "cp1252")
            except:
                dataBco=pd.read_csv( str(Path(__file__).resolve().parent.parent)+ "/media/"+ str( aCbrenc.archivobco ), delimiter="|", header=None, index_col=False, names = list(range(0,11)), encoding= "ISO-8859-1" )
        print("c")
        n = 0
        fallo = False
        for i in range(1, len( dataBco ) ):
            if pd.isnull(dataBco.loc[i, dataBco.columns[0]]) == False:
                mes = int(aCbrenc.mes)
                ano = int(aCbrenc.ano)
                try:
                    if n < 8:
                        time.sleep(1)
                    n = n+1
                    aCbrbod = Cbrbod()
                    errores = []
                    # Crea un Cbrod vacio y una lista vacia de errores. Cada error se agrega a la lista, para al final determinar si debe guardarse o no
                    aCbrbod.idrenc = aCbrenc
                    dia = dataBco.loc[i, dataBco.columns[0]]
                    try:
                        dia = int(dia)
                        if FueradeCalendario(dia,mes,ano):
                            errores.append(1)
                    except:
                        errores.append(1)
                    aCbrbod.diatra = dia
                    #Si el día esta fuera del calendario o no es un numero devuelve errores 1
                    aCbrbod.oficina = dataBco.loc[i, dataBco.columns[1]]
                    #Si la oficina está en blanco devuelve errores 2
                    if aCbrbod.oficina == "" or pd.isnull(dataBco.loc[i, dataBco.columns[1]]):
                        errores.append(2)
                        aCbrbod.oficina = ""
                    aCbrbod.desctra = dataBco.loc[i, dataBco.columns[2]]
                    try:
                        debe = dataBco.loc[i, dataBco.columns[3]].replace(".","").replace(",","")
                    except:
                        debe = '0'
                        if pd.isnull(dataBco.loc[i, dataBco.columns[3]]) == False:
                            errores.append(3)
                        # Si el debe no está vacio ni es un numero devuelve errores 3
                    if debe[-1]=="-":
                        debe = debe[0:-1]
                    if es_decimal(debe) == False:
                        debe = 0
                        errores.append(3)
                        # si el debe no es un numero devuelve errores 3
                    if 3 not in errores:
                        debe = float(debe)/100
                    try:
                        haber = dataBco.loc[i, dataBco.columns[4]].replace(".","").replace(",","")
                    except:
                        if pd.isnull(dataBco.loc[i, dataBco.columns[4]]) == False:
                            errores.append(4)
                            haber = dataBco.loc[i, dataBco.columns[4]]
                            # Si el haber no está vacio ni es un numero devuelve errores 4
                        else:
                            haber = '0'
                    if es_decimal(haber) == False:
                        if 4 not in errores:
                            errores.append(4)

                        # si el haber no es un numero devuelve errores 4
                    if 4 not in errores:
                        haber = float(haber)/100
                    try:
                        if float(debe) > 0 and float(haber) > 0:
                            errores.append(6)
                        if float(debe) == 0 and float(haber) == 0:
                            errores.append(6)
                    except:
                        pass
                    try:
                        saldo = dataBco.loc[i, dataBco.columns[5]].replace(".","").replace(",","")
                    except:
                        pass
                    try:
                        if saldo[-1]=="-":
                            saldo = float(saldo[0:-1])*-1
                    except:
                        errores.append(5)
                    if es_decimal(saldo) == False and 5 not in errores:
                        errores.append(5)
                        saldo = dataBco.loc[i, dataBco.columns[5]]
                    # si el saldo no es un numero devuelve errores 5
                    if 5 not in errores:
                        saldo = float(saldo)/100
                    aCbrbod.fechact = dt.datetime.now(tz=timezone.utc)
                    aCbrbod.idusu=request.user.username
                    aCbrbod.debe = debe
                    aCbrbod.haber = haber
                    aCbrbod.saldo = saldo
                    if len(errores) > 0:
                        debe = dataBco.loc[i, dataBco.columns[3]]
                        haber = dataBco.loc[i, dataBco.columns[4]]
                        saldo = dataBco.loc[i, dataBco.columns[5]]
                    else:
                        aCbrbod.save() 

                    time.sleep(0.01)
                                   
                    for error in errores:
                        fallo = True
                        aCbrbod.idrenc = None
                        try:
                            aCbrbod.save()
                        except:
                            pass
                        aCbrbode = Cbrbode(idrbod=aCbrbod , coderr=error)
                        aCbrbode.save()
                except Exception as e:
                    print("d")
                    print(e)
                    fallo = True
                    try:
                        aCbrbod.idrenc = None
                        aCbrbod.save() 
                        aCbrbode = Cbrbode(idrbod=aCbrbod ,coderr= 99)
                        aCbrbode.save()
                    except Exception as e:
                        aCbrbod.idrenc = None
                        aCbrbode = Cbrbode(coderr = 99)
                        aCbrbode.save()
                        print("e")
                        print(e)

                #En caso de errores deja solo los errores en la tabla
        if fallo:
            data["error"] = '<p>Verifique errores de banco en <a href=" ../../cbrbode" target="_blank"> Formulario CBF10</a></p>'
    #Caso contrario carga el cbrbcoe
        else:
            print("f")
            Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).delete()
            try:
                Cbrbcod.objects.filter(idrbcoe=Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).first().idrbcoe).delete()
            except Exception as e:
                print(e)
            print("g")
            tableBcoEnc = Cbrbcoe(
                idrbcoe=aCbrenc.idrenc,
                idrenc=aCbrenc,
                fechact1 = dt.datetime.now(tz=timezone.utc),
                idusu1 = request.user.username
                )
            print("h")
            Cbrbcoe.objects.filter( idrenc=aCbrenc.idrenc ).delete()
            tableBcoEnc.save()
            n = 0
            print("i")
            for registro in Cbrbod.objects.order_by("idrbod").filter(idrenc=aCbrbod.idrenc).all():
                if n < 8:
                    time.sleep(1)
                n = n + 1
                tableBco=Cbrbcod(
                fechatra=dt.datetime(aCbrenc.ano, aCbrenc.mes, int(registro.diatra)),
                horatra="00:00:00",
                oficina=registro.oficina,
                desctra=registro.desctra,
                reftra="",
                codtra="",
                debe=float(registro.debe),
                haber=float(registro.haber),
                saldo=float(registro.saldo),
                idrbcoe=tableBcoEnc,
                    )
                saldo = registro.saldo
                tableBco.fechact = dt.datetime.now(tz=timezone.utc)
                tableBco.idusu = request.user.username
                tableBco.save( aCbrenc )
            aCbrenc.recordbco = len( dataBco )
            aCbrenc.saldobco = saldo
            aCbrenc.idusubco=request.user.username
            print("j")
            return True
    except Exception as e:
        print("k")
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
        Cbrgale.objects.all().delete()
        try:
            Cbrerpd.objects.filter(idrbcoe=Cbrerpe.objects.filter( idrerpe=aCbrenc.idrenc ).first().idrerpe).delete()
        except:
            pass
        Cbrerpd.objects.filter( idrerpe=aCbrenc.idrenc ).delete()
        try:
            dataErp=pd.read_csv( str(Path(__file__).resolve().parent.parent)+"/media/" +str( aCbrenc.archivoerp ), header=None, delimiter = "|", index_col=False, names = list(range(0,15)))
        except:
            try:
                dataErp=pd.read_csv( str(Path(__file__).resolve().parent.parent)+"/media/" +str( aCbrenc.archivoerp ), header=None, delimiter = "|", index_col=False, names = list(range(0,15)), encoding= "cp1252")
            except:
                dataErp=pd.read_csv( str(Path(__file__).resolve().parent.parent)+"/media/" +str( aCbrenc.archivoerp ), header=None, delimiter = "|", index_col=False, names = list(range(0,15)), encoding= "ISO-8859-1")
    # quirox, 2021-10-26: 
    #         adicionar un try y si este try cae en except, entonces envie un mensaje de no lectura exitosa y se detiene
        iniciado = False
        pausa = False
        fallo = False
        haberTotal = 0
        debeTotal = 0
        n = 0
        print(1)
        for i in range(1, len( dataErp ) ):
            try:
                print("uno")
                if dataErp.loc[i, dataErp.columns[0]].find("/")>-1:
                    if n < 8:
                        time.sleep(1)
                    else:
                        time.sleep(0.01)
                    if n < 40:
                        print(dataErp.loc[i, dataErp.columns[0]])
                    n= n+1
                    errores = []
                    pausa = False
                    iniciado = True
                    aCbrgal = Cbrgal()
                    aCbrgal.idrenc = aCbrenc
                    s_date=dataErp.loc[i, dataErp.columns[0]]
                    try:
                        fechatra=dt.datetime.strptime( s_date, '%d/%m/%Y' )
                        if fechatra.year != aCbrenc.ano or fechatra.month != aCbrenc.mes:
                            errores.append(1)
                    except:
                        try:
                            s_date2 = s_date[0:-2]+"20"+s_date[-2:]
                            fechatra=dt.datetime.strptime( s_date2, '%d/%m/%Y' )
                            if fechatra.year != aCbrenc.ano or fechatra.month != aCbrenc.mes:
                                errores.append(1)
                        except:
                            fechatra=dataErp.loc[i, dataErp.columns[0]]
                            errores.append(1)
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
                        float(dataErp.loc[i, dataErp.columns[7]].replace(",",""))
                        debe = dataErp.loc[i, dataErp.columns[7]].replace(",","")
                    except:
                        errores.append(3)
                    
                    try:
                        float(dataErp.loc[i, dataErp.columns[9]].replace(",",""))
                        haber = dataErp.loc[i, dataErp.columns[9]].replace(",","")
                    except:
                        errores.append(4)
                    try:
                        if float(debe) > 0 and float(haber) > 0:
                            errores.append(6)
                        if float(debe) == 0 and float(haber) == 0:
                            errores.append(6)
                    except:
                        pass
                    try:
                        float(dataErp.loc[i, dataErp.columns[11]].replace(",",""))
                        saldo = dataErp.loc[i, dataErp.columns[11]].replace(",","")

                    except:
                        try:
                            saldo = "-" + dataErp.loc[i, dataErp.columns[7]][1:-1].replace(",","")
                        except:
                            errores.append(5)
                    s_date=dataErp.loc[i, dataErp.columns[12]]
                    try:
                        fechacon = dt.datetime.strptime( s_date, '%d/%m/%Y' )
                    except:
                        try:
                            s_date2 = s_date[0:-2]+"20"+s_date[-2:]
                            fechacon=dt.datetime.strptime( s_date2, '%d/%m/%Y' )
                        except:
                            errores.append(1)
                    aCbrgal.idusu=request.user.username
                    aCbrgal.fechact=dt.datetime.now(tz=timezone.utc)
                    aCbrgal.debe = debe
                    aCbrgal.haber = haber
                    aCbrgal.saldo = saldo
                    aCbrgal.fechacon = fechacon
                    aCbrgal.fechatra = fechatra
                    if len(errores) > 0:
                        print("1")
                        debe = dataErp.loc[i, dataErp.columns[7]]
                        haber = dataErp.loc[i, dataErp.columns[9]]
                        saldo = dataErp.loc[i, dataErp.columns[11]]
                        fechacon = dataErp.loc[i, dataErp.columns[12]]
                        fechatra = dataErp.loc[i, dataErp.columns[0]]
                    else:
                        haberTotal = float(haber) + haberTotal
                        debeTotal = float(debe) + debeTotal
                        aCbrgal.save(aCbrgal)

                    
                    for error in errores:
                        print("2")
                        print(error)
                        fallo = True
                        try:
                            aCbrgal.idrenc = None
                            aCbrgal.save(aCbrgal)
                        except Exception as e:
                            print(e)
                        aCbrgale = Cbrgale(idrgal=aCbrgal ,coderr = error)
                        aCbrgale.save()
            except Exception as e:
                print("3")
                print(e)
                if dataErp.loc[i, dataErp.columns[4]] != " Van:" and dataErp.loc[i, dataErp.columns[4]] != "TOTALES . . . . . . . " and pausa == False and iniciado:
                    aCbrgal.glosa = str(aCbrgal.glosa) + " " +str(dataErp.loc[i, dataErp.columns[4]])
                    aCbrgal.actualizar(aCbrgal)
                    pausa = True
                if dataErp.loc[i, dataErp.columns[5]] != "Vienen:":
                    pausa = False
                if dataErp.loc[i, dataErp.columns[5]] == "TOTALES . . . . . . . ":
                    if(math.isclose(float(dataErp.loc[i, dataErp.columns[7]].replace(",","")),debeTotal) and math.isclose(float(dataErp.loc[i, dataErp.columns[9]].replace(",","")) , haberTotal)) == False:
                        try:
                            data["error"] = "<p>La suma de debes y la suma de haberes del ERP no coincide con los totales(se esperaba" + str(dataErp.loc[i, dataErp.columns[7]].replace(',','')) + " y " + str(dataErp.loc[i, dataErp.columns[9]].replace(",","")) + "se obtuvo" + str(debeTotal) + " y " + str(haberTotal) + "</p>" + data["error"]
                        except:
                            data["error"] = "<p>La suma de debes y la suma de haberes del ERP no coincide con los totales(se esperaba" + str(dataErp.loc[i, dataErp.columns[7]].replace(',','')) + " y " + str(dataErp.loc[i, dataErp.columns[9]].replace(",","")) + "se obtuvo" + str(debeTotal) + " y " + str(haberTotal) + "</p>"
        if fallo:
            print("4")
            try:
                data["error"] = '<p>Verifique errores de ERP en <a href=" ../../cbrgale" target="_blank"> Formulario CBF11</a></p>'+ data["error"] 
            except:
                data["error"] = '<p>Verifique errores de ERP en  <a href=" ../../cbrgale" target="_blank"> Formulario CBF11</a></p>'
        else:
            print("5")
            try:
                Cbrerpd.objects.filter(idrbcoe=Cbrerpe.objects.filter( idrerpe=aCbrenc.idrenc ).first().idrerpe).delete()
            except:
                pass
            Cbrerpd.objects.filter( idrerpe=aCbrenc.idrenc ).delete()
            print("6")
            tableErpEnc = Cbrerpe(
                idrerpe=aCbrenc.idrenc,
                idrenc=aCbrenc,
                fechact = dt.datetime.now(tz=timezone.utc),
                idusu = request.user.username
                )
            aCbrenc.saldobcoori = aCbrenc.saldobco
            print("7")
            try:
                aCbrenc.corr = Cbrenc.objects.filter(codbco=aCbrenc.codbco,nrocta=aCbrenc.nrocta,ano=aCbrenc.ano, mes=aCbrenc.mes,empresa=aCbrenc.empresa).order_by('-corr')[0].corr + 1
            except:
                aCbrenc.corr = 1
            try:
                aCbrenc.save()
            except:
                aCbrenc.corr = 1
                aCbrenc.save()
            print("8")
            tableErpEnc.save()
            n = 0
            print("9")
            for registro in Cbrgal.objects.order_by("idrgal").filter(idrenc=aCbrenc.idrenc).all():
                if n < 8:
                    time.sleep(1)
                    print("a")
                    print(registro.fechatra)
                else:
                    time.sleep(0.01)
                n = n+1
                
                fechatra = registro.fechatra[0:10]
                fechacon = registro.fechacon[0:10]
                tableErp=Cbrerpd(
                nrotra = 0,
                fechatra=dt.datetime.strptime( fechatra, '%Y-%m-%d' ),
                nrocomp=registro.nrocomp,
                aux = registro.aux,
                ref= registro.ref,
                glosa = registro.glosa, 
                debe=float(registro.debe),
                haber=float(registro.haber),
                saldo=float(registro.saldo),
                fechacon=dt.datetime.strptime( fechacon, '%Y-%m-%d' ),
                idrerpe=tableErpEnc,
                    )
                saldo = registro.saldo
                tableErp.fechact = dt.datetime.now(tz=timezone.utc)
                tableErp.idusu = request.user.username
                tableErp.save( aCbrenc )
            print("10")
            aCbrenc.recorderp = len( dataErp )
            aCbrenc.saldoerp = saldo
            aCbrenc.estado = "0"
            try:
                aCbrenc.difbcoerp = float(aCbrenc.saldobco) - float(saldo)
            except:
                aCbrenc.difbcoerp = 0
            aCbrenc.saldoerpori = aCbrenc.saldoerp
            aCbrenc.fechacons=dt.datetime.now(tz=timezone.utc)
            aCbrenc.idusu=request.user.username
            print("11")
            aCbrenc.save()
            print("12")
            return True
           
    except Exception as e:
        print(e)
        data["error"] = "Problema desconocido en el archivo del ERP"