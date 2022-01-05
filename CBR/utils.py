# EXPLICACION


#region imports
import datetime as dt
import json
from json.decoder import JSONDecodeError
import time
from typing import Union

from django.contrib.auth import logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import transaction
from django.db.models.aggregates import Max
from django.dispatch import receiver
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from CBR.models import (Cbmbco, Cbrbcod, Cbrbcoe, Cbrbod, Cbrenc, Cbrencl, Cbrenct, Cbrerpd, Cbrerpe, Cbrgal, Cbsres, Cbsresc, Cbsusu,
                        Cbtbco, Cbtcli, Cbtcol, Cbtcta, Cbtemp, Cbterr, Cbtlic, Cbtpai, Cbttco, Cbtusu,
                        Cbtusuc, Cbtusue, Cbwres, Cbtcfg, Cbtcfgc)
from pathlib import Path
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from dotenv import dotenv_values
import pydf as htmltopydf
from PyPDF2 import PdfFileMerger, PdfFileReader

#importa las variables de .env
config = dotenv_values(".env")
#endregion

@login_required
def cbtctaDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data = {}
            idtcta = request.POST['idtcta']
            aCbtcta = Cbtcta.objects.get(idtcta=idtcta)
            diccionario = clienteYEmpresas(request)
            if aCbtcta.empresa in diccionario["empresas"] and aCbtcta.cliente == diccionario["cliente"]:

                # verifica que no haya registros posteriores
                if Cbrenc.objects.exclude(estado="3").filter(codbco=aCbtcta.codbco,
                                                             nrocta=aCbtcta.nrocta,
                                                             empresa=aCbtcta.empresa,
                                                             ).exists():
                    data['error'] = "Existen meses posteriores cargados"
                    return JsonResponse(data, safe=False)
                else:
                    aCbtcta.delete()

        except Exception as e:
            print(e)
            data = {}
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request


# ******************************************************************************************************************** #

def chequearNoDobleConexion(request):
    aCbsusu = Cbsusu.objects.filter(
        idusu1=request.user.username).order_by("corrusu").last()
    if aCbsusu == None:
        try:
            logout(request)
        except:
            pass
        return False
    aCbtusu = Cbtusu.objects.filter(
        idusu1=request.user.username).first()
    if aCbtusu.actpas != "A":
        logout(request)
        return False
    aCbtlic = Cbtlic.objects.filter(cliente=clienteYEmpresas(request)["cliente"]).first()
    if aCbtlic.fechalic < dt.datetime.now(tz=timezone.utc):
        logout(request)
        return False
    if request.session["iddesesion"] < aCbsusu.corrusu:
        logout(request)
        return False
    else:
        return True

# ******************************************************************************************************************** #


def clienteYEmpresas(request):
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    empresasHabilitadas = []
    if aCbtusu.tipousu == "S":
        empresas = Cbtemp.objects.filter(cliente=aCbtusu.cliente).all()
        for empresa in empresas:
            empresasHabilitadas.append(empresa.empresa)
    else:
        for empresa in Cbtusue.objects.filter(idtusu=aCbtusu.idtusu).all():
            empresasHabilitadas.append(empresa.empresa)
    return{"cliente": aCbtusu.cliente, "empresas": empresasHabilitadas}


@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    try:
        print("estacosa")
        cerrarCbrenct(request)
        if Cbsusu.objects.filter(
                idusu1=request.user.username, finlogin=None).count()>0:
            
            aCbsusu = Cbsusu.objects.filter(
                idusu1=request.user.username, finlogin=None).order_by("corrusu").first()
            aCbsusu.finlogin = dt.datetime.now(tz=timezone.utc)
            aCbsusu.save()
        else:
            data = {}
            data['error'] = "Debe cerrar sesión en el otro navegador"
            return JsonResponse(data)
    except:
        pass


@csrf_exempt
def cerrarsesionusuario(request):
    usuario = request.POST.get("usuario")
    data = {}
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario, finlogin = None).all()
    for registro in aCbsusu:
        registro.finlogin = dt.datetime.now(tz=timezone.utc)
        registro.save()
    cerrarCbrenct(request)
    return JsonResponse(data)


def login(request):
    
    usuario = request.GET.get("usuario")
   
    aCbtusu = Cbtusu.objects.filter(idusu1=usuario).first()
    aCbtlic = Cbtlic.objects.filter(cliente=aCbtusu.cliente).first()
    usuariosConectados = Cbsusu.objects.filter(finlogin=None, cliente = aCbtusu.cliente).count()
    data = {}
    if dt.datetime.now(tz=timezone.utc) > aCbtlic.fechalic:
        data["vencida"] = True
        data["dia"] = aCbtlic.fechalic
    else:
        data["vencida"] = False
    if usuariosConectados >= aCbtlic.nrousuario:
        data["limite"] = True
    else:
        data["limite"] = False
    if aCbtusu is None:
        data["noexiste"] = True
    else:
        data["noexiste"] = False
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario, finlogin=None).first()
    print("arte")
    print(aCbsusu)
    print(usuario)
    print("artista")
    try:
        
        if aCbsusu is not None:
            data["yaconectado"] = True
            data["iniciodesesion"] = aCbsusu.iniciologin
        else:
            data["yaconectado"] = False
    except Exception as e:
        data["iniciodesesion"] = 0
        data["yaconectado"] = False
        print(e)
    try:
        data["activo"] = aCbtusu.actpas == "A"
    except:
        data["activo"] = False
    try:
        data["reinicia"] = aCbtusu.pasusu
    except:
        data["reinicia"] = False
    return JsonResponse(data)


def reiniciarUsuario(request):
    if request.method == "GET":
        usuario = request.GET.get("usuario")
        return render(request, "registration/reset.html", {"usuario": usuario})
    elif request.method == "POST":
        usuario = request.POST.get("username")
        contra = request.POST.get("password1")
        aCbsusu = Cbtusu.objects.filter(idusu1=usuario).first()
        if aCbsusu.pasusu:
            user = User.objects.filter(username=usuario).first()
            user.password = make_password(contra)
            user.save()
            aCbsusu.pasusu = False
            aCbsusu.save()
        data = {}
        return redirect("/")


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbsusu = Cbsusu.objects.filter(
        idusu1=request.user.username, finlogin = None).all()
    try:
        cliente = aCbtusu.cliente
        idusu1 = request.user.username
        iniciologin = dt.datetime.now(tz=timezone.utc)
        aCbsusu = Cbsusu(cliente=cliente, idusu1=idusu1,
                         iniciologin=iniciologin, fechact=iniciologin, idusu=idusu1)
        aCbsusu.guardar(aCbsusu)
        request.session["iddesesion"] = aCbsusu.corrusu
    except Exception as e:
        try:
            cliente = aCbtusu.cliente
            idusu1 = request.user.username
            iniciologin = dt.datetime.now(tz=timezone.utc)
            aCbsusu = Cbsusu(cliente=cliente, idusu1=idusu1,
                             iniciologin=iniciologin, fechact=iniciologin, idusu=idusu1)
            aCbsusu.guardar(aCbsusu)
            request.session["iddesesion"] = aCbsusu.corrusu
            print(e)
        except Exception as e:
            print(e)
        #cliente = aCbtusu.cliente
        #idusu1 = request.user.username
        #iniciologin = dt.datetime.now(tz=timezone.utc)
        #aCbsusu = Cbsusu(cliente=cliente,idusu1=idusu1,iniciologin=iniciologin,fechact=iniciologin, idusu=idusu1)
        # aCbsusu.guardar(aCbsusu)



# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def cbtusuDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data = {}
            idusu1 = request.POST['idusu1']
            
            aCbtusu = Cbtusu.objects.get(idusu1=idusu1)
            diccionario = clienteYEmpresas(request)
            if aCbtusu.tipousu == "S":
                if Cbtusu.objects.filter(tipousu="S", cliente=diccionario["cliente"]).count() < 2:
                    data = {}
                    data["error"] = "No es posible eliminar el único superusuario"
                    return JsonResponse(data)
            aUser = User.objects.filter(username=idusu1).first()
            try:
                if aUser.is_staff == False:
                    aUser.delete()
            except:
                aUser.delete()
            
            aCbtusurequest = Cbtusu.objects.filter(
                idusu1=request.user.username).first()
            if aCbtusu.cliente == diccionario["cliente"] and aCbtusurequest.tipousu == "S":

                # verifica que no haya registros posteriores
                if Cbrenc.objects.filter(idusucons=idusu1).exists() == False:
                    Cbtusue.objects.filter(idtusu=aCbtusu.idtusu).delete()
                    aCbtusu.delete()

        except Exception as e:
            print(e)
            data = {}
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request


