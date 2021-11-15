# EXPLICACION


#region imports
import datetime as dt
import json
from json.decoder import JSONDecodeError
import time
from typing import Union

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.aggregates import Max
from django.dispatch import receiver
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from CBR.models import (Cbmbco, Cbrbcod, Cbrbcoe, Cbrbod, Cbrenc, Cbrencl, Cbrenct, Cbrerpd, Cbrerpe, Cbrgal, Cbsres, Cbsresc, Cbsusu,
                        Cbtbco, Cbtcli, Cbtcol, Cbtcta, Cbtemp, Cbterr, Cbtlic, Cbtpai, Cbttco, Cbtusu,
                        Cbtusuc, Cbtusue, Cbwres)

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
        if request.POST.get("autocierre") != True:
            aCbsusu = Cbsusu.objects.filter(
                idusu1=request.user.username).order_by("corrusu").last()
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
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario).last()
    aCbsusu.finlogin = dt.datetime.now(tz=timezone.utc)
    aCbsusu.save()
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
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario).last()
    try:
        data["iniciodesesion"] = aCbsusu.iniciologin
        if aCbsusu.finlogin == None:
            data["yaconectado"] = True
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
        idusu1=request.user.username).order_by("corrusu").last()
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
            print(aUser)
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
        print("empieza")
        chequearNoDobleConexion(request)
        print("empieza2")
        try:
            idrenc = request.POST.get('idrenc')
            print(idrenc)
            try:
                estado = Cbrenc.objects.get(idrenc=idrenc).estado
            except:
                estado = 1
            if (int(estado) < 2):
                existe = Cbsres.objects.filter(idrenc=idrenc).count()
                sobreescribir = request.POST['sobreescribir']
                # Define si es posible conciliar(es primera vez, se acepto la sobreescritura y el estado no es conciliado ni eliminado)
                if ((sobreescribir == 'true') or (existe == 0)):
                    print("poraca")
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
                    print("poralla")
                    # Define los objetos a cargar y los saldos iniciales
                    aCbrencAnterior= Cbrenc.objects.filter(ano=anoanterior, mes=mesanterior, cliente=aCbrenc.cliente, empresa=aCbrenc.empresa, codbco=aCbrenc.codbco).first()
                    print(aCbrencAnterior)
                    if aCbrencAnterior is not None:
                        bcoDataSetAnterior =  Cbsres.objects.filter(estadobco=0, fechatrabco__isnull=False, idrenc=aCbrencAnterior.idrenc).order_by("-fechatrabco")
                    else:
                        bcoDataSetAnterior = []
                        print("alfa")
                    bcoDataSet = list(Cbrbcod.objects.filter(
                        idrbcoe=idrenc).order_by('fechatra', 'horatra'))
                    print("beta")
                    for element in bcoDataSetAnterior:
                        print("a")
                        if Cbttco.objects.filter(codtco=element.codtcobco, indtco=1, indpend=0).exists() == False:
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
                            aUnir.idrbcoe=Cbrbcoe.objects.filter(idrenc=element.idrenc).first()
                            print("b")
                            bcoDataSet.insert(0,aUnir)
                            print("c")
                    if aCbrencAnterior is not None:
                        erpDataSetAnterior = Cbsres.objects.filter(estadoerp=0, fechatraerp__isnull=False, idrenc=aCbrencAnterior.idrenc).order_by("-fechatraerp")
                    else:
                        erpDataSetAnterior = []
                    erpDataSet = list(Cbrerpd.objects.filter(
                        idrerpe=idrenc).order_by('fechatra'))
                    for element in erpDataSetAnterior:
                        if Cbttco.objects.filter(codtco=element.codtcoerp, indtco=2, indpend=0).exists()==False:
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
                            aUnir.idrerpe=Cbrerpe.objects.filter(idrenc=element.idrenc).first()
                            ##Completar con el resto de las cosas
                            erpDataSet.insert(0,aUnir)

                    rowInicialbco = Cbrbcod.objects.filter(
                        idrbcoe=idrenc).order_by('fechatra', 'horatra').first()

                    rowInicialerp = Cbrerpd.objects.filter(
                        idrerpe=idrenc).order_by('fechatra').first()

                    currentDay = rowInicialbco.fechatra
                    Cbsres.objects.filter(idrenc=idrenc).delete()
                    color = 0
                    cambio = False
                    
                    diaMenor = dt.datetime.date(dt.datetime.strptime("01/01/2030", "%d/%m/%Y"))
                    diaMayor = dt.datetime.date(dt.datetime.strptime("01/01/2010", "%d/%m/%Y"))
                    print("tiempo inicial")
                    print(time.time())
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
                    print("tiempo final")
                    print(time.time())
                    dia = diaMenor
                    while dia <= diaMayor:
                        # Para cada dia carga los registros del banco en orden, calculando los saldos
                        fechatrabco = None
                        for vwRow in bcoDataSet:
                            print(vwRow)
                            print(vwRow.fechatra)
                            if vwRow.fechatra == dia:
                                fechatrabco = vwRow.fechatra
                                if (vwRow.fechatra is None):
                                    if (currentDay != vwRow.fechatra):
                                        currentDay = vwRow.fechatra
                                print("esto")
                                print(idrenc)
                                print(Cbrenc.objects.get(
                                        idrenc=idrenc))
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
                                    codtcobco=" ",
                                    pautado=color
                                    # --------------------
                                )
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
                    n = 0
                    for aCbsres in Cbsres.objects.filter(idrenc=idrenc).order_by('idsres').all():
                        if n == 0:
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
                    while n < Cbsres.objects.filter(idrenc=idrenc).count():
                        aCbsres = Cbsres.objects.filter(
                            idrenc=idrenc).order_by('idsres')[n]
                        if Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco, debebco=aCbsres.debebco, haberbco=aCbsres.haberbco).count() == 1:
                            if Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco, debeerp=aCbsres.haberbco, habererp=aCbsres.debebco).count() == 1:
                                bCbsres = Cbsres.objects.filter(
                                    idrenc=idrenc, fechatrabco=aCbsres.fechatrabco, debeerp=aCbsres.haberbco, habererp=aCbsres.debebco).first()
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

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def Unir(vwRow, insCbsres, idrenc, color):
    # sistema que une el cbsres con banco cargado con un registro del cbrerpd

    insCbsres.idrerpd = vwRow.idrerpd

    insCbsres.saldoerp = vwRow.saldo

    # estado=vwRow.esta,
    # historial=vwRow.,
    # --------------------
    insCbsres.fechatraerp = vwRow.fechatra
    insCbsres.debeerp = vwRow.debe
    insCbsres.habererp = vwRow.haber
    insCbsres.codtcoerp = " "
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
    chequearNoDobleConexion(request)
    try:
        tabla = list(dict(request.POST).keys())[0][1:-1]
        while True:

            fila = tabla[:tabla.find("}")+1]
            comienzo = tabla[10:].find("{")

            fila = json.loads(fila)

            idsres = fila["idsres"]
            idrenc = float(fila["idrenc"])
            try:
                debeerp = float(fila["debeerp"])
            except:
                debeerp = None
            try:
                habererp = float(fila["habererp"])
            except:
                habererp = None
            try:
                saldoacumeserp = float(fila["saldoacumeserp"])
            except:
                saldoacumeserp = float(0)
            try:
                saldoacumdiaerp = float(fila["saldoacumdiaerp"])
            except:
                saldoacumdiaerp = float(0)
            saldodiferencia = float(fila["saldodiferencia"])
            historial = int(fila["historial"])
            try:
                idrbcodl = int(fila["idrbcodl"])
            except:
                idrbcodl = int(0)
            try:
                idrerpdl = int(fila["idrerpdl"])
            except:
                idrerpdl = int(0)
            codtcobco = fila["codtcobco"]
            codtcoerp = fila["codtcoerp"]
            idrenc = Cbrenc.objects.filter(idrenc=idrenc).first()
            if Cbwres.objects.filter(idsres=int(idsres)).exists():
                aCbsres = Cbwres.objects.filter(idsres=int(idsres)).first()
            else:
                aCbsres = Cbsres.objects.filter(idsres=int(idsres)).first()
            estadobco = fila["estadobco"]
            estadoerp = fila["estadoerp"]
            cliente = aCbsres.cliente
            empresa = aCbsres.empresa
            codbco = aCbsres.codbco
            nrocta = aCbsres.nrocta
            ano = aCbsres.ano
            mes = aCbsres.mes
            fechatrabco = aCbsres.fechatrabco
            horatrabco = aCbsres.horatrabco
            pautado = aCbsres.pautado
            debebco = aCbsres.debebco
            haberbco = aCbsres.haberbco
            saldobco = aCbsres.saldobco
            saldoacumesbco = aCbsres.saldoacumesbco
            saldoacumdiabco = aCbsres.saldoacumdiabco
            oficina = aCbsres.oficina
            desctra = aCbsres.desctra
            reftra = aCbsres.reftra
            codtra = aCbsres.codtra
            idrbcod = aCbsres.idrbcod
            nrotraerp = aCbsres.nrotraerp
            fechatraerp = aCbsres.fechatraerp
            nrocomperp = aCbsres.nrocomperp
            auxerp = aCbsres.auxerp
            referp = aCbsres.referp
            glosaerp = aCbsres.glosaerp
            saldoerp = aCbsres.saldoerp
            fechaconerp = aCbsres.fechaconerp
            idrerpd = aCbsres.idrerpd
            idusu = request.user.username
            Cbwres.objects.filter(idsres=idsres).delete()
            aCbwres = Cbwres(idrbcodl=idrbcodl, idrerpdl=idrerpdl, idsres=idsres, idrenc=idrenc, cliente=cliente, empresa=empresa, codbco=codbco, nrocta=nrocta, ano=ano, mes=mes, fechatrabco=fechatrabco, horatrabco=horatrabco, debebco=debebco, haberbco=haberbco, saldobco=saldobco, saldoacumesbco=saldoacumesbco, saldoacumdiabco=saldoacumdiabco, oficina=oficina, desctra=desctra, reftra=reftra, codtra=codtra, idrbcod=idrbcod,
                             nrotraerp=nrotraerp, fechatraerp=fechatraerp, nrocomperp=nrocomperp, auxerp=auxerp, referp=referp, glosaerp=glosaerp, debeerp=debeerp, habererp=habererp, saldoerp=saldoerp, saldoacumeserp=saldoacumeserp, saldoacumdiaerp=saldoacumdiaerp, fechaconerp=fechaconerp, idrerpd=idrerpd, saldodiferencia=saldodiferencia, estadobco=estadobco, estadoerp=estadoerp, historial=historial, codtcobco=codtcobco, codtcoerp=codtcoerp, idusu=idusu)
            aCbwres.save()
            if comienzo == -1:
                break
            tabla = tabla[comienzo+10:]
        return HttpResponse("")
    except Exception as e:
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

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def getanomes(request):
    chequearNoDobleConexion(request)
    empresa = request.GET.get('empresa')
    codbco = request.GET.get('banco')
    nrocta = request.GET.get('cuenta')
    try:
        maxAno = Cbrenc.objects.exclude(estado="3").filter(empresa=empresa,
            codbco=codbco, nrocta=nrocta).aggregate(Max('ano'))
        maxAno = maxAno['ano__max']
        if maxAno is None:
            aCbtcta = Cbtcta.objects.filter(empresa=empresa,
                codbco=codbco, nrocta=nrocta).first()
            if aCbtcta is None:
                data = {'ano': 0, 'mes': 0}
            maxAno = aCbtcta.ano
            maxMes = aCbtcta.mes
            if maxMes < 12:
                data = {'ano': maxAno, 'mes': maxMes + 1}
            else:
                data = {'ano': maxAno + 1, 'mes': 1}
        else:
            maxMes = Cbrenc.objects.exclude(estado="3").filter(empresa=empresa, codbco=codbco, nrocta=nrocta, ano=maxAno).aggregate(
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
    print(empresa)
    print(codbco)
    for cuenta in Cbtcta.objects.filter(empresa=empresa, codbco=codbco, cliente=clienteYEmpresas(request)["cliente"]).order_by("nrocta"):
        print("se agrego")
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
        print(codbco)
        algo = Cbmbco.objects.filter(codbco=codbco).first()
        print(algo)
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
                if (aCbrerpd.debe != registro.debeerp or aCbrerpd.haber != registro.habererp) and (registro.codtcoerp == " " or registro.codtcoerp == None):
                    data = {
                        "guardado": "Explique la modificacion en IDSRES =" + str(registro.idsres)}
    return JsonResponse(data)


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


@login_required
def getTiposDeConciliacion(request):
    chequearNoDobleConexion(request)
    idrenc = request.GET["idrenc"]
    data = {"debebcototal": 0, "haberbcototal": 0, "saldobcototal": 0, "debeerptotal": 0,
            "habererptotal": 0, "saldoerptotal": 0, "saldodiferenciatotal": 0}
    yaTomadas = []
    n = 0
    m = 0
    # calcula que codigos suman a cada lado
    listadoSumaDebeBco = []
    listadoSumaHaberBco = []
    listadoSumaDebeErp = []
    listadoSumaHaberErp = []
    for tipo in Cbttco.objects.all():
        if tipo.indsuma == 1:
            if tipo.erpbco == 1:
                if tipo.inddebhab == "H":
                    listadoSumaDebeBco.append(tipo.codtco)
                elif tipo.inddebhab == "D":
                    listadoSumaHaberBco.append(tipo.codtco)
            elif tipo.erpbco == 2:
                if tipo.inddebhab == "H":
                    listadoSumaDebeErp.append(tipo.codtco)
                elif tipo.inddebhab == "D":
                    listadoSumaHaberErp.append(tipo.codtco)
    saldoextrabco = 0
    saldoextraerp = 0
    # Listado de quienes tienen codigo para la tabla de respectiva
    data["listado"] = []

    # calcula primero las del cbwres y si no existen las del cbsres

    for registro in Cbsres.objects.filter(idrenc=idrenc).order_by("idsres").all():
        if Cbwres.objects.filter(idsres=registro.idsres).exists():
            registroAnalizado = Cbwres.objects.filter(
                idsres=registro.idsres).first()
        else:
            registroAnalizado = registro

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
        try:
            if data["saldobcototal"] is not None:
                data["saldobcototal"] = registroAnalizado.saldoacumesbco
        except:
            pass
        try:
            if data["saldoerptotal"] is not None:
                data["saldoerptotal"] = registroAnalizado.saldoacumeserp
        except:
            pass
        if registroAnalizado.codtcobco in listadoSumaDebeErp:
            try:
                data["debeerptotal"] = registroAnalizado.haberbco + \
                    data["debeerptotal"]
                data[str(registroAnalizado.idsres)] = [registroAnalizado.codtcobco, "", 0, 0,
                                                       registroAnalizado.haberbco, 0, registroAnalizado.saldoacumesbco, registroAnalizado.saldoacumeserp]
                data["listado"].append(registroAnalizado.idsres)
                saldoextraerp = saldoextraerp + registroAnalizado.haberbco
            except Exception as e:
                pass
        elif registroAnalizado.codtcobco in listadoSumaHaberErp:
            try:
                data["habererptotal"] = registroAnalizado.debebco + \
                    data["habererptotal"]
                data["listado"].append(registroAnalizado.idsres)
                data[str(registroAnalizado.idsres)] = [registroAnalizado.codtcobco, "", 0, 0, 0,
                                                       registroAnalizado.debebco, registroAnalizado.saldoacumesbco, registroAnalizado.saldoacumeserp]
                saldoextraerp = saldoextraerp - registroAnalizado.debebco
            except Exception as e:
                pass
        if registroAnalizado.codtcoerp in listadoSumaDebeBco:
            try:
                data["debebcototal"] = registroAnalizado.habererp + \
                    data["debebcototal"]
                data["listado"].append(registroAnalizado.idsres)
                try:
                    data[str(registroAnalizado.idsres)
                         ][1] = registroAnalizado.codtcoerp
                    data[str(registroAnalizado.idsres)
                         ][2] = registroAnalizado.habererp
                    data[str(registroAnalizado.idsres)
                         ][6] = registroAnalizado.saldoacumesbco
                    data[str(registroAnalizado.idsres)
                         ][7] = registroAnalizado.saldoacumeserp
                except:
                    data[str(registroAnalizado.idsres)] = ["", registroAnalizado.codtcoerp, registroAnalizado.habererp,
                                                           0, 0, 0, registroAnalizado.saldoacumesbco, registroAnalizado.saldoacumeserp]
                saldoextrabco = saldoextrabco + registroAnalizado.habererp
            except:
                pass
        elif registroAnalizado.codtcoerp in listadoSumaHaberBco:
            try:
                data["haberbcototal"] = registroAnalizado.debeerp + \
                    data["haberbcototal"]
                data["listado"].append(registroAnalizado.idsres)
                try:
                    data[str(registroAnalizado.idsres)
                         ][1] = registroAnalizado.codtcoerp
                    data[str(registroAnalizado.idsres)
                         ][3] = registroAnalizado.debeerp
                    data[str(registroAnalizado.idsres)
                         ][6] = registroAnalizado.saldoacumesbco
                    data[str(registroAnalizado.idsres)
                         ][7] = registroAnalizado.saldoacumeserp
                except:
                    data[str(registroAnalizado.idsres)] = ["", registroAnalizado.codtcoerp, 0, registroAnalizado.debeerp,
                                                           0, 0, registroAnalizado.saldoacumesbco, registroAnalizado.saldoacumeserp]
                saldoextrabco = saldoextrabco + registroAnalizado.debeerp
            except Exception as e:
                pass
    data["saldobcototal"] = data["saldobcototal"] + saldoextrabco
    data["saldoerptotal"] = data["saldoerptotal"] + saldoextraerp
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

def conservarGuardado(request):
    idrenca = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu=request.user.username, fechorafin=None).exists():
        bCbrenct = Cbrenct.objects.filter(
            idusu=request.user.username, fechorafin=None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario="CBF02",
                       idrenc=Cbrenc.objects.filter(idrenc=idrenca).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)
    aCbrenct.accion = 4
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)
    aCbrenct.save()

    while Cbwres.objects.filter(idrenc=idrenca).exists():
        idsres = Cbwres.objects.filter(idrenc=idrenca).first().idsres
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
    tiposDeConciliacion = json.loads(getTiposDeConciliacion(request).content)

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
    try:
        aCbsres = Cbsres.objects.filter(
            idrenc=idrenca).order_by('-idsres').first()
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
        aCbrenc.saldobco = tiposDeConciliacion["saldobcototal"]
        aCbrenc.saldoerp = tiposDeConciliacion["saldoerptotal"]
        aCbrenc.difbcoerp = tiposDeConciliacion["saldodiferenciatotal"]
        aCbrenc.save()
        ultimoDebeErp = aCbsres.debeerp
        if ultimoDebeErp is None:
            ultimoDebeErp = 0
        ultimoHaberErp = aCbsres.habererp
        if ultimoHaberErp is None:
            ultimoHaberErp = 0

        aCbrencl = Cbrencl(
            idrenc=Cbrenc.objects.filter(idrenc=idrenca).first(),
            status=1,
            saldobco=Cbrenc.objects.filter(idrenc=idrenca).first().saldobco,
            saldoerp=aCbsres.saldoacumeserp+ultimoDebeErp-ultimoHaberErp,
            difbcoerp=Cbrenc.objects.filter(idrenc=idrenca).first(
            ).saldobco - aCbsres.saldoacumeserp+ultimoDebeErp-ultimoHaberErp,
            idusu=request.user.username)
        aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)
        anteriorCbrencl = Cbrencl.objects.filter(idrenc=aCbrencl.idrenc).last()
        if aCbrencl.status != anteriorCbrencl.status or aCbrencl.difbcoerp != anteriorCbrencl.difbcoerp or aCbrencl.saldobco != anteriorCbrencl.saldobco:
            aCbrencl.save(aCbrencl)
        if Cbsres.objects.filter(idrenc=idrenca, idrbcodl=0).exists() or Cbsres.objects.filter(idrenc=idrenca, idrerpdl=0).exists() or Cbsres.objects.filter(idrenc=idrenca, idrbcodl=None).exists() or Cbsres.objects.filter(idrenc=idrenca, idrerpdl=None).exists() or Cbsres.objects.filter(idrenc=idrenca).exists() == False:
            aCbrenc.estado = 1
            aCbrenc.save()
            return redirect("../../cbsres/?idrenc="+idrenca)
        else:
            aCbrenc.estado = 2
            aCbrenc.save()
            return redirect("../../")
    except Exception as e:
        print(e)
        pass
    return redirect("../../cbsres/?idrenc="+idrenca)