# ******************************************************************************************************************** #
# ********************
@login_required
def cbtempDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data = {}
            idtemp = request.POST['idtemp']
            aCbtemp = Cbtemp.objects.get(idtemp=idtemp)
            diccionario = clienteYEmpresas(request)
            if aCbtemp.empresa in diccionario["empresas"] and aCbtemp.cliente == diccionario["cliente"]:

                # verifica que no haya registros Cargados
                if Cbrenc.objects.exclude(estado="3").filter(
                    empresa=aCbtemp.empresa,
                ).exists():
                    data['error'] = "Existen meses cargados con esta empresa"
                    return JsonResponse(data, safe=False)
                elif Cbtcta.objects.filter(empresa=aCbtemp.empresa).exists():
                    data['error'] = "Existen Una cuenta cargada con esta empresa"
                    return JsonResponse(data, safe=False)                    
                else:
                    aCbtemp.delete()

        except Exception as e:
            print(e)
            data = {}
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def cbtbcoDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data = {}
            idtbco = request.POST['idtbco']
            diccionario = clienteYEmpresas(request)
            aCbtbco = Cbtbco.objects.get(idtbco=idtbco)
            if aCbtbco.cliente == diccionario["cliente"]:

                # verifica que no haya registros Cargados
                if Cbrenc.objects.exclude(estado="3").filter(
                    codbco=aCbtbco.codbco,
                ).exists():
                    data['error'] = "Existen meses cargados con este banco"
                    return JsonResponse(data, safe=False)
                else:
                    aCbtbco.delete()

        except Exception as e:
            print(e)
            data = {}
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@csrf_exempt
def conciliarSaldos(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            idrenc = request.POST.get('idrenc')
            try:
                estado = Cbrenc.objects.get(idrenc=idrenc).estado
            except:
                estado = 1
            if (int(estado) < 2):
                existe = Cbsres.objects.filter(idrenc=idrenc).count()
                sobreescribir = request.POST['sobreescribir']
                # Define si es posible conciliar(es primera vez, se acepto la sobreescritura y el estado no es conciliado ni eliminado)
                if ((sobreescribir == 'true') or (existe == 0)):
                    with transaction.atomic():
                        Cbwres.objects.filter(idrenc=idrenc).delete()
                        aCbrenc=Cbrenc.objects.get(idrenc=idrenc)
                        ano = aCbrenc.ano
                        mes = aCbrenc.mes
                        if mes == 1:
                            mesanterior = 12
                            anoanterior = int(ano)-1
                        else:
                            mesanterior = int(mes) - 1
                            anoanterior = int(ano)
                        data = {}
                        # Define los objetos a cargar y los saldos iniciales
                        aCbrencAnterior= Cbrenc.objects.filter(ano=anoanterior, mes=mesanterior, cliente=aCbrenc.cliente, empresa=aCbrenc.empresa, codbco=aCbrenc.codbco, estado=2).first()
                        if aCbrencAnterior is not None:
                            bcoDataSetAnterior =  Cbsres.objects.filter(estadobco=0, fechatrabco__isnull=False, idrenc=aCbrencAnterior.idrenc).order_by("-fechatrabco")
                        else:
                            bcoDataSetAnterior = []
                        print("PASA POR ACA")
                        aCbrbcoe = Cbrbcoe.objects.get(idrenc=idrenc)
                        bcoDataSet = list(Cbrbcod.objects.filter(
                            idrbcoe=aCbrbcoe.idrbcoe).order_by('fechatra', 'horatra','idrbcod'))
                        print("POR ACA NO")
                        
                        for element in bcoDataSetAnterior:
                            if Cbttco.objects.filter(codtco=element.codtcobco,indtco=2, indpend=0).exists() == False:
                                aUnir = Object()
                                aUnir.idrbcod= element.idrbcod
                                aUnir.fechatra=element.fechatrabco
                                aUnir.horatra=element.horatrabco
                                aUnir.oficina=element.oficina
                                aUnir.desctra=element.desctra
                                aUnir.reftra=element.reftra
                                aUnir.codtra=element.codtra
                                aUnir.debe=element.debebco
                                aUnir.haber=element.haberbco
                                aUnir.saldo=element.saldobco
                                try:
                                    aUnir.codtcobco=element.codtcobco
                                except:
                                    aUnir.codtcobco=""
                                aUnir.idrbcoe=Cbrbcoe.objects.filter(idrenc=element.idrenc).first()
                                bcoDataSet.insert(0,aUnir)
                        if aCbrencAnterior is not None:
                            erpDataSetAnterior = Cbsres.objects.filter(estadoerp=0, fechatraerp__isnull=False, idrenc=aCbrencAnterior.idrenc).order_by("-fechatraerp")
                        else:
                            erpDataSetAnterior = []
                        print("LLEGA ACA")
                        aCbrerpe = Cbrerpe.objects.get(idrenc=idrenc)
                        erpDataSet = list(Cbrerpd.objects.filter(
                            idrerpe=aCbrerpe.idrerpe).order_by('fechatra','idrerpd'))
                        for element in erpDataSetAnterior:
                            if Cbttco.objects.filter(codtco=element.codtcoerp, indtco=1, indpend=0).exists()==False:
                                aUnir = Object()
                                aUnir.idrerpd = element.idrerpd
                                aUnir.nrotra = element.nrotraerp
                                aUnir.fechatra = element.fechatraerp
                                aUnir.nrocomp = element.nrocomperp
                                aUnir.aux = element.auxerp
                                aUnir.ref = element.referp
                                aUnir.glosa = element.glosaerp
                                aUnir.debe = element.debeerp
                                aUnir.haber = element.habererp
                                aUnir.saldo = element.saldoerp
                                aUnir.fechacon = element.fechaconerp
                                aUnir.codtcoerp=element.codtcoerp
                                aUnir.idrerpe=Cbrerpe.objects.filter(idrenc=element.idrenc).first()
                                ##Completar con el resto de las cosas
                                erpDataSet.insert(0,aUnir)

                        rowInicialbco = Cbrbcod.objects.filter(
                            idrbcoe=aCbrbcoe.idrbcoe).order_by('fechatra', 'horatra').first()

                        rowInicialerp = Cbrerpd.objects.filter(
                            idrerpe=aCbrerpe.idrerpe).order_by('fechatra').first()

                        currentDay = rowInicialbco.fechatra
                        Cbsres.objects.filter(idrenc=idrenc).delete()
                        color = 0
                        cambio = False
                        
                        diaMenor = dt.datetime.date(dt.datetime.strptime("01/01/2030", "%d/%m/%Y"))
                        diaMayor = dt.datetime.date(dt.datetime.strptime("01/01/2010", "%d/%m/%Y"))
                        for vwRow in bcoDataSet:
                            if vwRow.fechatra < diaMenor:
                                diaMenor = vwRow.fechatra
                            if vwRow.fechatra > diaMayor:
                                diaMayor = vwRow.fechatra
                        for vwRow in erpDataSet:
                            if vwRow.fechatra < diaMenor:
                                diaMenor = vwRow.fechatra
                            if vwRow.fechatra > diaMayor:
                                diaMayor = vwRow.fechatra
                        dia = diaMenor
                        while dia <= diaMayor:
                            # Para cada dia carga los registros del banco en orden, calculando los saldos
                            fechatrabco = None
                            for vwRow in bcoDataSet:
                                if vwRow.fechatra == dia:
                                    fechatrabco = vwRow.fechatra
                                    if (vwRow.fechatra is None):
                                        if (currentDay != vwRow.fechatra):
                                            currentDay = vwRow.fechatra
                                    
                                    insCbsres = Cbsres(
                                        idrenc=Cbrenc.objects.get(idrenc=idrenc),
                                        cliente=Cbrenc.objects.get(
                                            idrenc=idrenc).cliente,
                                        empresa=Cbrenc.objects.get(
                                            idrenc=idrenc).empresa,
                                        saldobco=vwRow.saldo,
                                        idrbcod=vwRow.idrbcod,
                                        oficina=vwRow.oficina,
                                        desctra=vwRow.desctra,
                                        reftra=vwRow.reftra,
                                        codtra=vwRow.codtra,
                                        # isconciliado=vwRow.isconciliado,
                                        # estado=vwRow.esta,
                                        # historial=vwRow.,
                                        # --------------------
                                        fechatrabco=vwRow.fechatra,
                                        horatrabco=vwRow.horatra,
                                        debebco=vwRow.debe,
                                        haberbco=vwRow.haber,
                                        codbco=Cbrenc.objects.get(
                                            idrenc=idrenc).codbco,
                                        nrocta=Cbrenc.objects.get(
                                            idrenc=idrenc).nrocta,
                                        ano=Cbrenc.objects.get(idrenc=idrenc).ano,
                                        mes=Cbrenc.objects.get(idrenc=idrenc).mes,
                                        estadobco=0,
                                        pautado=color
                                        # --------------------
                                    )
                                    try:
                                        insCbsres.codtcobco=vwRow.codtcobco
                                    except:
                                        insCbsres.codtcobco=""
                                    insCbsres.fechact = dt.datetime.now(
                                        tz=timezone.utc)
                                    insCbsres.idusu = request.user.username
                                    insCbsres.save()
                                    cambio = True
                            # for vwRow in erpDataSet:
                            #    #Para cada dia carga los registros del erp que coincilian
                            #    if vwRow.fechatra.day == dia:
                            #            if Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).exists():
                            #                insCbsres=Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).first()
                            #                Unir(vwRow,insCbsres,idrenc,color)
                            #                erpDataSet = erpDataSet.exclude(idrerpd=vwRow.idrerpd)
                            for vwRow in erpDataSet:
                                # Para cada dia carga los registros del erp que no concilian en  orden de cercania
                                if vwRow.fechatra == dia:
                                    if fechatrabco != 0 and Cbsres.objects.filter(idrenc=idrenc, idrerpd=0, fechatrabco=fechatrabco).exists():
                                        insCbsres = Cbsres.objects.filter(
                                            idrenc=idrenc, idrerpd=0, fechatrabco=fechatrabco).first()
                            #            insCbsres = Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco).annotate(abs_diff=Func(F('debebco') - vwRow.haber + F('haberbco') - vwRow.debe, function='ABS')).order_by('abs_diff').first()
                                    else:
                                        try:
                                            insCbsres = Cbsres(idrenc=Cbrenc.objects.get(
                                                idrenc=idrenc), pautado=color)
                                        except:
                                            insCbsres = Cbsres(
                                                idrenc=Cbrenc.objects.get(idrenc=idrenc))
                                    Unir(vwRow, insCbsres, idrenc, color)
                            dia = dia + dt.timedelta(days=1)
                            if cambio == True:
                                if color == 0:
                                    color = 1
                                else:
                                    color = 0
                                cambio = False
                        conciliacioAutoySemiAuto(request, idrenc, aCbrenc)
                        CbrencUpd = Cbrenc.objects.get(idrenc=idrenc)
                        CbrencUpd.fechacons = dt.datetime.now(tz=timezone.utc)
                        CbrencUpd.idusucons = request.user.username
                        CbrencUpd.save()
                        if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
                            bCbrenct = Cbrenct.objects.filter(
                                idusu=request.user.username, fechorafin=None).first()
                            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
                            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                            bCbrenct.save()
                        aCbrenct = Cbrenct(
                            formulario="CBF02", idrenc=Cbrenc.objects.filter(idrenc=idrenc).first())
                        aCbrenct.idusu = request.user.username
                        aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
                        aCbrenct.accion = 2
                        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
                        aCbrenct.save()
                        data = {"idrenc": idrenc}
                else:
                    hist = Cbrenc.objects.get(idrenc=idrenc)
                    data = {
                        "existe_info": "¿Desea sobreescribir la conciliación anterior?"}
                    data['fechacons'] = hist.fechacons.strftime(
                        '%d-%m-%Y %H:%M:%S')
                    data['idusucons'] = hist.idusucons

            else:
                data = {"info": "La conciliación ya fue cerrada"}
        except Exception as e:
            data = {}
            print(e)
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request

def conciliacioAutoySemiAuto(request, idrenc, aCbrenc):
    n = 0
    primerRegistro = False
    for aCbsres in Cbsres.objects.filter(idrenc=idrenc).order_by('idsres').all():
        if n == 0:
            if primerRegistro == False:
                fecha = aCbsres.fechatrabco
                if fecha == None:
                    fecha = aCbsres.fechatraerp
                if fecha.year == aCbrenc.ano and fecha.month == aCbrenc.mes:
                    primerRegistro = True
            if primerRegistro:
                n = 1
                saldoacumesbco = float(aCbsres.saldobco or 0)
                saldoacumdiabco = float(
                                        aCbsres.haberbco or 0)-float(aCbsres.debebco or 0)
                saldoacumeserp = float(aCbsres.saldoerp or 0)
                saldoacumdiaerp = float(
                                        aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
                saldodiferencia = saldoacumesbco - saldoacumeserp
                diabcoant = aCbsres.fechatrabco
                diaerpant = aCbsres.fechatraerp
                aCbsres.saldodiferencia = saldodiferencia
                aCbsres.saldoacumesbco = saldoacumesbco
                aCbsres.saldoacumdiabco = saldoacumdiabco
                aCbsres.saldoacumeserp = saldoacumeserp
                aCbsres.saldoacumdiaerp = saldoacumdiaerp
                aCbsres.fechact = dt.datetime.now(tz=timezone.utc)
                aCbsres.idusualt = request.user.username
                aCbsres.save()
        else:
            diabco = aCbsres.fechatrabco
            diaerp = aCbsres.fechatraerp
            saldoacumesbco = saldoacumesbco + \
                                    float(aCbsres.haberbco or 0) - \
                                    float(aCbsres.debebco or 0)
            if diabco == diabcoant or diaerp == diaerpant:
                saldoacumdiabco = saldoacumdiabco + \
                                        float(aCbsres.haberbco or 0) - \
                                        float(aCbsres.debebco or 0)
                saldoacumdiaerp = float(
                                        saldoacumdiaerp or 0)+float(aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
            else:
                saldoacumdiabco = float(
                                        aCbsres.haberbco or 0)-float(aCbsres.debebco or 0)
                saldoacumdiaerp = float(
                                        aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
            saldoacumeserp = saldoacumeserp + \
                                    float(aCbsres.debeerp or 0) - \
                                    float(aCbsres.habererp or 0)
            saldodiferencia = saldoacumesbco - saldoacumeserp
            aCbsres.saldoacumesbco = saldoacumesbco
            aCbsres.saldoacumdiabco = saldoacumdiabco
            aCbsres.saldoacumeserp = saldoacumeserp
            aCbsres.saldoacumdiaerp = saldoacumdiaerp
            aCbsres.saldodiferencia = saldodiferencia
            diabcoant = diabco
            diaerpant = diaerp
            aCbsres.fechact = dt.datetime.now(tz=timezone.utc)
            aCbsres.idusualt = request.user.username
            aCbsres.save()
    n = 0
    listado = Cbsres.objects.filter(
                                idrenc=idrenc).order_by('idsres')
    while n < Cbsres.objects.filter(idrenc=idrenc).count():
        aCbsres = listado[n]
        if Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco, debebco=aCbsres.debebco, haberbco=aCbsres.haberbco).count() == 1:
            if Cbsres.objects.filter(idrenc=idrenc, fechatraerp=aCbsres.fechatrabco, debeerp=aCbsres.haberbco, habererp=aCbsres.debebco).count() == 1:
                bCbsres = Cbsres.objects.filter(
                                        idrenc=idrenc, fechatraerp=aCbsres.fechatrabco, debeerp=aCbsres.haberbco, habererp=aCbsres.debebco).first()
                aCbsres.estadobco = 1
                bCbsres.estadoerp = 1
                aCbsres.idrerpdl = bCbsres.idrerpd
                bCbsres.idrbcodl = aCbsres.idrbcod
                aCbsres.save()
                bCbsres.save()
                if bCbsres.debeerp == bCbsres.haberbco and bCbsres.habererp == bCbsres.debebco:
                    bCbsres.estadobco = 1
                    bCbsres.idrerpdl = bCbsres.idrerpd
                    bCbsres.save()
        n = n+1
                        ### CONCILIACION SEMI AUTOMATICA
                        
                        #Si aparece despues en el banco
    cliente = clienteYEmpresas(request)["cliente"]
    if Cbtcfg.objects.filter(codcfg=1, actpas="A", cliente=cliente).exists():
        conciliarBancoFechaPosterior(idrenc)
                        #Si aparece despues en el ERP
    if Cbtcfg.objects.filter(codcfg=2, actpas="A", cliente=cliente).exists():
        conciliarErpFechaPosterior(idrenc)
    for aCbtcfgc in Cbtcfgc.objects.filter(idtcfg__cliente=cliente, idtcfg__actpas="A").order_by("ordencfg"):
        campoBco = aCbtcfgc.campobco
        campoErp = aCbtcfgc.campoerp
                            #Si las referencias son iguales
        conciliarCamposIguales(idrenc,campoBco,campoErp)
                        
    tiposDeConciliacion = json.loads(getTiposDeConciliacion(request,idrenc).content)
    aCbrenc = Cbrenc.objects.filter(idrenc=idrenc).first()
    aCbrenc.saldobco = tiposDeConciliacion["saldobcototal"]
    aCbrenc.saldoerp = tiposDeConciliacion["saldoerptotal"]
    aCbrenc.difbcoerp = tiposDeConciliacion["saldodiferenciatotal"]
    aCbrenc.save()

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #



def conciliarCamposIguales(idrenc,campoBco, campoErp):
    if campoBco != "" and campoErp != "":
        n = 0
        listado = Cbsres.objects.filter(
                                idrenc=idrenc).order_by('idsres')
        while n < Cbsres.objects.filter(idrenc=idrenc).count():
            aCbsres = listado[n]
            if aCbsres.estadoerp == 0:

                bCbsresraw = Cbsres.objects.raw("SELECT * FROM cbsres where idrenc= %s and "+campoBco+"=%s and estadobco = 0 LIMIT 1", [str(idrenc), str(aCbsres.toJSON()[campoErp])])
                bCbsres = None
                for element in bCbsresraw:
                    bCbsres = element
                if bCbsres is not None:
                    bCbsres.estadobco = 2
                    bCbsres.idrerpdl = aCbsres.idrerpd
                    aCbsres.idrbcodl = bCbsres.idrbcod
                    aCbsres.estadoerp = 2
                    aCbsres.save()
                    bCbsres.save()

            n = n+1
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def conciliarErpFechaPosterior(idrenc):
    n = 0
    listado = Cbsres.objects.filter(
                            idrenc=idrenc).order_by('idsres')
    while n < Cbsres.objects.filter(idrenc=idrenc).count():
        aCbsres = listado[n]
        if aCbsres.estadobco == 0 and aCbsres.debebco is not None:
            bCbsres = Cbsres.objects.filter(idrenc=idrenc, estadoerp=0, fechatraerp__gt=aCbsres.fechatrabco, habererp=aCbsres.debebco, debeerp=aCbsres.haberbco).first()
            if bCbsres is not None:
                aCbsres.estadobco = 2
                aCbsres.idrerpdl = bCbsres.idrerpd
                bCbsres.idrbcodl = aCbsres.idrbcod
                bCbsres.estadoerp = 2
                aCbsres.save()
                bCbsres.save()

        n = n+1
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

def conciliarBancoFechaPosterior(idrenc):
    n = 0
    listado = Cbsres.objects.filter(
                            idrenc=idrenc).order_by('idsres')
    while n < Cbsres.objects.filter(idrenc=idrenc).count():
        aCbsres = listado[n]
        if aCbsres.estadoerp == 0 and aCbsres.debeerp is not None:
            bCbsres = Cbsres.objects.filter(idrenc=idrenc, estadobco = 0, fechatrabco__gt=aCbsres.fechatraerp, haberbco=aCbsres.debeerp, debebco=aCbsres.habererp).first()
            if bCbsres is not None:
                aCbsres.estadoerp = 2
                bCbsres.idrerpdl = aCbsres.idrerpd
                aCbsres.idrbcodl = bCbsres.idrbcod
                bCbsres.estadobco = 2
                aCbsres.save()
                bCbsres.save()

        n = n+1

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def Unir(vwRow, insCbsres, idrenc, color):
    # sistema que une el cbsres con banco cargado con un registro del cbrerpd
    insCbsres.idrenc=Cbrenc.objects.get(idrenc=idrenc)
    insCbsres.cliente=Cbrenc.objects.get(idrenc=idrenc).cliente
    insCbsres.empresa=Cbrenc.objects.get(idrenc=idrenc).empresa
    insCbsres.idrerpd = vwRow.idrerpd

    insCbsres.saldoerp = vwRow.saldo

    # estado=vwRow.esta,
    # historial=vwRow.,
    # --------------------
    insCbsres.fechatraerp = vwRow.fechatra
    insCbsres.debeerp = vwRow.debe
    insCbsres.habererp = vwRow.haber
    try:
        insCbsres.codtcoerp = vwRow.codtcoerp
    except:
        insCbsres.codtcoerp = ""
    if insCbsres.saldodiferencia == 0:
        insCbsres.historial = 3
    insCbsres.nrotraerp = vwRow.nrotra
    insCbsres.fechatraerp = vwRow.fechatra
    insCbsres.nrocomperp = vwRow.nrocomp
    insCbsres.auxerp = vwRow.aux
    insCbsres.referp = vwRow.ref
    insCbsres.glosaerp = vwRow.glosa
    insCbsres.fechaconerp = vwRow.fechacon
    insCbsres.pautado = color

    insCbsres.estadobco = 0
    insCbsres.estadoerp = 0

    # --------------------
    insCbsres.save()
    cambio = True

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def editCbwres(request):
    try:
        idrenc = None
        tabla = list(dict(request.POST).keys())[0][1:-1]
        print(tabla[:200])
        while True:
            
            fila = tabla[:tabla.find("}")+1]
            comienzo = tabla[10:].find("{")

            fila = json.loads(fila)
            idsres = fila["idsres"]
            idrenc = float(fila["idrenc"])
            aCbwsres = Cbwres.objects.filter(idsres=int(idsres)).first()
            if aCbwsres is None:
                aCbsres = Cbsres.objects.filter(idsres=int(idsres)).first()
                aCbwsres = Cbwres(idrbcodl=aCbsres.idrbcodl, idrerpdl=aCbsres.idrerpdl, idsres=idsres, idrenc=aCbsres.idrenc, cliente=aCbsres.cliente, empresa=aCbsres.empresa, codbco=aCbsres.codbco, nrocta=aCbsres.nrocta, ano=aCbsres.ano, mes=aCbsres.mes, fechatrabco=aCbsres.fechatrabco, horatrabco=aCbsres.horatrabco, saldobco=aCbsres.saldobco, oficina=aCbsres.oficina, desctra=aCbsres.desctra, reftra=aCbsres.reftra, codtra=aCbsres.codtra, idrbcod=aCbsres.idrbcod,
                             nrotraerp=aCbsres.nrotraerp, fechatraerp=aCbsres.fechatraerp, nrocomperp=aCbsres.nrocomperp, auxerp=aCbsres.auxerp, referp=aCbsres.referp, glosaerp=aCbsres.glosaerp, saldoerp=aCbsres.saldoerp, saldoacumdiaerp=aCbsres.saldoacumdiaerp, fechaconerp=aCbsres.fechaconerp, idrerpd=aCbsres.idrerpd, debebco=aCbsres.debebco, haberbco=aCbsres.haberbco, saldoacumesbco=aCbsres.saldoacumesbco)
            try:
                aCbwsres.debeerp = float(fila["debeerp"])
            except:
                aCbwsres.debeerp = None
            try:
                aCbwsres.habererp = float(fila["habererp"])
            except:
                aCbwsres.habererp = None
            try:
                aCbwsres.saldoacumeserp = float(fila["saldoacumeserp"])
            except:
                aCbwsres.saldoacumeserp = float(0)
            try:
                aCbwsres.saldoacumdiaerp = float(fila["saldoacumdiaerp"])
            except:
                aCbwsres.saldoacumdiaerp = float(0)
            try:
                aCbwsres.saldodiferencia = float(fila["saldodiferencia"])
            except:
                aCbwsres.saldodiferencia = float(0)
            aCbwsres.historial = int(fila["historial"])
            try:
                aCbwsres.idrbcodl = int(fila["idrbcodl"])
            except:
                aCbwsres.idrbcodl = int(0)
            try:
                aCbwsres.idrerpdl = int(fila["idrerpdl"])
            except:
                aCbwsres.idrerpdl = int(0)
            try:
                aCbwsres.codtcobco = fila["codtcobco"]
            except Exception as e:
                print(e)
                aCbwsres.codtcobco = ""
            try:
                aCbwsres.codtcoerp = fila["codtcoerp"]
            except:
                aCbwsres.codtcoerp = ""
                

            print("A")
            #print(fila["codtcobco"])
            aCbwsres.estadobco = fila["estadobco"]
            aCbwsres.estadoerp = fila["estadoerp"]
            
            aCbwsres.idusu = request.user.username
            
            
            aCbwsres.save()
            if comienzo == -1:
                break
            tabla = tabla[comienzo+10:]
        return HttpResponse("")
    except Exception as e:
        print("ACA")
        print(e)
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


@login_required
def cerrarConciliacion(request):
    chequearNoDobleConexion(request)
    if request.method == 'POST':
        try:
            idrenc = request.POST.get('idrenc')
            CbrencUpd = Cbrenc.objects.get(idrenc=idrenc)
            diccionario = clienteYEmpresas(request)
            if CbrencUpd.empresa in diccionario["empresas"] and CbrencUpd.cliente == diccionario["cliente"]:
                guardado(idrenc,request)
                CbrencUpd = Cbrenc.objects.get(idrenc=idrenc)
                lista = Cbsres.objects.filter(idrenc=idrenc).all()
                error = False
                if CbrencUpd.difbcoerp != 0:
                    data={}
                    data["exito"] = False
                    data["error"] = "El saldo no es 0, es " +str(CbrencUpd.difbcoerp)
                    return JsonResponse(data)
                for aCbsres in lista:
                    if (aCbsres.estadobco == 0 and (aCbsres.codtcobco == "" or aCbsres.codtcobco == None) and aCbsres.fechatrabco is not None or (aCbsres.estadoerp == 0 and (aCbsres.codtcoerp == "" or aCbsres.codtcoerp == None) and aCbsres.fechatraerp is not None)):
                        error = True
                        data={}
                        data["exito"] = False
                        data["error"] = "El idsres " + str(aCbsres.idsres) + " no se encuentra conciliado ni tiene un código de conciliación"
                        return JsonResponse(data)
                CbrencUpd.estado = 2
                CbrencUpd.save()
                data = {"idrenc": idrenc}
                if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
                    bCbrenct = Cbrenct.objects.filter(
                        idusu=request.user.username, fechorafin=None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(
                    formulario="CBF02", idrenc=Cbrenc.objects.filter(idrenc=idrenc).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
                aCbrenct.accion = 2
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
                aCbrenct.save()
                data={}
                data["exito"] = True
                return JsonResponse(data)

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return None


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def getanomes(request):
    chequearNoDobleConexion(request)
    empresa = request.GET.get('empresa')
    codbco = request.GET.get('banco')
    nrocta = request.GET.get('cuenta')
    cliente = clienteYEmpresas(request)["cliente"]
    try:
        maxAno = Cbrenc.objects.exclude(estado="3").filter(empresa=empresa,
            codbco=codbco, nrocta=nrocta, cliente=cliente).aggregate(Max('ano'))
        maxAno = maxAno['ano__max']
        if maxAno is None:
            aCbtcta = Cbtcta.objects.filter(empresa=empresa,
                codbco=codbco, nrocta=nrocta, cliente=cliente).first()
            if aCbtcta is None:
                data = {'ano': 0, 'mes': 0}
            maxAno = aCbtcta.ano
            maxMes = aCbtcta.mes
            if maxMes < 12:
                data = {'ano': maxAno, 'mes': maxMes + 1}
            else:
                data = {'ano': maxAno + 1, 'mes': 1}
        else:
            maxMes = Cbrenc.objects.exclude(estado="3").filter(empresa=empresa, codbco=codbco, nrocta=nrocta, ano=maxAno, cliente=cliente).aggregate(
                Max('mes'))
            maxMes = maxMes['mes__max']
            if maxMes < 12:
                data = {'ano': maxAno, 'mes': maxMes + 1}
            else:
                data = {'ano': maxAno + 1, 'mes': 1}
    finally:
        return JsonResponse(data)

@login_required
def getcuenta(request):
    chequearNoDobleConexion(request)
    empresa = request.GET.get('empresa')
    codbco = request.GET.get('banco')
    cuentas=[]
    for cuenta in Cbtcta.objects.filter(empresa=empresa, codbco=codbco, cliente=clienteYEmpresas(request)["cliente"]).order_by("nrocta"):
        cuentas.append({"nombre": cuenta.nrocta, "descripcion": cuenta.descta})
    data = {}
    data["cuentas"]=cuentas
    return JsonResponse(data, safe=False)


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def getdesbco(request):
    chequearNoDobleConexion(request)
    codbco = request.GET.get('codbco')
    data = {}
    try:
        algo = Cbmbco.objects.filter(codbco=codbco).first()
        data["desbco"] = Cbmbco.objects.filter(codbco=codbco).first().desbco
    except Exception as e:
        print(e)
        data["desbco"] = ""
    return JsonResponse(data)


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

@login_required
def getguardado(request):
    chequearNoDobleConexion(request)
    data = {"guardado": "si"}
    idrenc = request.GET.get('idrenc')
    if Cbwres.objects.filter(idrenc=idrenc, debeerp=0, habererp=0).exists():
        alertaGuardado = str(Cbwres.objects.filter(
            idrenc=idrenc, debeerp=0, habererp=0).first().idsres)
        data = {
            "guardado": "Debe y Haber no pueden ser 0 en IDSRES = " + alertaGuardado}
    else:
        for registro in Cbwres.objects.filter(idrenc=idrenc).all():
            if registro.idrerpd != 0:
                aCbrerpd = Cbrerpd.objects.filter(idrerpd=registro.idrerpd).first()
                if (aCbrerpd.debe != registro.debeerp or aCbrerpd.haber != registro.habererp) and (registro.codtcoerp == "" or registro.codtcoerp == None):
                    data = {
                        "guardado": "Explique la modificacion en IDSRES =" + str(registro.idsres)}
    return JsonResponse(data)


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


@login_required
def getTiposDeConciliacionpost(request):
    idrenc = request.GET.get("idrenc")
    data = getTiposDeConciliacion(request, idrenc)
    return JsonResponse(json.loads(data.content))

def getTiposDeConciliacion(request, idrenc):
    data = {"debebcototal": 0, "haberbcototal": 0, "saldobcototal": 0, "debeerptotal": 0,
            "habererptotal": 0, "saldoerptotal": 0, "saldodiferenciatotal": 0, "puedeCerrar": 1}
    yaTomadas = []
    n = 0
    m = 0
    # calcula
    listadoSumaDebe = []
    listadoSumaHaber = []
    for tipo in Cbttco.objects.all():
        if tipo.indsuma == 1:
            if tipo.inddebhab == "H":
                listadoSumaDebe.append(tipo.codtco)
            elif tipo.inddebhab == "D":
                listadoSumaHaber.append(tipo.codtco)


            

    
    saldoextrabco = 0
    saldoextraerp = 0
    # Listado de quienes tienen codigo para la tabla de respectiva
    data["listado"] = []

    # calcula primero las del cbwres y si no existen las del cbsres
    primerRegistroBanco = False
    primerRegistroErp =False
    primerRegistro = False
    aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
    sumaBco = 0
    sumaErp = 0
    for registro in Cbsres.objects.filter(idrenc=idrenc).order_by("idsres").all():
        registroAnalizado = Cbwres.objects.filter(idsres=registro.idsres).first()
        if registroAnalizado is None:
            registroAnalizado = registro
        if data["puedeCerrar"]==1:
            if registroAnalizado.estadobco == 0 and registroAnalizado.fechatrabco is not None and registroAnalizado.codtcobco == "":
                data["puedeCerrar"]=0
            if registroAnalizado.estadoerp == 0  and registroAnalizado.fechatraerp is not None and registroAnalizado.codtcoerp =="":
                data["puedeCerrar"]=0
            if (registroAnalizado.historial == 2 or registroAnalizado.historial ==4) and registroAnalizado.codtcoerp =="":
                data["puedeCerrar"]=0
        if primerRegistroBanco == False:
            try:
                fecha = registroAnalizado.fechatrabco
                saldoinicialbco=registroAnalizado.saldoacumesbco+registroAnalizado.debebco-registroAnalizado.haberbco
                primerRegistroBanco = True
            except:
                pass
        if primerRegistroErp ==False:
            try:
                saldoinicialerp=registroAnalizado.saldoacumeserp+registroAnalizado.habererp-registroAnalizado.debeerp
                primerRegistroErp = True
            except:
                pass
        if primerRegistro == False:
            if fecha == None:
                fecha = registroAnalizado.fechatraerp
            if fecha.year == aCbrenc.ano and fecha.month == aCbrenc.mes:
                primerRegistro = True
        if primerRegistro:
            try:
                data["debeerptotal"] = registroAnalizado.debeerp + \
                    data["debeerptotal"]
            except:
                pass
            try:
                data["habererptotal"] = registroAnalizado.habererp + \
                    data["habererptotal"]
            except:
                pass
            if registroAnalizado.codtcoerp in listadoSumaDebe:
                try:
                    data["debebcototal"] = registroAnalizado.habererp + \
                        data["debebcototal"]
                except:
                    pass
            elif registroAnalizado.codtcoerp in listadoSumaHaber:
                try:
                    data["haberbcototal"] = registroAnalizado.debeerp + \
                        data["haberbcototal"]
                except:
                    pass
            try:
                data["debebcototal"] = registroAnalizado.debebco + \
                    data["debebcototal"]
            except:
                pass
            try:
                data["haberbcototal"] = registroAnalizado.haberbco + \
                    data["haberbcototal"]
            except:
                pass
            if registroAnalizado.codtcobco in listadoSumaDebe:
                try:
                    data["debeerptotal"] = registroAnalizado.haberbco + \
                        data["debeerptotal"]
                except:
                    pass
            elif registroAnalizado.codtcobco in listadoSumaHaber:
                try:
                    data["habererptotal"] = registroAnalizado.debebco + \
                        data["habererptotal"]
                except:
                    pass
    try:
        data["saldobcototal"] = data["haberbcototal"] - data["debebcototal"] + saldoinicialbco
    except:
        data["saldobcototal"] = data["haberbcototal"] - data["debebcototal"]
    try:
        data["saldoerptotal"] = data["debeerptotal"] - data["habererptotal"] + saldoinicialerp
    except:
        data["saldoerptotal"] = data["debeerptotal"] - data["habererptotal"]
    data["saldodiferenciatotal"] = data["saldobcototal"] - data["saldoerptotal"]


    return JsonResponse(data)





def getPais(codigo):
    idpais = codigo[0:2]
    aCbtpai = Cbtpai.objects.filter(codpai=idpais).first()
    return aCbtpai.despai


def getColumnas(request):
    n = 0
    columnas = {}
    while n < 33:
        if Cbtusuc.objects.filter(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu, codcol=n).exists():
            columnas[n] = True
        else:
            columnas[n] = False
        n = n+1

    return JsonResponse(columnas)


def updateCbtusue(request):
    fila = request.POST["fila"]
    checked = request.POST["checked"]
    usuario = fila[0:fila.find("--")]
    empresa = fila[fila.find("--")+2:]
    if checked == "false":
        Cbtusue.objects.filter(empresa=empresa, idtusu=Cbtusu.objects.filter(
            idusu1=usuario).first()).delete()
    else:
        aCbtusue = Cbtusue(idtusu=Cbtusu.objects.filter(
            idusu1=usuario).first(), empresa=empresa, actpas="A")
        aCbtusue.save()

    return JsonResponse({})

@login_required
def resetPassword(request):
    usuario = request.GET.get("usuario")

    aCbtusu = Cbtusu.objects.filter(idusu1=usuario).first()
    aCbtusu.pasusu = True
    aCbtusu.save()
    return redirect("../")

def CbtusucGuardar(request):
    try:
        Cbtusuc.objects.filter(idtusu=Cbtusu.objects.filter(
            idusu1=request.user.username).first().idtusu).delete()
        i = 0
        while i < 34:
            clave = 'cbtusuc['+str(i)+']'

            if request.POST[clave] == "true":
                aCbtusuc = Cbtusuc(codcol=i)
                aCbtusuc.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtusuc.idusu = request.user.username
                aCbtusuc.idtusu = Cbtusu.objects.filter(
                    idusu1=request.user.username).first().idtusu
                aCbtusuc.save()
            i = i+1
    except Exception as e:
        print(e)
        pass
    return JsonResponse({})

def eliminarGuardado(request):
    idrenc = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
        bCbrenct = Cbrenct.objects.filter(
            idusu=request.user.username, fechorafin=None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario="CBF02",
                       idrenc=Cbrenc.objects.filter(idrenc=idrenc).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
    aCbrenct.accion = 10
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
    aCbrenct.save()

    Cbwres.objects.filter(idrenc=idrenc).delete()

    return redirect("../../cbsres/?idrenc="+idrenc)

def guardado(idrenc, request):
    if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
        bCbrenct = Cbrenct.objects.filter(
            idusu=request.user.username, fechorafin=None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario="CBF02",
                       idrenc=Cbrenc.objects.filter(idrenc=idrenc).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
    aCbrenct.accion = 4
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
    aCbrenct.save()
    with transaction.atomic():
        while Cbwres.objects.filter(idrenc=idrenc).exists():
            idsres = Cbwres.objects.filter(idrenc=idrenc).first().idsres
            aCbwres = Cbwres.objects.filter(idsres=idsres).first()
            aCbsres = Cbsres.objects.filter(idsres=idsres).first()
            aCbsres.debeerp = aCbwres.debeerp
            aCbsres.habererp = aCbwres.habererp
            aCbsres.historial = aCbwres.historial
            aCbsres.saldoacumeserp = aCbwres.saldoacumeserp
            aCbsres.saldoacumdiaerp = aCbwres.saldoacumdiaerp
            aCbsres.saldodiferencia = aCbwres.saldodiferencia
            aCbsres.idrbcodl = aCbwres.idrbcodl
            aCbsres.codtcobco = aCbwres.codtcobco
            aCbsres.estadobco = aCbwres.estadobco
            aCbsres.idrerpdl = aCbwres.idrerpdl
            aCbsres.codtcoerp = aCbwres.codtcoerp
            aCbsres.estadoerp = aCbwres.estadoerp
            aCbsres.save()
            aCbwres.delete()
        tiposDeConciliacion = json.loads(getTiposDeConciliacion(request,idrenc).content)
        for idsres in tiposDeConciliacion["listado"]:
            dato = tiposDeConciliacion[str(idsres)]
            try:
                Cbsresc.objects.filter(idsres=idsres).delete()
            except:
                pass
            if dato[0] != "":
                aCbsresc = Cbsresc(idsres=idsres, codtco=dato[0], debebco=dato[4],
                                haberbco=dato[5], saldoacumesbco=dato[6], saldoacumeserp=dato[7])
                aCbsresc.save()
            if dato[1] != "":
                aCbsresc = Cbsresc(idsres=idsres, codtco=dato[1], debeerp=dato[2],
                                habererp=dato[3], saldoacumesbco=dato[6], saldoacumeserp=dato[7])
                aCbsresc.save()
        aCbsres = Cbsres.objects.filter(
                idrenc=idrenc).order_by('-idsres').first()
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenc).first()
        aCbrenc.saldobco = tiposDeConciliacion["saldobcototal"]
        aCbrenc.saldoerp = tiposDeConciliacion["saldoerptotal"]
        aCbrenc.difbcoerp = tiposDeConciliacion["saldodiferenciatotal"]
        aCbrenc.save()
        try:
            ultimoDebeErp = aCbsres.debeerp
            if ultimoDebeErp is None:
                ultimoDebeErp = 0
            ultimoHaberErp = aCbsres.habererp
            if ultimoHaberErp is None:
                ultimoHaberErp = 0

            aCbrencl = Cbrencl(
                idrenc=Cbrenc.objects.filter(idrenc=idrenc).first(),
                status=1,
                saldobco=Cbrenc.objects.filter(idrenc=idrenc).first().saldobco,
                saldoerp=aCbsres.saldoacumeserp+ultimoDebeErp-ultimoHaberErp,
                difbcoerp=Cbrenc.objects.filter(idrenc=idrenc).first(
                ).saldobco - aCbsres.saldoacumeserp+ultimoDebeErp-ultimoHaberErp,
                idusu=request.user.username)
            aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)
            anteriorCbrencl = Cbrencl.objects.filter(idrenc=aCbrencl.idrenc).last()
            if aCbrencl.status != anteriorCbrencl.status or aCbrencl.difbcoerp != anteriorCbrencl.difbcoerp or aCbrencl.saldobco != anteriorCbrencl.saldobco:
                aCbrencl.save(aCbrencl)
        except Exception as e:
            print(e)
            pass
    

def conservarGuardado(request):
    idrenca = request.GET['idrenc']
    guardado(idrenca, request)
    aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
    if Cbsres.objects.filter(idrenc=idrenca, idrbcodl=0).exists() or Cbsres.objects.filter(idrenc=idrenca, idrerpdl=0).exists() or Cbsres.objects.filter(idrenc=idrenca, idrbcodl=None).exists() or Cbsres.objects.filter(idrenc=idrenca, idrerpdl=None).exists() or Cbsres.objects.filter(idrenc=idrenca).exists() == False:
        aCbrenc.estado = 1
        aCbrenc.save()
        return redirect("../../cbsres/?idrenc="+idrenca)
    else:
        aCbrenc.estado = 2
        aCbrenc.save()
        return redirect("../../")
    


def eliminarCarga(request):
    aCbrenc = Cbrenc.objects.order_by('-idrenc').first()
    idrenc = aCbrenc.idrenc
    idrbcoe = Cbrbcoe.objects.filter(
        idrenc=idrenc).first()
    if idrbcoe is not None:
        idrbcoe=idrbcoe.idrbcoe
    idrerpe = Cbrerpe.objects.filter(
        idrenc=idrenc).first()
    if idrerpe is not None:
        idrerpe=idrerpe.idrerpe
    Cbrbod.objects.filter(idrenc=idrenc).delete()
    Cbrgal.objects.filter(idrenc=idrenc).delete()
    Cbrbcod.objects.filter(idrbcoe=idrbcoe).delete()
    Cbrerpd.objects.filter(idrerpe=idrerpe).delete()
    Cbrbcoe.objects.filter(idrenc=idrenc).delete()
    Cbrerpe.objects.filter(idrenc=idrenc).delete()
    Cbrencl.objects.filter(idrenc=idrenc).delete()
    Cbrenct.objects.filter(idrenc=idrenc).delete()
    Cbrenc.objects.filter(idrenc=idrenc).delete()
    return redirect("../../")

def verificarCarga(request):
    aCbrenc = Cbrenc.objects.order_by('-idrenc').first()
    idrenc = aCbrenc.idrenc
    ano = aCbrenc.ano
    mes = aCbrenc.mes
    nrocta = aCbrenc.nrocta
    empresa = aCbrenc.empresa
    codbco = aCbrenc.codbco
    # verifica que el registro anterior sea del mes y ao correspondiente(o del siguiente a cbttca)
    if mes == 1:
        mesanterior = 12
        anoanterior = int(ano)-1
    else:
        mesanterior = int(mes) - 1
        anoanterior = int(ano)
    aCberencAnterior = Cbrenc.objects.filter(codbco=codbco,
                                             nrocta=nrocta,
                                             ano=anoanterior,
                                             mes=mesanterior,
                                             #  cliente=cliente,
                                             empresa=empresa,
                                             ).first()
    aCbtcta = Cbtcta.objects.filter(
            codbco=codbco, nrocta=nrocta, empresa=empresa).first()
    if aCberencAnterior == None:

        saldobcoanterior = aCbtcta.saldoinibco
        saldoerpanterior = aCbtcta.saldoinierp
    else:
        saldobcoanterior = aCberencAnterior.saldobco
        saldoerpanterior = aCberencAnterior.saldoerp
    aCbrbcoe = Cbrbcoe.objects.get(idrenc=idrenc)
    aCbrerpe = Cbrerpe.objects.get(idrenc=idrenc)
    primerRegistroBco = Cbrbcod.objects.filter(
        idrbcoe=aCbrbcoe.idrbcoe).order_by("idrbcod").order_by("fechatra").first()
    saldobco = primerRegistroBco.saldo + \
        primerRegistroBco.debe - primerRegistroBco.haber
    primerRegistroErp = Cbrerpd.objects.filter(
        idrerpe=aCbrerpe.idrerpe).order_by("idrerpd").order_by("fechatra").first()
    saldoerp = primerRegistroErp.saldo - \
        primerRegistroErp.debe + primerRegistroErp.haber
    if saldoerp == saldoerpanterior and saldobco == saldobcoanterior:
        return redirect("../../")
    errorBco = False
    errorERP = False
    if saldoerp != saldoerpanterior:
        errorERP = True
    if saldobco != saldobcoanterior:
        errorBco = True
    moneda = aCbtcta.monbasebco
    saldoerp =  moneda+'{:,}'.format(float(saldoerp))
    saldobco =  moneda+'{:,}'.format(float(saldobco))
    saldoerpanterior =  moneda+'{:,}'.format(float(saldoerpanterior))
    saldobcoanterior =  moneda+'{:,}'.format(float(saldobcoanterior))
    return render(request, "cbrenc/confirmarcarga.html", {"saldobcoanterior": saldobcoanterior,  "saldoerpanterior": saldoerpanterior, "saldobco": saldobco, "saldoerp": saldoerp, "errorBco": errorBco, "errorERP": errorERP})

def verificarGuardado(request):
    return render(request, "cbrenc/confirmation-form.html")


def createCbrenct(request, idrenc, accion, formulario):
        cerrarCbrenct(request)
        aCbrenct = Cbrenct(
                    formulario=formulario, idrenc=Cbrenc.objects.filter(idrenc=idrenc).first())
        aCbrenct.idusu = request.user.username
        aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
        aCbrenct.accion = accion
        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
        aCbrenct.save()

def cerrarCbrenct(request):
        if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
            bCbrenct = Cbrenct.objects.filter(
                        idusu=request.user.username, fechorafin=None).first()
            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
            bCbrenct.save()

def getContext(request, context, titulo, formulario):

    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbtcli = Cbtcli.objects.filter(cliente=aCbtusu.cliente).first()
    context["cliente"] = aCbtcli.cliente + "-" + aCbtcli.descli
    context["clientepuro"] = aCbtcli.cliente
    context['title'] = titulo
    context['codigo'] = formulario
    context['return_url'] = reverse_lazy('CBR:cbrenc-list')
    context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
    context['account_url'] = reverse_lazy('CBR:cbtcta-list')
    context['list_url'] = reverse_lazy('CBR:cbrenc-list')
    context['list_cbtcta_url'] = reverse_lazy('CBR:cbtcta-list')
    context['list_cbtusu_url'] = reverse_lazy('CBR:cbtusu-list')
    context['usuarios_url'] = reverse_lazy('CBR:cbtusu-list')
    context['empresas_url'] = reverse_lazy('CBR:cbtemp-list')
    context['bancos_url'] = reverse_lazy('CBR:cbtbco-list')
    context['usuario_empresas_url'] = reverse_lazy('CBR:cbtusue-list')
    context['new_empresa_url'] = reverse_lazy('CBR:empresa-nueva')
    context['create_account_url'] = reverse_lazy('CBR:cbtcta_nueva_cuenta')
    context['new_user_url'] = reverse_lazy('CBR:usuario-nuevo')
    context['new_banco_url'] = reverse_lazy('CBR:banco-nuevo')
    context['sesiones_url'] = reverse_lazy('CBR:visualizacion_usuarios')
    context['idrenc'] = request.GET.get('idrenc')
    context['conciliacion_semiautomatica'] = reverse_lazy('CBR:conciliacion_semiautomatica')
    context["erppordefecto"] = aCbtcli.codhomerp
    if aCbtusu.tipousu == "S":
        context['superusuario'] = True
        context['idusu1'] = aCbtusu.idusu1



def calcularTotales(request, context):
        n = 0
        indtco_erp = ""
        moneda = context["moneda"]
        for i in Cbttco.objects.filter(indtco="1").order_by('codtco'):
            if n > 0:
                indtco_erp = indtco_erp + ","
            indtco_erp = indtco_erp + i.codtco
            n = n+1
        context['indtco_erp'] = indtco_erp
        indtco_bco = ""
        n = 0
        n = 0
        for i in Cbttco.objects.filter(indtco="2").order_by('codtco'):
            if n > 0:
                indtco_bco = indtco_bco + ","
            indtco_bco = indtco_bco + i.codtco
            n = n+1
        alertaa = ""
        n = 0
        for i in Cbttco.objects.filter(indtco="1").order_by('codtco'):
            if n > 0:
                alertaa = alertaa + "\\n"
            alertaa = alertaa + i.codtco + " : " + i.destco
            n = n+1
        context['alertaa'] = alertaa
        alertab = ""
        n = 0
        for i in Cbttco.objects.filter(indtco="2").order_by('codtco'):
            if n > 0:
                alertab = alertab + "\\n"
            alertab = alertab + i.codtco + " : " + i.destco
            n = n+1
        context['alertab'] = alertab
        alertac = ""
        n = 0
        for i in Cbttco.objects.filter().order_by('codtco'):
            if n > 0:
                alertac = alertac + "\\n"
            alertac = alertac + i.codtco + " : " + i.destco

            n = n+1
        context['alertac'] = alertac
        context['indtco_bco'] = indtco_bco
        debeerp = 0
        habererp = 0
        saldoerp = 0
        debebco = 0
        haberbco = 0
        saldobco = 0
        saldodiferencia = 0
        try:
            listado = Cbsres.objects.order_by("idsres").filter(
                idrenc=request.GET.get('idrenc'))
            for registro in listado:
                try:
                    debeerp = debeerp + registro.debeerp
                except:
                    pass
                try:
                    habererp = habererp + registro.habererp
                except:
                    pass
                try:
                    if registro.saldoerp is not None:
                        saldoerp = registro.saldoacumeserp
                except:
                    pass
                try:
                    debebco = debebco + registro.debebco
                except:
                    pass
                try:
                    haberbco = haberbco + registro.haberbco
                except:
                    pass
                try:
                    if registro.saldobco is not None:
                        saldobco = registro.saldoacumesbco
                except:
                    pass
                try:
                    if registro.saldodiferencia is not None:
                        saldodiferencia = registro.saldodiferencia
                except:
                    pass
        except Exception as e:
            print(e)

        tiposDeConciliacion = json.loads(
            getTiposDeConciliacion(request,request.GET.get('idrenc')).content)
        context['debebcototal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["debebcototal"]))
        context['haberbcototal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["haberbcototal"]))
        context['saldobcototal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["saldobcototal"]))
        context['debeerptotal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["debeerptotal"]))
        context['habererptotal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["habererptotal"]))
        context['saldoerptotal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["saldoerptotal"]))
        context['saldodiferenciatotal'] =  moneda + \
            '{:,}'.format(float(tiposDeConciliacion["saldodiferenciatotal"]))
        context['habererp'] =  moneda+'{:,}'.format(habererp)
        context['debeerp'] =  moneda+'{:,}'.format(debeerp)
        context['debebco'] =  moneda+'{:,}'.format(debebco)
        context['haberbco'] =  moneda+'{:,}'.format(haberbco)
        context['saldobco'] =  moneda+'{:,}'.format(saldobco)
        context['saldoerp'] =  moneda+'{:,}'.format(saldoerp)
        context['saldodiferencia'] =  moneda+'{:,}'.format(saldodiferencia)
        

def populateDatabase():
        if Cbtcli.objects.filter(cliente="pablo").exists() == False:
            aCbtcli = Cbtcli(cliente="pablo", descli="describo a pablo")
            aCbtcli.save()
        if Cbtcol.objects.filter(codcol=3).exists() == False:
            aCbtcol = Cbtcol(codcol=0, descol="IDSRES ", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=1, descol="FECHA TRANSACCION BCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=2, descol="HORA TRANSACCION BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=3, descol="DEBE BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=4, descol="HABER BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=5, descol="SALDO ARCHIVO BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=6, descol="SALDO ACUMULADO BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=7, descol="SALDO AL DIA BCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=8, descol="OFICINA", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=9, descol="DESC TRANS", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=10, descol="REF TRANS", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=11, descol="COD TRANS", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=12, descol="IDRBCOD", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=13, descol="ESTADO BANCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=14, descol="COD CONCILIACION BCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=15, descol="LINK CONCILIADO ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=16, descol="ESTADO ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=17, descol="CODIGO CONCILIACION ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=18, descol="LINK CONCILIADO BCO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=19, descol="IDRERPD", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=20, descol="FECHA TRANSACCION ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=21, descol="DEBE ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=22, descol="HABER ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=23, descol="SALDO ARCHIVO ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=24, descol="SALDO ACUMULADO ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=25, descol="SALDO DIA ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=26, descol="DIFERENCIA SALDO", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=27, descol="NUM TRANS ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=28, descol="NUM COMPRO ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=29, descol="AUXILIAR ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=30, descol="REFERENCIA ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=31, descol="GLOSA ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=32, descol="FECHA CONTA ERP", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol=33, descol="HISTORIAL", inddef=1)
            aCbtcol.save()

        if Cbttco.objects.filter(codtco="DPTR").exists() == False:
            aCbttco = Cbttco(
                1, 1, "DPTR", "Depositos en Transito (+)", 0, 1, "H", 1)
            aCbttco.save()
            aCbttco = Cbttco(2, 2, "CERR", "Cargos Erroneos", 0, 2, "D", 0)
            aCbttco.save()
            aCbttco = Cbttco(
                3, 2, "CHNC", "Cheques no Contabilizados (-)", 0, 2, "H", 1)
            aCbttco.save()
            aCbttco = Cbttco(
                4, 2, "NDNC", "Notas de Debito no C (-)", 0, 2, "H", 1)
            aCbttco.save()
            aCbttco = Cbttco(
                5, 2, "NCNC", "Notas de Credito no C(+)", 0, 2, "D", 1)
            aCbttco.save()
            aCbttco = Cbttco(
                6, 2, "DNC", "Deposito no Contabilizado (+)", 0, 2, "D", 1)
            aCbttco.save()
            aCbttco = Cbttco(
                7, 1, "NDTR", "Notas de Debito en T (-)", 0, 1, "D", 1)
            aCbttco.save()
            aCbttco = Cbttco(
                8, 1, "NCTR", "Notas de Credito en T (+)", 0, 1, "H", 1)
            aCbttco.save()
            aCbttco = Cbttco(9, 2, "AERR", "Abonos Erroneos", 0, 2, "H", 0)
            aCbttco.save()
        if Cbterr.objects.filter(coderr=99).exists() == False:
            aCbterr = Cbterr(coderr=1, descerr="Día Fuera de Calendario")
            aCbterr.save()
            aCbterr = Cbterr(coderr=2, descerr="Sin Código de Oficina")
            aCbterr.save()
            aCbterr = Cbterr(coderr=3, descerr="Debe Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr=4, descerr="Haber Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr=5, descerr="Saldo Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr=99, descerr="Error Desconocido")
            aCbterr.save()
        if Cbterr.objects.filter(coderr=6).exists() == False:
            aCbterr = Cbterr(coderr=6, descerr="Incumple Logica de aplicación")
            aCbterr.save()

def posibilidadDeConciliar(request):
    data = {}
    idrenc = request.POST.get("idrenc")
    usuario = request.user.username
    data["posible"] = "si"
    if Cbwres.objects.filter(idrenc=idrenc).exists():
        if Cbwres.objects.filter(idrenc=idrenc).first().idusu != usuario:
            data["posible"] = "no"
    

    return JsonResponse(data)

def updateCbtusuc(request):
    codcol = request.POST["codcol"]
    checked = request.POST["checked"]
    if checked == "false":
        Cbtusuc.objects.filter(idusu=request.user.username, codcol=codcol).delete()
    else:
        aCbtusuc = Cbtusuc(idusu=request.user.username, codcol=codcol)
        aCbtusuc.fechact = dt.datetime.now(tz=timezone.utc)
        aCbtusuc.idusu = request.user.username
        aCbtusuc.save()
    return JsonResponse({})

class Object(object):
    pass

def cbrencDesconciliar(request):
    aCbrenc = Cbrenc.objects.get(idrenc= request.POST.get("idrenc"))
    if Cbrenc.objects.exclude(estado=3).filter(cliente=aCbrenc.cliente, codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta, idrenc__gt = aCbrenc.idrenc).exists():
        data = {}
        data["info"] = "No es posible desconciliar"
        return JsonResponse(data)
    
    aCbrenc.estado = 1
    aCbrenc.save()
    return HttpResponse("")

def CbtcfgCreate(request):
    cliente = clienteYEmpresas(request)["cliente"]
    ordencfg= Cbtcfg.objects.filter(cliente=cliente).count()-1
    aCbtcfg = Cbtcfg(cliente=cliente, codcfg=3,actpas="P", fechact=dt.datetime.now(), idusu=request.user.username)
    aCbtcfg.save()
    Cbtcfgc(idtcfg=aCbtcfg, campobco="", campoerp="", ordencfg=ordencfg, fechact=dt.datetime.now(), idusu=request.user.username).save()
    return HttpResponse("")


def chequearUsuarioConectado(request):
    data = {}
    try:
        aCbtusu = Cbtusu.objects.filter(idtusu=request.POST["idtusu"]).first()
        if Cbsusu.objects.filter(idusu1=aCbtusu.idusu1, finlogin__isnull=True).exists():
            data['enuso']=True
        else:
            data['enuso']=False
    except Exception as e:
        data['enuso']=False
        print(e)
    return JsonResponse(data)

def userCheck(request):
    data = {}
    data["cerrar"]= False
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    if aCbtusu == None:
        data["cerrar"]= True
    elif aCbtusu.actpas != "A":
        data["cerrar"]= True
    aCbtlic = Cbtlic.objects.filter(cliente=clienteYEmpresas(request)["cliente"]).first()
    if aCbtlic.fechalic < dt.datetime.now(tz=timezone.utc):
        data["cerrar"]= True
    return JsonResponse(data)

def cierreDeEmergencia(request):
    return render(request, "utils/cierredeemergencia.html")

def updateCbtcfg(request):
    if request.POST['fila'][0:9] == 'optionbco':
        aCbtcfgc = Cbtcfgc.objects.filter(idtcfg=request.POST['fila'][10:]).first()
        aCbtcfgc.campobco = request.POST['value']
        aCbtcfgc.save()
    elif request.POST['fila'][0:9] == 'optionerp':
        aCbtcfgc = Cbtcfgc.objects.filter(idtcfg=request.POST['fila'][10:]).first()
        aCbtcfgc.campoerp = request.POST['value']
        aCbtcfgc.save()
    elif request.POST['fila'][0:6]=="actpas":
        aCbtcfg = Cbtcfg.objects.filter(idtcfg=request.POST['fila'][7:]).first()
        if request.POST['checked'] == 'true':
            aCbtcfg.actpas = "A"
        else:
            aCbtcfg.actpas = "P"
        aCbtcfg.save()
    elif request.POST['fila'][0:8]=="ordencfg":
        aCbtcfgc = Cbtcfgc.objects.filter(idtcfg=request.POST['fila'][9:]).first()
        aCbtcfgc.ordencfg = int(request.POST['value'])
        aCbtcfgc.save()

    return HttpResponse("")

@csrf_exempt
def conciliarSaldosExistentes(request):
    chequearNoDobleConexion(request)
    try:
        idrenc = request.POST.get('idrenc')
        aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
        conciliacioAutoySemiAuto(request,idrenc, aCbrenc)
    except Exception as e:
        print(e)
    return JsonResponse({})

def enviarMailLadoBancoHtml(request):
    data={}
    try:
        idrenc = request.POST.get("idrenc")
        send_to, context = CreateContextNoConciliadosBancoHtml(request, idrenc)
        content = render_to_string('utils/paradescargarbanco.html', context)
        with open(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginabanco.html", 'w', encoding='utf-8') as f:
            f.write(content)
        send_mail(send_to, "banco", [str(Path(__file__).resolve().parent.parent) + "/media/temp/paginabanco.html"])
        data["info"]="Lado Banco de No conciliados del Idrenc " + idrenc + " enviado correctamente en formato HTML"
    except Exception as e:
        print(e)
        data["info"]="Envio Fallido"

    return JsonResponse(data)

def CreateContextNoConciliadosBancoHtml(request, idrenc):
    aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
    aCbtcta = Cbtcta.objects.get(nrocta = aCbrenc.nrocta)
    send_to = aCbtcta.diremail
    context = {}
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbtcli = Cbtcli.objects.get(cliente=aCbtusu.cliente)
        
    aCbtemp = Cbtemp.objects.get(empresa=aCbrenc.empresa)
    aCbmbco = Cbmbco.objects.get(codbco = aCbrenc.codbco)
    context["descli"]=aCbtcli.descli
    context["fechaDeEmision"] =str(dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
    context["desemp"] = aCbtemp.desemp
    context["desbco"] = aCbmbco.desbco
    context["cuenta"] = aCbtcta.nrocta
    context["descta"] = aCbtcta.descta
    context["ano"] = aCbrenc.ano
    context["mes"] = aCbrenc.mes
    context["tabla"] = 'tableFixHead'
    row = "odd"
    allCbsres = Cbsres.objects.filter(idrenc=idrenc, estadobco=0, fechatrabco__isnull=False).all()
    context["pagina"] = 1
    registros = []
    for aCbsres in allCbsres:
        datos = {}
        datos["class"]=row
        datos["fecha"]= aCbsres.fechatrabco.strftime('%d/%m/%Y')
        datos["hora"]=aCbsres.horatrabco.strftime('%H:%M:%S')
        datos["oficina"]=aCbsres.oficina
        datos["descripcion"]=aCbsres.desctra
        datos["referencia"] = aCbsres.reftra
        datos["codigo"] = aCbsres.codtra
        datos["debe"] = '{:,.2f}'.format(aCbsres.debebco)
        datos["haber"] = '{:,.2f}'.format(aCbsres.haberbco)
        registros.append(datos)
        if row=="odd":
            row="even"
        else:
            row="odd"
    context["registros"] = registros
    return send_to,context

def enviarMailLadoBancoPdf(request):
    
    try:
        data, idrenc, send_to = crearPdfBanco(request)
        send_mail(send_to, "banco", [str(Path(__file__).resolve().parent.parent) + "/media/temp/ladobanco.pdf"])
        data["info"]="Lado Banco de No conciliados del Idrenc " + idrenc + " enviado correctamente en formato PDF"
    except Exception as e:
        print(e)
        data["info"]="Envio Fallido"

    return JsonResponse(data) 

def crearPdfBanco(request):
    data={}
    idrenc = request.POST.get("idrenc")
    if idrenc == None:
        idrenc = request.GET.get("idrenc")
    context = {}
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbtcli = Cbtcli.objects.get(cliente=aCbtusu.cliente)
    aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
    aCbtemp = Cbtemp.objects.get(empresa=aCbrenc.empresa)
    aCbmbco = Cbmbco.objects.get(codbco = aCbrenc.codbco)
    aCbtcta = Cbtcta.objects.get(nrocta = aCbrenc.nrocta)
    send_to = aCbtcta.diremail
    context["descli"]=aCbtcli.descli
    context["fechaDeEmision"] =str(dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
    context["desemp"] = aCbtemp.desemp
    context["desbco"] = aCbmbco.desbco
    context["cuenta"] = aCbtcta.nrocta
    context["descta"] = aCbtcta.descta
    context["ano"] = aCbrenc.ano
    context["mes"] = aCbrenc.mes
    row = "odd"
    pagina = 0
    allCbsres = Cbsres.objects.filter(idrenc=idrenc, estadobco=0, fechatrabco__isnull=False).all()
    primerRegistro = 0
    merger = PdfFileMerger()
    while primerRegistro < len(allCbsres):
        registros = []
        pagina = pagina +1
        context["pagina"] = pagina
        if primerRegistro+15 < len(allCbsres):
            ultimoRegistro = primerRegistro+15
        else:
            ultimoRegistro = len(allCbsres)
        for aCbsres in allCbsres[primerRegistro:ultimoRegistro]:
            datos = {}
            datos["class"]=row
            datos["fecha"]= aCbsres.fechatrabco.strftime('%d/%m/%Y')
            datos["hora"]=aCbsres.horatrabco.strftime('%H:%M:%S')
            datos["oficina"]=aCbsres.oficina
            datos["descripcion"]=aCbsres.desctra
            datos["referencia"] = aCbsres.reftra
            datos["codigo"] = aCbsres.codtra
            datos["debe"] = '{:,.2f}'.format(aCbsres.debebco)
            datos["haber"] = '{:,.2f}'.format(aCbsres.haberbco)
            registros.append(datos)
            if row=="odd":
                row="even"
            else:
                row="odd"
        context["registros"] = registros
        content = render_to_string('utils/paradescargarbanco.html', context)
        pdf = htmltopydf.generate_pdf(content)
        with open(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginabanco"+str(pagina)+".pdf", 'wb') as f:
            f.write(pdf)
        merger.append(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginabanco"+str(pagina)+".pdf", import_bookmarks=False )
        print(ultimoRegistro)
        primerRegistro = ultimoRegistro + 1
        print(ultimoRegistro)
    merger.write(str(Path(__file__).resolve().parent.parent) + "/media/temp/ladobanco.pdf")
    return data,idrenc,send_to 

def enviarMailLadoErpHtml(request):
    data={}
    try:
        idrenc = request.POST.get("idrenc")
        send_to, context = CreateContextNoConciliadosErpHtml(request, idrenc)
        content = render_to_string('utils/paradescargarerp.html', context)
        with open(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginaerp.html", 'w', encoding='utf-8') as f:
            f.write(content)
        send_mail(send_to, "banco", [str(Path(__file__).resolve().parent.parent) + "/media/temp/paginaerp.html"])
        data["info"]="Lado Erp de No conciliados del Idrenc " + idrenc + " enviado correctamente en formato HTML"
    except Exception as e:
        print(e)
        data["info"]="Envio Fallido"

    return JsonResponse(data)

def CreateContextNoConciliadosErpHtml(request, idrenc):
    context = {}
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbtcli = Cbtcli.objects.get(cliente=aCbtusu.cliente)
    aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
    aCbtemp = Cbtemp.objects.get(empresa=aCbrenc.empresa)
    aCbmbco = Cbmbco.objects.get(codbco = aCbrenc.codbco)
    aCbtcta = Cbtcta.objects.get(nrocta = aCbrenc.nrocta)
    send_to = aCbtcta.diremail
    context["descli"]=aCbtcli.descli
    context["fechaDeEmision"] =str(dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
    context["desemp"] = aCbtemp.desemp
    context["desbco"] = aCbmbco.desbco
    context["cuenta"] = aCbtcta.nrocta
    context["descta"] = aCbtcta.descta
    context["ano"] = aCbrenc.ano
    context["mes"] = aCbrenc.mes
    context["tabla"] = 'tableFixHead'
    row = "odd"
    allCbsres = Cbsres.objects.filter(idrenc=idrenc, estadoerp=0, fechatraerp__isnull=False).all()
    context["pagina"] = 1
    registros = []
    for aCbsres in allCbsres:
        datos = {}
        datos["class"]=row
        datos["fecha"]= aCbsres.fechatraerp.strftime('%d/%m/%Y')
        datos["comprobante"]=aCbsres.nrocomperp
        datos["auxiliar"]=aCbsres.auxerp
        datos["referencia"]=aCbsres.referp
        datos["glosa"] = aCbsres.glosaerp
        datos["debe"] = '{:,.2f}'.format(aCbsres.debeerp)
        datos["haber"] = '{:,.2f}'.format(aCbsres.habererp)
        registros.append(datos)
        if row=="odd":
            row="even"
        else:
            row="odd"
    context["registros"] = registros
    return send_to,context

def enviarMailLadoErpPdf(request):
    
    try:
        data, idrenc, send_to = crearPdferp(request)
        send_mail(send_to, "banco", [str(Path(__file__).resolve().parent.parent) + "/media/temp/ladoerp.pdf"])
        data["info"]="Lado ERP de No conciliados del Idrenc " + idrenc + " enviado correctamente en formato PDF"
    except Exception as e:
        print(e)
        data["info"]="Envio Fallido."

    return JsonResponse(data) 

def crearPdferp(request):
    data={}
    idrenc = request.POST.get("idrenc")
    if idrenc == None:
        idrenc = request.GET.get("idrenc")

    context = {}
    aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
    aCbtcli = Cbtcli.objects.get(cliente=aCbtusu.cliente)
    aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
    aCbtemp = Cbtemp.objects.get(empresa=aCbrenc.empresa)
    aCbmbco = Cbmbco.objects.get(codbco = aCbrenc.codbco)
    aCbtcta = Cbtcta.objects.get(nrocta = aCbrenc.nrocta)
    send_to = aCbtcta.diremail
    context["descli"]=aCbtcli.descli
    context["fechaDeEmision"] =str(dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
    context["desemp"] = aCbtemp.desemp
    context["desbco"] = aCbmbco.desbco
    context["cuenta"] = aCbtcta.nrocta
    context["descta"] = aCbtcta.descta
    context["ano"] = aCbrenc.ano
    context["mes"] = aCbrenc.mes
    row = "odd"
    pagina = 0
    allCbsres = Cbsres.objects.filter(idrenc=idrenc, estadoerp=0, fechatraerp__isnull=False).all()
    primerRegistro = 0
    merger = PdfFileMerger()
    while primerRegistro < len(allCbsres):
        registros = []
        pagina = pagina +1
        context["pagina"] = pagina
        if primerRegistro+15 < len(allCbsres):
            ultimoRegistro = primerRegistro+15
        else:
            ultimoRegistro = len(allCbsres)
        for aCbsres in allCbsres[primerRegistro:ultimoRegistro]:
            datos = {}
            datos["class"]=row
            datos["fecha"]= aCbsres.fechatraerp.strftime('%d/%m/%Y')
            datos["comprobante"]=aCbsres.nrocomperp
            datos["auxiliar"]=aCbsres.auxerp
            datos["referencia"]=aCbsres.referp
            datos["glosa"] = aCbsres.glosaerp
            datos["debe"] = '{:,.2f}'.format(aCbsres.debeerp)
            datos["haber"] = '{:,.2f}'.format(aCbsres.habererp)
            registros.append(datos)
            if row=="odd":
                row="even"
            else:
                row="odd"
        context["registros"] = registros
        content = render_to_string('utils/paradescargarerp.html', context)
        pdf = htmltopydf.generate_pdf(content)
        with open(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginaerp"+str(pagina)+".pdf", 'wb') as f:
            f.write(pdf)
        merger.append(str(Path(__file__).resolve().parent.parent) + "/media/temp/paginaerp"+str(pagina)+".pdf", import_bookmarks=False )
        print(ultimoRegistro)
        primerRegistro = ultimoRegistro + 1
        print(ultimoRegistro)
    merger.write(str(Path(__file__).resolve().parent.parent) + "/media/temp/ladoerp.pdf")
    return data,idrenc,send_to


def send_mail(send_to,lado, files=None):
    #assert isinstance(send_to, list)
    try:
        text = "Se envía el listado de registros no conciliados del " + lado
        msg = MIMEMultipart()
        print(config)
        msg['From'] = 'vadiasys.cb.noreply@gmail.com'
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Registros No Conciliados del " + lado

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
         # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)  
        smtp = smtplib.SMTP()
        smtp.connect('127.0.0.1')
        print("aqui")
        #smtp.starttls()
        #smtp.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
        print("b")
        smtp.sendmail('vadiasys.cb.noreply@gmail.com', send_to, msg.as_string())
        print("c")
        smtp.quit()
        smtp.close()
        print("d")
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

def getMailEmpresa(request):
    data = {}
    try:
        cliente = request.GET.get("cliente")
        print(cliente)
        empresa = request.GET.get('empresa')
        print(empresa)
        aCbtemp = Cbtemp.objects.filter(empresa=empresa, cliente=cliente).first()
        data["diremail"] = aCbtemp.diremail
        return JsonResponse(data)
    except Exception as e:
        print(e)
        data["diremail"] = "Error en mail"
        return JsonResponse(data)

    