def eliminarCarga(request):
    aCbrenc = Cbrenc.objects.order_by('-idrenc').first()
    idrenc = aCbrenc.idrenc
    Cbrbod.objects.filter(idrenc=idrenc).delete()
    Cbrgal.objects.filter(idrenc=idrenc).delete()
    Cbrbcod.objects.filter(idrbcoe=idrenc).delete()
    Cbrerpd.objects.filter(idrerpe=idrenc).delete()
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
    # verifica que el registro anterior sea del mes y año correspondiente(o del siguiente a cbttca)
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
                                             # cliente=cliente,
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
    primerRegistroBco = Cbrbcod.objects.filter(
        idrbcoe=idrenc).order_by("idrbcod").order_by("fechatra").first()
    saldobco = primerRegistroBco.saldo + \
        primerRegistroBco.debe - primerRegistroBco.haber
    primerRegistroErp = Cbrerpd.objects.filter(
        idrerpe=idrenc).order_by("idrerpd").order_by("fechatra").first()
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

    if aCbtusu.tipousu == "S":
        context['superusuario'] = True



def calcularTotales(request, context):
        n = 0
        indtco_erp = ""
        moneda = context["moneda"]
        for i in Cbttco.objects.filter(indtco="1").all():
            if n > 0:
                indtco_erp = indtco_erp + ","
            indtco_erp = indtco_erp + i.codtco
            n = n+1
        context['indtco_erp'] = indtco_erp
        indtco_bco = ""
        n = 0
        n = 0
        for i in Cbttco.objects.filter(indtco="2").all():
            if n > 0:
                indtco_bco = indtco_bco + ","
            indtco_bco = indtco_bco + i.codtco
            n = n+1
        alertaa = ""
        n = 0
        for i in Cbttco.objects.filter(indtco="1").all():
            if n > 0:
                alertaa = alertaa + "\\n"
            alertaa = alertaa + i.codtco + " : " + i.destco
            n = n+1
        context['alertaa'] = alertaa
        alertab = ""
        n = 0
        for i in Cbttco.objects.filter(indtco="2").all():
            if n > 0:
                alertab = alertab + "\\n"
            alertab = alertab + i.codtco + " : " + i.destco
            n = n+1
        context['alertab'] = alertab
        alertac = ""
        n = 0
        for i in Cbttco.objects.filter().all():
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
            getTiposDeConciliacion(request).content)
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
    print(request)
    print(request.POST.get("idrenc"))
    aCbrenc = Cbrenc.objects.get(idrenc= request.POST.get("idrenc"))
    if Cbrenc.objects.filter(cliente=aCbrenc.cliente, codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta, idrenc__gt = aCbrenc.idrenc).exists():
        data = {}
        data["info"] = "No es posible desconciliar"
        return JsonResponse(data)
    
    aCbrenc.estado = 1
    aCbrenc.save()
    return HttpResponse("")
