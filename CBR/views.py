
#region imports
import base64
import datetime as dt
import json
import os
from pathlib import Path
from wsgiref.util import FileWrapper

import pandas as pd
import requests
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction

from django.db.models import F, Func, Max
from django.db.models.query import RawQuerySet, prefetch_related_objects
from django.http import (FileResponse, HttpResponseRedirect, JsonResponse,
                         request)
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic import CreateView, ListView, UpdateView, View

from CBR.forms import (CbrbcodForm, CbrencaForm, CbrencDeleteForm, CbrerpdForm,
                       CbtbcoForm, CbtctaForm, CbtempForm, CbtusucForm,
                       CbtusuForm)
from CBR.homologacion import *
from CBR.models import (Cbmbco, Cbrbcod, Cbrbcoe, Cbrbode, Cbrenc,
                        Cbrencl, Cbrenct, Cbrerpd, Cbrerpe, Cbrgale, Cbsres,
                        Cbsresc, Cbsusu, Cbtbco, Cbtcfge, Cbtcfgc, Cbtcli, Cbtcol, Cbtcon, Cbtcta,
                        Cbtemp, Cbterr, Cbtlic, Cbtpai, Cbttco, Cbtusu,
                        Cbtusuc, Cbtusue, Cbwres, Cbrenci, Cbthom)
from .utils import *
#endregion

#************************* CBF01 - FORMULARIO DE CONCILIACIONES *************************#

class CbrencListView(ListView):
    model = Cbrenc
    template_name = 'cbrenc/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        
        # si no existe la base de datos de CBTTCO la crea, esto solo para pruebas, no mantener en produccion
        populateDatabase()
        data = {}
        try:
            action = request.POST['action']
            cerrarCbrenct(request)
            if action == 'searchdata':
                data = []
                position = 1
                diccionario = clienteYEmpresas(request)
                for i in Cbrenc.objects.all():
                    item = i.toJSON()
                    if item['empresa'] in diccionario["empresas"] and item["cliente"] == diccionario["cliente"]:
                        item['position'] = position
                        item['noDesconciliable'] = Cbrenc.objects.exclude(estado=3).filter(cliente=item["cliente"], codbco=item["codbco"], empresa=item["empresa"], nrocta=item["nrocta"], idrenc__gt = item["idrenc"]).exists()
                        item['archivobco'] = i.archivobco.name
                        item['archivoerp'] = i.archivoerp.name
                        item['moneda']= Cbtcta.objects.filter(nrocta=item["nrocta"]).first().monbasebco
                        if Cbrenct.objects.filter(idrenc = item['idrenc'], formulario= "CBF02", fechorafin=None).exists():
                            item["usuario"] = Cbrenct.objects.filter(idrenc = item['idrenc'], formulario= "CBF02", fechorafin=None).first().idusu
                            item["enuso"] = True
                        else:
                            if Cbwres.objects.filter(idrenc=item['idrenc']).exists():
                                item["usuario"] = Cbwres.objects.filter(idrenc=item["idrenc"]).first().idusu
                                if item["usuario"] == request.user.username:
                                    item["enuso"]=False
                                else:
                                    item["enuso"]=True
                            else:
                                item["enuso"]=False
                                item["usuario"] = ""
                        
                        data.append(item)
                        position += 1
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {}
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        getContext(self.request, context, 'Lista de Conciliaciones', 'CBF01')
        try:
            if self.request.GET.get("accesoinvalido") == "true":
                context['accesoinvalido'] = True
        except Exception as e:
            print(e)
            pass
        aCbtlic = Cbtlic.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"]).first()
        if aCbtlic.fechalic < dt.datetime.now(tz=timezone.utc) + dt.timedelta(days=7):
            context["proximoavencimiento"] = True
            context["fechalic"] = aCbtlic.fechalic
        context["desconciliador"] = False
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        if aCbtusu.indconc == "S":
            context["desconciliador"] = True
        return context

#************************* CBF02 - FORMULARIO DE RESULTADOS *************************#

class CbsresListView(ListView):
    model = Cbsres
    template_name = 'cbsres/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            try:

                idrenca = request.GET.get('idrenc')
                if idrenca is None:
                    idrenca = request.POST.get('idrenc')

                diccionario = clienteYEmpresas(request)
                if Cbtusuc.objects.filter(idtusu = Cbtusu.objects.filter(
                        idusu1=request.user.username).first().idtusu).exists() == False:
                    return redirect ("/definircolumnas")
                if Cbwres.objects.filter(idrenc=idrenca).exists():
                    aCbsres = Cbsres.objects.filter(idrenc=idrenca).first()
                    if aCbsres.cliente == diccionario["cliente"] and aCbsres.empresa in diccionario["empresas"]:
                        return redirect('/verificar/?idrenc='+idrenca, idrenc=idrenca)
                    else:
                        return redirect ('/?accesoinvalido=true')
                else:
                    if Cbsres.objects.filter(idrenc=idrenca).exists() == False:
                        try:
                            conciliarSaldos(request)
                        except Exception as e:
                            print(e)
                    aCbsres = Cbsres.objects.filter(idrenc=idrenca).first()
                    if aCbsres.cliente == diccionario["cliente"] and aCbsres.empresa in diccionario["empresas"]:
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        return redirect ('/?accesoinvalido=true')
            
            except Exception as e:
                print(e)
                return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
        

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            idrenc = request.POST['idrenc']
            aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
            ano = aCbrenc.ano
            mes = aCbrenc.mes
            primerRegistro = False
            if action == 'searchdata':
                data = []
                position = 1
                DataSet = Cbsres.objects.order_by(
                    "idsres").filter(idrenc=idrenc)
                for i in DataSet:
                    item = i.toJSON()
                    item["primerRegistro"] = False
                    if primerRegistro == False:
                        
                        fecha = item["fechatrabco"]
                        if fecha is None:
                            fecha = item["fechatraerp"]
                        if primerRegistro == False  and fecha.year== ano and fecha.month == mes:
                            item["primerRegistro"] = True
                            primerRegistro = True


                    # item['id']=position
                    item['ID'] = position
                    item['position'] = position
                    if item['idrerpd'] == 0:
                        item['debeerporiginal'] = 0
                        item['habererporiginal'] = 0
                    else:
                        aCbrerpd = Cbrerpd.objects.filter(
                            idrerpd=item['idrerpd']).first()
                        item['debeerporiginal'] = aCbrerpd.debe
                        item['habererporiginal'] = aCbrerpd.haber
                    data.append(item)
                    position += 1
                createCbrenct(request, idrenc, 2, "CBF02")
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context,'Resultados', 'CBF02')
        context['editable'] = "Editable"
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        context['indconc'] = aCbtusu.indconc == "S"
        idrenca = self.request.GET.get('idrenc')
        codigosExcluidos = ""
        for i in Cbttco.objects.filter(indsuma="0"):
            codigosExcluidos = codigosExcluidos + i.codtco
        context["codigosExcluidos"] = codigosExcluidos
        if idrenca is None:
            idrenca = self.request.POST.get('idrenc')
        aCbrenc = Cbrenc.objects.get(idrenc = idrenca)
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco
        context["empresa"]=aCbrenc.empresa
        context["codbco"]=aCbrenc.codbco
        context["nrocta"]=aCbrenc.nrocta
        context["ano"]=aCbrenc.ano
        context["mes"]=aCbrenc.mes
        # Lee todo la tabla Cbttco y pasa la informacion al renderizaco de la tabla
        calcularTotales(self.request, context)
        return context


class CbsresviewListView(ListView):
    model = Cbsres
    template_name = 'cbsres/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            idrenca = request.GET.get('idrenc')
            if idrenca is None:
                idrenca = request.POST.get('idrenc')

            diccionario = clienteYEmpresas(request)
            aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
            if aCbrenc.cliente == diccionario["cliente"] and aCbrenc.empresa in diccionario["empresas"]:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect ('/?accesoinvalido=true')
        else:
            return redirect("/")

        
        

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            idrenc = request.POST['idrenc']
            if action == 'searchdata':
                data = []
                position = 1
                DataSet = Cbsres.objects.order_by(
                    "idsres").filter(idrenc=idrenc)
                for i in DataSet:
                    item = i.toJSON()
                    # item['id']=position
                    item['ID'] = position
                    item['position'] = position
                    if item['idrerpd'] == 0:
                        item['debeerporiginal'] = 0
                        item['habererporiginal'] = 0
                    else:
                        aCbrerpd = Cbrerpd.objects.filter(
                            idrerpd=item['idrerpd']).first()
                        item['debeerporiginal'] = aCbrerpd.debe
                        item['habererporiginal'] = aCbrerpd.haber
                    data.append(item)
                    position += 1
                createCbrenct(request,idrenc, 7, "CBF02")
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        getContext(self.request, context,'Resultados', 'CBF02')
        context['editable'] = "No Editable"
        idrenca = self.request.GET.get('idrenc')
        if idrenca is None:
            idrenca = self.request.POST.get('idrenc')
        aCbrenc = Cbrenc.objects.get(idrenc = idrenca)
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco
        context["empresa"]=aCbrenc.empresa
        context["codbco"]=aCbrenc.codbco
        context["nrocta"]=aCbrenc.nrocta
        context["ano"]=aCbrenc.ano
        context["mes"]=aCbrenc.mes
        # Lee todo la tabla Cbttco y pasa la informacion al renderizaco de la tabla
        calcularTotales(self.request, context)
        
        return context

#************************* CBF03 - FORMULARIO DE CARGA DE DATOS *************************#

class CbrencCreateView(CreateView):
    model = Cbrenc
    form_class = CbrencaForm
    template_name = 'cbrenc/add-edit.html'

    success_url = reverse_lazy('CBR:cbrenc-list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
            

    def post(self, request, *args, **kwargs):
        data = {}
        aCbtusu = Cbtusu.objects.filter(idusu1=request.user.username).first()
        if aCbtusu == None:
            return redirect("/", permanent=True)
        try:
            diccionario = clienteYEmpresas(request)
            # Lee las respuetas al formulario
            cliente = diccionario["cliente"]
            empresa = request.POST['empresa']
            if empresa not in diccionario["empresas"]:
                data["error"] = "Empresa no habilitada"
                return JsonResponse(data)
            codbco = request.POST['codbco']
            nrocta = request.POST['nrocta']
            ano = request.POST['ano']
            mes = request.POST['mes']
            # verifica que el registro anterior sea del mes y año correspondiente(o del siguiente a cbttca)
            if mes == 1:
                mesanterior = 12
                anoanterior = int(ano)-1
            else:
                mesanterior = int(mes) - 1
                anoanterior = int(ano)
            # Si existe un registro con esa información
            if Cbrenc.objects.exclude(estado="3").filter(codbco=codbco,
                                                         nrocta=nrocta,
                                                         ano=ano,
                                                         mes=mes,
                                                         cliente=cliente,
                                                         empresa=empresa,
                                                         ).exists():

                data['error'] = 'Ya existe un registro con esa información: (' \
                    + ' Cliente ' + cliente \
                    + ' Empresa ' + empresa \
                    + ' Banco: ' + codbco \
                    + ' Cuenta: ' + nrocta \
                    + ' Año: ' + ano \
                    + ' Mes: ' + mes + ')'
            # Si existe la conciliación del mes anterior o no existe la cuenta sigue
            elif Cbrenc.objects.filter(codbco=codbco,
                                       nrocta=nrocta,
                                       ano=anoanterior,
                                       mes=mesanterior,
                                       # cliente=cliente,
                                       empresa=empresa,
                                       estado=2,
                                       ).exists() or Cbrenc.objects.exclude(estado="3").filter(codbco=codbco,
                                                                                               nrocta=nrocta,
                                                                                               # cliente=cliente,
                                                                                               empresa=empresa,
                                                                                               ).exists() == False:
                if Cbrenc.objects.exclude(estado=3).filter(codbco=codbco,
                                         nrocta=nrocta,
                                         ano=anoanterior,
                                         mes=mesanterior,
                                         # cliente=cliente,
                                         empresa=empresa,
                                         ).exists() == False:
                    if Cbtcta.objects.filter(codbco=codbco, nrocta=nrocta, empresa=empresa).exists():
                        aCbtcta = Cbtcta.objects.filter(
                            codbco=codbco, nrocta=nrocta, empresa=empresa).first()
                        if (int(aCbtcta.ano) == int(ano) and int(aCbtcta.mes) == int(mes)-1) or (int(aCbtcta.ano) == int(ano)-1 and int(aCbtcta.mes) == 12 and int(mes) == 1):
                            saldobcoanterior = aCbtcta.saldoinibco
                            saldoerpanterior = aCbtcta.saldoinierp
                        else:
                            data['error'] = "No existe el mes anterior en el listado de cuentas"
                            return JsonResponse(data)
                    else:
                        data['error'] = "No existe la cuenta"
                        return JsonResponse(data)

                else:
                    # Verifica el saldo anterior
                    saldobcoanterior = Cbrenc.objects.exclude(estado="3").get(codbco=codbco,
                                                                              nrocta=nrocta,
                                                                              ano=anoanterior,
                                                                              mes=mesanterior,
                                                                              # cliente=cliente,
                                                                              empresa=empresa,
                                                                              ).saldobco
                    saldoerpanterior = Cbrenc.objects.exclude(estado="3").get(codbco=codbco,
                                                                              nrocta=nrocta,
                                                                              ano=anoanterior,
                                                                              mes=mesanterior,
                                                                              # cliente=cliente,
                                                                              empresa=empresa,
                                                                              ).saldoerp
                if Cbtbco.objects.filter(codbco=codbco).first().actpas != "A":
                    data['error'] = "El Banco no se encuentra activo"
                    return JsonResponse(data)
                if Cbtemp.objects.filter(empresa=empresa).first().actpas != "A":
                    data['error'] = "La Empresa no se encuentra activa"
                    return JsonResponse(data)

                # Crea el CBRENC
                #with transaction.atomic():
                form = self.get_form()
                form.fechact = dt.datetime.now(tz=timezone.utc)
                form.idusualt = request.user.username
                self.CbrencNew = form.save()
                codbco = request.POST.get( 'codbco')
                empresa = request.POST.get( 'empresa')
                aCbmbco = Cbmbco.objects.filter(codbco=codbco).first()
                error = False
                if aCbmbco == None:
                    data['error'] = "El Banco no tiene un sistema homologador válido"
                    error = True
                
                aCbtemp = Cbtemp.objects.filter(empresa=empresa).first()
                if aCbtemp == None:
                    data['error'] = "El ERP no tiene un sistema homologador válido"
                    error = True
                ##Verifica la existencia del codhomerp
                if error == False:
                    codhomerp = aCbtemp.codhomerp
                    if codhomerp == "":
                        codhomerp = Cbtcli.objects.filter(cliente=diccionario["cliente"]).first().codhomerp
                    if codhomerp != "VEGAL":
                        data['error'] = "El ERP no tiene un sistema homologador válido"
                        error = True
                if error == False:
                    codhombco = aCbmbco.codhombco
                    if codhombco == "VEBOD":
                        HomologacionBcoBOD(request, self.CbrencNew,
                                        data, saldobcoanterior)
                    else:
                        data['error'] = "El Banco no tiene un sistema homologador válido"
                        error = True

                    
                    # Homologa el ERP Gal, posteriormente debe verificar que es lo que se encuentra en request.POST.get( 'coderp') para saber que homologacion usar
                    
                if error == False:
                    if codhomerp == "VEGAL":
                        HomologacionErpGAL(request, self.CbrencNew,
                                            data, saldoerpanterior)
                    else:
                        data['error'] = "El ERP no tiene un sistema homologador válido"
                        error = True
                if error == False:
                    self.CbrencNew.cliente = diccionario["cliente"]
                    self.CbrencNew.save()
                    try:
                        imgbco = base64.b64encode(open(str(Path(__file__).resolve(
                        ).parent.parent) + "/media/" + str(self.CbrencNew.archivoimgbco), 'rb').read())
                        aCbrenci = Cbrenci(
                            idrenc=self.CbrencNew.idrenc, imgbco=imgbco)
                        aCbrenci.save()
                        time.sleep(2)
                        os.remove(str(Path(__file__).resolve().parent.parent) +
                                "/media/" + str(self.CbrencNew.archivoimgbco))
                    except:
                        pass
                        # Guarda la imagen del ERP. Se encuentra funcionando pero no es necesario.
                        #try:
                        #    imgerp = base64.b64encode(open(str(Path(__file__).resolve(
                        #    ).parent.parent) + "/media/" + str(self.CbrencNew.archivoimgerp), 'rb').read())
                        #    aCbrencierp = Cbrencierp(
                        #        idrenc=self.CbrencNew.idrenc, imgerp=imgerp)
                        #    aCbrencierp.save()
                        #    time.sleep(2)
                        #    os.remove(str(Path(__file__).resolve().parent.parent) +
                        #              "/media/" + str(self.CbrencNew.archivoimgerp))
                        #except:
                        #    print("No hay imagen de ERP")
                    try:
                        print(data['error'])
                        error = True
                    except:
                        error = False

                if error == True:
                    idrbcoe = Cbrbcoe.objects.filter(
                        idrenc=self.CbrencNew.idrenc).first()
                    if idrbcoe is not None:
                        idrbcoe=idrbcoe.idrbcoe
                    idrerpe = Cbrerpe.objects.filter(
                        idrenc=self.CbrencNew.idrenc).first()
                    if idrerpe is not None:
                        idrerpe=idrerpe.idrerpe
                    Cbrbod.objects.filter(
                        idrenc=self.CbrencNew.idrenc).delete()
                    Cbrgal.objects.filter(
                        idrenc=self.CbrencNew.idrenc).delete()
                    Cbrbcod.objects.filter(
                        idrbcoe=idrbcoe).delete()
                    Cbrerpd.objects.filter(
                        idrerpe=idrerpe).delete()
                    Cbrbcoe.objects.filter(
                        idrenc=self.CbrencNew.idrenc).delete()
                    Cbrerpe.objects.filter(
                        idrenc=self.CbrencNew.idrenc).delete()
                    Cbrenc.objects.filter(
                        idrenc=self.CbrencNew.idrenc).delete()
                    return JsonResponse(data)
                    # Crea el log correspondiente
                aCbrencl = Cbrencl(
                    idrenc=self.CbrencNew,
                    status=0,
                    saldobco=self.CbrencNew.saldobco,
                    saldoerp=self.CbrencNew.saldoerp,
                    difbcoerp=self.CbrencNew.difbcoerp,
                    idusu=request.user.username)

                aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)
                aCbrencl.save(aCbrencl)
                # Crea el archivo de tiempo correspondiente
                createCbrenct(request, self.CbrencNew.idrenc,1, "CBF03")
                # Crea la imagen de banco correspondiente

            else:
                if Cbrenc.objects.filter(codbco=codbco,
                                         nrocta=nrocta,
                                         ano=anoanterior,
                                         mes=mesanterior,
                                         # cliente=cliente,
                                         empresa=empresa,
                                         ).exists():
                    data['error'] = 'El Mes anterior no se encuentra conciliado'
                else:
                    data['error'] = 'Error desconocido'
        except Exception as e:
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request,context, 'Carga de Datos', 'CBF03')
        empresa = []
        banco = []
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        if aCbtusu.tipousu == "S":
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("empresa"):
                empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        else:
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"],actpas="A"):
                if Cbtusue.objects.filter(idtusu=aCbtusu, empresa=empresaAAgregar.empresa).exists():
                    empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        for bancoAAgregar in Cbtbco.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("codbco"):
            try:
                descripcion = Cbmbco.objects.filter(codbco=bancoAAgregar.codbco).first().desbco
            except:
                descripcion = ""
            banco.append({"nombre":bancoAAgregar.codbco, "descripcion":descripcion})
        context["empresas"]=empresa
        context["bancos"]=banco
        return context


class Uploadimage(CreateView):
    model = Cbrenc
    form_class = CbrencaForm
    template_name = 'cbrenc/add-edit.html'

    success_url = reverse_lazy('CBR:cbrenc-list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def get_initial(self):

        
        try:
            aCbrbcoe = Cbrbcoe.objects.get(idrbcoe=self.request.GET.get("idrbcoe"))
            aCbrenc = Cbrenc.objects.filter(idrenc=aCbrbcoe.idrenc.idrenc).first()
            empresa = aCbrenc.empresa
            codbco = aCbrenc.codbco
            nrocta = aCbrenc.nrocta
            ano = aCbrenc.ano
            mes = aCbrenc.mes
            return {"empresa":empresa, "codbco":codbco, "nrocta":nrocta, "ano":ano, "mes":mes}
        except:
            return {}

    def post(self, request, *args, **kwargs):

        data = {}
        form = self.get_form()
        try:
            form = self.get_form()
            self.CbrencNew = form.save()
            aCbrenc = Cbrenc.objects.filter(idrenc=request.POST["idrenc"]).first()
            aCbrenc.archivoimgbco = "temp"
            aCbrenc.save()
            imgbco = base64.b64encode(open(str(Path(__file__).resolve(
            ).parent.parent) + "/media/" + str(self.CbrencNew.archivoimgbco), 'rb').read())
            Cbrenci.objects.filter(idrenc=request.POST["idrenc"]).delete()
            aCbrenci = Cbrenci(
                idrenc=request.POST["idrenc"], imgbco=imgbco)
            aCbrenci.save()
            time.sleep(2)

            os.remove(str(Path(__file__).resolve().parent.parent) +
                        "/media/" + str(self.CbrencNew.archivoimgbco))
            return JsonResponse(data)
        except Exception as e:
            print(e)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request,context, 'Carga de Datos', 'CBF03')
        context["action"]= "edit"
        aCbrbcoe = Cbrbcoe.objects.get(idrbcoe=self.request.GET.get("idrbcoe"))
        context["idrenc"]= aCbrbcoe.idrenc.idrenc
        return context
#************************* CBF04 - FORMULARIO DE LOGS *************************#

class DetalleLogListView(ListView):
    model = Cbrencl
    template_name = 'cbrencl/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            idrenca = request.GET.get('idrenc')
            if idrenca is None:
                idrenca = request.POST.get('idrenc')

            diccionario = clienteYEmpresas(request)
            aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
            if aCbrenc.cliente == diccionario["cliente"] and aCbrenc.empresa in diccionario["empresas"]:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect ('/?accesoinvalido=true')
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            action = request.POST['action']
            idrenc = request.POST['idrenc']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Cbrencl.objects.filter(idrenc=idrenc):
                    item = i.toJSON()
                    item['position'] = position
                    item['ID'] = position
                    # item['idrenc']=i.idrenc
                    data.append(item)
                    position += 1
                createCbrenct(request, idrenc, 7, "CBF04")
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, "Lista de Logs", "CBF04")
        context['idrenc'] = self.request.GET.get('idrenc')
        idrenca = self.request.GET.get('idrenc')
        if idrenca is None:
            idrenca = self.request.POST.get('idrenc')
        aCbrenc = Cbrenc.objects.get(idrenc = idrenca)
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco        
        return context

#************************* CBF05 - FORMULARIO DE TIEMPOS *************************#

class DetalleTiempoListView(ListView):
    model = Cbrenct
    template_name = 'cbrenct/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            idrenca = request.GET.get('idrenc')
            if idrenca is None:
                idrenca = request.POST.get('idrenc')

            diccionario = clienteYEmpresas(request)
            aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
            if aCbrenc.cliente == diccionario["cliente"] and aCbrenc.empresa in diccionario["empresas"]:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect ('/?accesoinvalido=true')
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            idrenc = request.POST['idrenc']
            if action == 'searchdata':
                data = []
                position = 1
                tiempoacum = dt.timedelta(0)
                largo = Cbrenct.objects.filter(idrenc=idrenc).count()
                for i in Cbrenct.objects.filter(idrenc=idrenc)[:largo-1]:
                    item = i.toJSON()
                    item['position'] = position
                    item['ID'] = position
                    try:
                        tiempoacum = tiempoacum + item['tiempodif']
                    except:
                        pass
                    item['tiempodif'] = str(i.tiempodif)[:-7]
                    item['tiempodifacum'] = str(tiempoacum)[:-7]
                    # item['idrenc']=i.idrenc
                    data.append(item)
                    position += 1
                createCbrenct(request, idrenc, 7, "CBF05")
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Log de Tiempo', 'CBF05')
        context['idrenc'] = self.request.GET.get('idrenc')
        idrenc = self.request.GET['idrenc']
        tiempototal = dt.timedelta(0)
        for i in Cbrenct.objects.filter(idrenc=idrenc):
            try:
                tiempototal += i.tiempodif
            except:
                pass
        tiempototal = str(tiempototal)[:-7].replace("day", "día")
        context["tiempototal"] = tiempototal
        return context

#************************* CBF06 - FORMULARIO DE DETALLE DE BANCO *************************#

class DetalleBcoListView(ListView):
    model = Cbrbcod
    template_name = 'cbrbcod/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            idrenc = request.POST['idrbcoe']
            aCbrbcoe = Cbrbcoe.objects.get(idrenc=idrenc)
            action = request.POST['action']
            data = []
            position = 1
            for i in Cbrbcod.objects.filter(idrbcoe=aCbrbcoe.idrbcoe):
                item = i.toJSON()
                item['position'] = position
                item['ID'] = position
                data.append(item)
                position += 1
            
            createCbrenct(request, aCbrbcoe.idrenc.idrenc, 7, "CBF06" )
                

        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Detalle de carga del archivo de Banco', 'CBF06')
        idrenc = self.request.GET['idrbcoe']
        aCbrbcoe = Cbrbcoe.objects.get(idrenc=idrenc)
        context['idrbcoe'] = aCbrbcoe.idrbcoe
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenc).first()
        context['imagen'] = False
        if aCbrenc.archivoimgbco != "":
            context['imagen'] = True
        if aCbrenc.estado == "0" or aCbrenc.estado == "1":
            context["modificable"] = True
        else:
            context["modificable"] = False
        
        idrenca = self.request.GET.get('idrbcoe')
        if idrenca is None:
            idrenca = self.request.POST.get('idrbcoe')
        aCbrbcoe = Cbrbcoe.objects.get(idrenc=idrenca)
        aCbrenc = aCbrbcoe.idrenc
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco
        return context

#************************* CBF07 - FORMULARIO DE DETALLE DE ERP *************************#
class DetalleErpListView(ListView):
    model = Cbrerpd
    template_name = 'cbrerpd/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            action = request.POST['action']
            idrenc = request.POST['idrerpe']
            idrerpe = Cbrerpe.objects.get(idrenc=idrenc).idrerpe
            if action == 'searchdata':
                data = []
                position = 1
                for i in Cbrerpd.objects.filter(idrerpe=idrerpe):
                    item = i.toJSON()
                    item['position'] = position
                    item['ID'] = position
                    # item['idrenc']=i.idrenc
                    data.append(item)
                    position += 1
                createCbrenct(request, idrenc, 7, "CBF07")
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Detalle de carga del archivo del ERP', 'CBF07')
        
        context['idrerpe'] = self.request.GET.get('idrerpe')
        idrenc = context['idrerpe']
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenc).first()
        #context['imagen'] = False
        #if aCbrenc.archivoimgbco != "":
        #    context['imagen'] = True
        idrenca = self.request.GET.get('idrerpe')
        if idrenca is None:
            idrenca = self.request.POST.get('idrerpe')
        aCbrenc = Cbrenc.objects.get(idrenc = idrenca)
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco
        return context

#************************* CBF08 - FORMULARIO DE CUENTAS *************************#

class CbtctaListView(ListView):
    model = Cbtcta
    template_name = 'cbtcta/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Cbtcta.objects.all():
                    diccionario = clienteYEmpresas(request)
                    item = i.toJSON()
                    if item["empresa"] in diccionario["empresas"] and item["cliente"] in diccionario["cliente"]:
                        item['position'] = position
                        #aCbmbco = Cbmbco.objects.filter(
                        #    codbco=item["codbco"]).first()
                        try:
                            item["codbco"] = item["codbco"]
                        except Exception as e:
                            print(e)
                        if Cbrenc.objects.exclude(estado="3").filter(codbco=i.codbco,
                                                                     nrocta=i.nrocta,
                                                                     empresa=i.empresa,
                                                                     ).exists():
                            item['modificable'] = False
                        else:
                            item['modificable'] = True
                        data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Administración de Cuentas', 'CBF08')
        return context

#************************* CBF09 - FORMULARIO DE NUEVA/EDITAR CUENTA *************************#

class CbtctaCreateView(CreateView):
    model = Cbtcta
    form_class = CbtctaForm
    template_name = 'cbtcta/add-edit.html'

    success_url = reverse_lazy('CBR:cbtcta-list')
    url_redirect = success_url

    def get_initial(self):

        try:
            idtcta = Cbtcta.objects.order_by('-idtcta')[0].idtcta + 1
            return {'idtcta': idtcta}
        except:
            idtcta = 1
            return {'idtcta': idtcta}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            empresa = request.POST['empresa']
            if empresa not in diccionario["empresas"]:
                data['error'] = "Empresa no habilitada"
                return JsonResponse(data)
            codbco = request.POST['codbco']
            aCbtbco = Cbtbco.objects.filter(
                cliente=diccionario["cliente"], codbco=codbco).first()
            if aCbtbco == None:
                data['error'] = "El código de banco no existe"
                return JsonResponse(data, safe=False)
            if aCbtbco.actpas != "A":
                data['error'] = "El código de banco se encuentra inactivo"
                return JsonResponse(data, safe=False)
            aCbtemp = Cbtemp.objects.filter(cliente=diccionario["cliente"], empresa=empresa).first()
            if aCbtemp == None:
                data['error'] = "La Empresa no existe"
                return JsonResponse(data, safe=False)
            if aCbtemp.actpas != "A":
                data['error'] = "La empresa se encuentra pasiva"
                return JsonResponse(data, safe=False)
            nrocta = request.POST['nrocta']
            if Cbtcta.objects.filter(cliente= diccionario["cliente"], empresa=empresa, codbco=codbco, nrocta=nrocta).exists():
                data['error'] = "Cuenta Existente"
                return JsonResponse(data, safe=False)

            # CREATE
            form = self.get_form()

            form = form.save()
            
            form.cliente = diccionario["cliente"]
            form.fechact = dt.datetime.now(tz=timezone.utc)
            form.idusu = request.user.username

            form.save()
            aCbtcon = Cbtcon(codcon=form.codctaconbco, descon=form.descta, actpas="A")
            aCbtcon.fechact = dt.datetime.now(tz=timezone.utc)
            aCbtcon.idusu = request.user.username
            aCbtcon.save()
        except Exception as e:

            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Nueva Cuenta', 'CBF09')
        context['action'] = 'nueva'
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        banco = []
        empresa = []
        if aCbtusu.tipousu == "S":
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("empresa"):
                empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        else:
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"],actpas="A"):
                if Cbtusue.objects.filter(idtusu=aCbtusu, empresa=empresaAAgregar.empresa).exists():
                    empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        for bancoAAgregar in Cbtbco.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("codbco"):
            try:
                descripcion = Cbmbco.objects.filter(codbco=bancoAAgregar.codbco).first().desbco
            except:
                descripcion = ""
            banco.append({"nombre":bancoAAgregar.codbco, "descripcion":descripcion})
        context["empresas"]=empresa
        context["bancos"]=banco
        return context

class CbtctaEditView(CreateView):
    model = Cbtcta
    form_class = CbtctaForm

    def get_initial(self):

        try:
            idtcta = self.request.GET.get('idtcta')
            aCbtcta = Cbtcta.objects.filter(idtcta=idtcta).first()
            print(aCbtcta.nrocta)
            return {'empresa': aCbtcta.empresa, 'codbco': aCbtcta.codbco, 'idtcta': idtcta, 'nrocta': aCbtcta.nrocta, 'descta': aCbtcta.descta, 'diremail' : aCbtcta.diremail, 'monbasebco': aCbtcta.monbasebco, 'codctaconbco':aCbtcta.codctaconbco, 'ano': aCbtcta.ano, 'mes': aCbtcta.mes, 'saldoinibco': aCbtcta.saldoinibco, 'saldoinierp': aCbtcta.saldoinierp}
        except:
            pass

    template_name = 'cbtcta/add-edit.html'

    success_url = reverse_lazy('CBR:cbtcta-list')
    url_redirect = success_url

    def get_object(self):
        idtcta = self.kwargs.get('idtcta')
        return get_object_or_404(Cbtcta, idtcta=idtcta)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            # Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            cliente = diccionario["cliente"]
            idtcta = request.POST['idtcta']
            aCbtcta = Cbtcta.objects.filter(idtcta=idtcta).first()
            empresa = aCbtcta.empresa
            codbco = aCbtcta.codbco
            if empresa not in diccionario["empresas"]:
                data = {}
                data['error'] = "Empresa no habilitada"
                return JsonResponse(data)
            try:
                getPais(empresa)
            except:
                try:
                    data = {}
                    data['error'] = "El código de pais" + \
                        empresa[0:2] + "no existe."
                    return JsonResponse(data)
                except:
                    data = {}
                    data['error'] = "La empresa debe tener al menos dos dígitos."
                    return JsonResponse(data)

            #codbco = request.POST['codbco']
            #nrocta = request.POST['nrocta']
            #descta = request.POST['descta']
            #monbasebco = request.POST['monbasebco']
            #ano = request.POST['ano']
            #mes = request.POST['mes']
            #saldoinibco = request.POST['saldoinibco']
            #saldoinierp = request.POST['saldoinierp']
            aCbtbco = Cbtbco.objects.filter(
                cliente=diccionario["cliente"], codbco=codbco).first()
            if aCbtbco == None:
                data['error'] = "El código de banco no existe"
                return JsonResponse(data, safe=False)
            if aCbtbco.actpas != "A":
                data['error'] = "El código de banco se encuentra inactivo"
                return JsonResponse(data, safe=False)
            aCbtemp = Cbtemp.objects.filter(cliente=diccionario["cliente"], empresa=empresa).first()
            if aCbtemp == None:
                data['error'] = "La Empresa no existe"
                return JsonResponse(data, safe=False)
            if aCbtemp.actpas != "A":
                data['error'] = "La empresa se encuentra pasiva"
                return JsonResponse(data, safe=False)

            # CREATE
            
            form = self.get_form()
            aCbtcta.diremail = request.POST["diremail"]
            aCbtcta.descta = request.POST["descta"]
            print("a")
            if Cbrenc.objects.exclude(estado="3").filter(codbco=aCbtcta.codbco,
            nrocta=aCbtcta.nrocta,
            empresa=aCbtcta.empresa,
            ).exists():
                print("B")
                aCbtcta.save()
            else:
                print("C")           
                nuevoCbtcon = False
                if aCbtcta.codctaconbco != request.POST["codctaconbco"] or aCbtcta.descta != request.POST["descta"]:
                    nuevoCbtcon = True
                aCbtcta.codctaconbco = request.POST["codctaconbco"]
                aCbtcta.empresa = request.POST["empresa"]
                aCbtcta.nrocta = request.POST["nrocta"]
                aCbtcta.codbco = request.POST["codbco"]
                aCbtcta.monbasebco = request.POST["monbasebco"]
                aCbtcta.ano = request.POST["ano"]
                aCbtcta.mes = request.POST["mes"]
                aCbtcta.saldoinibco = request.POST["saldoinibco"]
                aCbtcta.saldoinierp = request.POST["saldoinierp"]
                aCbtcta.fechalt = dt.datetime.now(tz=timezone.utc)
                aCbtcta.idusualt = request.user.username
                aCbtcta.save()
                if nuevoCbtcon:
                    aCbtcon = Cbtcon(codcon=aCbtcta.codctaconbco, descon=aCbtcta.descta, actpas="A")
                    aCbtcon.fechact = dt.datetime.now(tz=timezone.utc)
                    aCbtcon.idusu = request.user.username
                    aCbtcon.save()
        except Exception as e:
            data = {}
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Editar Cuenta', 'CBF09')
        context["editable"] = True
        context["action" ]= "edit"
        context['idtcta'] = self.request.GET.get('idtcta')
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        banco = []
        empresa = []
        if aCbtusu.tipousu == "S":
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("empresa"):
                empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        else:
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"],actpas="A"):
                if Cbtusue.objects.filter(idtusu=aCbtusu, empresa=empresaAAgregar.empresa).exists():
                    empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        for bancoAAgregar in Cbtbco.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("codbco"):
            try:
                descripcion = Cbmbco.objects.filter(codbco=bancoAAgregar.codbco).first().desbco
            except:
                descripcion = ""
            banco.append({"nombre":bancoAAgregar.codbco, "descripcion":descripcion})
        context["empresas"]=empresa
        context["bancos"]=banco
        aCbtcta = Cbtcta.objects.get(idtcta=self.request.GET.get('idtcta'))
        context["empresa"] = aCbtcta.empresa
        context["banco"] = aCbtcta.codbco
        context["nrocta"] = aCbtcta.nrocta
        context["monbasebco"] = aCbtcta.monbasebco
        print(aCbtcta.codctaconbco)
        context["codctaconbco"] = aCbtcta.codctaconbco
        context["ano"] = aCbtcta.ano
        context["mes"] = aCbtcta.mes
        context["saldoinierp"] = aCbtcta.saldoinierp
        context["saldoinibco"] = aCbtcta.saldoinibco
        if Cbrenc.objects.exclude(estado="3").filter(codbco=aCbtcta.codbco,
            nrocta=aCbtcta.nrocta,
            empresa=aCbtcta.empresa,
            ).exists():
            context['modificable'] = False
        else:
            context['modificable'] = True
        return context


#************************* CBF10 - LOG DE ERRORES DE CARGA BANCO *************************#
class DetalleErroresBodListView(ListView):
    model = Cbrbode
    template_name = 'cbrbode/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            action = request.POST['action']
            data = []
            position = 1
            for i in Cbrbode.objects.all():
                detalle = i.idrbod
                item = i.toJSON()
                item['diatra'] = detalle.diatra
                item['oficina'] = detalle.oficina
                item['desctra'] = detalle.desctra
                item['debe'] = detalle.debe
                item['haber'] = detalle.haber
                item['saldo'] = detalle.saldo
                item['position'] = position
                aCbterr = Cbterr.objects.filter(coderr=i.coderr).first()
                item['coderr'] = aCbterr.descerr
                item['ID'] = position
                data.append(item)
                position += 1
        except Exception as e:
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Detalle de Errores Banco','CBF10')
        return context

#************************* CBF11 - LOG DE ERRORES DE CARGA ERP *************************#

class DetalleErroresGalListView(ListView):
    model = Cbrgale
    template_name = 'cbrgale/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            action = request.POST['action']
            data = []
            position = 1
            for i in Cbrgale.objects.all():
                detalle = i.idrgal
                item = i.toJSON()
                item['aux'] = detalle.aux
                item['fechatra'] = detalle.fechatra
                item['nrocomp'] = detalle.nrocomp
                item['ref'] = detalle.ref
                item['glosa'] = detalle.glosa
                item['debe'] = detalle.debe
                item['haber'] = detalle.haber
                item['saldo'] = detalle.saldo
                item['fechacon'] = detalle.fechacon
                item['position'] = position
                aCbterr = Cbterr.objects.filter(coderr=i.coderr).first()
                item['coderr'] = aCbterr.descerr
                item['fechact'] = detalle.fechact
                item['ID'] = position
                data.append(item)
                position += 1
        except Exception as e:
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Detalle de Errores ERP', 'CBF11')
        return context

#************************* CBF12 - CONFIRMACION DE ELIMINAR CONCILIACION *************************#

class ConciliacionDeleteForm(CreateView):
    model = Cbrencl
    form_class = CbrencDeleteForm

    def get_initial(self):
        try:
            idrenc = self.request.GET.get('idrenc')
            return {'idrenc': idrenc}
        except:
            pass

    template_name = 'cbrenc/delete-form.html'

    success_url = reverse_lazy('CBR:cbrenc-list')
    url_redirect = success_url

    def get_object(self):
        idrenc = self.kwargs.get('idrenc')
        return get_object_or_404(Cbrenc, idrenc=idrenc)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            # Lee las respuetas al formulario

            idrenc = request.POST['idrenc']
            aCbrenc = Cbrenc.objects.get(idrenc=idrenc)
            # verifica que no haya registros posteriores
            if Cbrenc.objects.exclude(estado="3").filter(codbco=aCbrenc.codbco,
                                                         nrocta=aCbrenc.nrocta,
                                                         ano__startswith=aCbrenc.ano+1,
                                                         cliente=aCbrenc.cliente,
                                                         empresa=aCbrenc.empresa,
                                                         ).exists() or Cbrenc.objects.exclude(estado="3").filter(codbco=aCbrenc.codbco,
                                                                                                                 nrocta=aCbrenc.nrocta,
                                                                                                                 ano=aCbrenc.ano,
                                                                                                                 mes__startswith=aCbrenc.mes+1,
                                                                                                                 cliente=aCbrenc.cliente,
                                                                                                                 empresa=aCbrenc.empresa,
                                                                                                                 ).exists():
                data['error'] = "Existen meses posteriores cargados"
                return JsonResponse(data, safe=False)
            if Cbwres.objects.filter(idrenc=idrenc).exists():
                data['error'] = "No es posible eliminar, el folio se encuentra en uso"
                return JsonResponse(data, safe=False)

            # CREATE
            createCbrenct(request, idrenc, 7, "CBF12")

            form = self.get_form()
            self.Cbrencl = form.save()
            if self.Cbrencl != {'error': {'glosa': ['Este campo es obligatorio.']}}:

                self.Cbrencl.status = 3
                self.Cbrencl.saldobco = aCbrenc.saldobco
                self.Cbrencl.saldoerp = aCbrenc.saldoerp
                self.Cbrencl.difbcoerp = aCbrenc.difbcoerp
                self.Cbrencl.idusu = request.user.username
                self.Cbrencl.fechact = dt.datetime.now(tz=timezone.utc)
                self.Cbrencl.save()
                aCbrenc.estado = 3
                aCbrenc.save()

        except Exception as e:
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'eliminar', 'CBF12')
        context['idrenc'] = self.request.GET.get('idrenc')
        return context

#************************* CBF13 - NUEVO EDITAR USUARIO *************************#
class CbtusuCreateView(CreateView):
    model = Cbtusu
    form_class = CbtusuForm
    template_name = 'cbtusu/add-edit.html'

    success_url = reverse_lazy('CBR:cbtusu-list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Lee las respuetas al formulario
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                with transaction.atomic():
                    idusu1 = request.POST['idusu1']
                    descusu = request.POST['descusu']
                    tipusu = request.POST.get('tipousu')
                    actpas = request.POST.get('actpas')
                    indconc = request.POST.get('indconc')
                    if actpas is None:
                        actpas = "on"
                    
                    if Cbtusu.objects.filter(idusu1=idusu1).exists() or User.objects.filter(username=idusu1).exists():
                        data['error'] = "Nombre de Usuario Existente"
                        return JsonResponse(data, safe=False)
                    cliente = clienteYEmpresas(request)["cliente"]
                    if actpas == "on":
                        licencias = Cbtlic.objects.filter(cliente=cliente).first().nrousuario
                        usuariosActivos = Cbtusu.objects.filter(actpas="A", cliente=cliente).count()
                        if licencias <= usuariosActivos:
                            data['error'] = "Máximo número de usuarios activos alcanzados. Usuarios activos máximos: "+str(licencias)
                            return JsonResponse(data, safe=False)
                    # CREATE
                    CbtusuNew = Cbtusu(idusu1=idusu1, descusu=descusu, actpas="A")
                    if tipusu == "on":
                        CbtusuNew.tipousu = "S"
                    else:
                        CbtusuNew.tipousu = ""
                    if actpas == "on":
                        CbtusuNew.actpas = "A"
                    else:
                        CbtusuNew.actpas = "P"
                    if indconc == "on":
                        CbtusuNew.indconc = "S"
                    else:
                        CbtusuNew.indconc = ""
                    CbtusuNew.pasusu = True
                    CbtusuNew.fechact = dt.datetime.now(tz=timezone.utc)
                    CbtusuNew.idusu = request.user.username
                    CbtusuNew.cliente = Cbtusu.objects.filter(
                        idusu1=request.user.username).first().cliente
                    
                    CbtusuNew.save(CbtusuNew)
                    empresas = Cbtemp.objects.filter(cliente=CbtusuNew.cliente).all()

            return JsonResponse(data)

        except Exception as e:

            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Nuevo Usuario', 'CBF13')
        context['modificable'] = True
        return context

class CbtusuEditView(CreateView):
    model = Cbtusu
    form_class = CbtusuForm

    def get_initial(self):
        try:
            idusu1 = self.request.GET.get('idusu1')
            aCbtusu = Cbtusu.objects.filter(idusu1=idusu1).first()
            if aCbtusu.tipousu == "S":
                tipousu = True
            else:
                tipousu = False
            if aCbtusu.actpas == "A":
                actpas = True
            else:
                actpas = False
            if aCbtusu.indconc =="S":
                indconc = True
            else:
                indconc = False

            return {'idusu1': aCbtusu.idusu1, 'descusu': aCbtusu.descusu, 'tipousu': tipousu, 'actpas': actpas, 'indconc': indconc}
        except:
            pass

    template_name = 'cbtusu/add-edit.html'

    success_url = reverse_lazy('CBR:cbtusu-list')
    url_redirect = success_url

    def get_object(self):
        idusu1 = self.kwargs.get('idusu1')
        return get_object_or_404(Cbtusu, idusu1=idusu1)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data = {}
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                # Lee las respuetas al formulario
                idusu1 = request.POST['idusu1']
                descusu = request.POST['descusu']
                tipusu = request.POST.get('tipousu')
                actpas = request.POST.get('actpas')
                indconc = request.POST.get('indconc')
                modificable = request.POST.get('modificable')

                idtusu = request.POST.get('idtusu')
                cliente = clienteYEmpresas(request)["cliente"]
                CbtusuNew = Cbtusu.objects.get(idtusu=idtusu)
                
                if actpas == "on":
                    licencias = Cbtlic.objects.filter(
                        cliente=cliente).first().nrousuario
                    usuariosActivos = Cbtusu.objects.filter(
                        actpas="A", cliente=cliente).count()
                    if licencias < usuariosActivos or CbtusuNew.actpas != "A" and licencias == usuariosActivos:
                        data['error'] = "Máximo número de usuarios activos alcanzados. Usuarios activos máximos: " + str(licencias)
                        return JsonResponse(data, safe=False)
                
                if (Cbtusu.objects.filter(idusu1=idusu1).exists() or User.objects.filter(username=idusu1).exists()) and CbtusuNew.idusu1 != idusu1:
                    data['error'] = "Nombre de Usuario Existente"
                    return JsonResponse(data, safe=False)
                # CREATE
                if CbtusuNew.actpas == "A" and actpas != "on":
                    
                    if CbtusuNew.idusu1 == request.user.username:
                        data['error'] = "No puede pasivarse al propio usuario"
                        return JsonResponse(data, safe=False)
                    aCbsusu = Cbsusu.objects.filter(idusu1=idusu1, finlogin = None).first()
                    if aCbsusu != None:
                        aCbsusu.finlogin = dt.datetime.now(tz=timezone.utc)
                        aCbsusu.save()
                    Cbwres.objects.filter(idusu=idusu1).delete()
                    aCbrenct= Cbrenct.objects.filter(idusu=idusu1, fechorafin=None).first()
                    if aCbrenct != None:
                        aCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)
                        aCbrenct.save()
                aUser = User.objects.filter(username=CbtusuNew.idusu1).first()

                if actpas == "on":
                    CbtusuNew.actpas = "A"
                else:
                    CbtusuNew.actpas = "P"
                if indconc == "on":
                    CbtusuNew.indconc = "S"
                else:
                    CbtusuNew.indconc = ""
                if tipusu == "on":
                    CbtusuNew.tipousu = "S"
                else:
                    if CbtusuNew.tipousu == "S" and Cbtusu.objects.filter(cliente = cliente, tipousu= "S").count() == 1:
                        data['error'] = "Debe haber al menos un superusuario"
                        return JsonResponse(data, safe=False)
                    CbtusuNew.tipousu = ""

                if idusu1 != CbtusuNew.idusu1:
                    usuario = User.objects.filter(username=CbtusuNew.idusu1).first()
                    usuario.username = idusu1
                    usuario.save()
                    CbtusuNew.idusu1 = idusu1
                CbtusuNew.descusu = descusu
                
                

                CbtusuNew.fechact = dt.datetime.now(tz=timezone.utc)
                CbtusuNew.idusu = request.user.username
                CbtusuNew.cliente = Cbtusu.objects.filter(
                    idusu1=request.user.username).first().cliente
                CbtusuNew.save()


        except Exception as e:
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Editar Usuario', 'CBF13')
        context['modificable'] = True
        idusu1 = self.request.GET.get("idusu1")
        context["idtusu"] = self.request.GET.get("idtusu")
        context["action"]="edit"
        if Cbrenc.objects.filter(idusucons=idusu1).exists():
            context['modificable'] = False
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        return context


#************************* CBF14 - FORMULARIO DE EMPRESAS *************************#

class ListaEmpresaView(ListView):
    model = Cbtemp
    template_name = 'cbtemp/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")


    def post(self, request, *args, **kwargs):
        diccionario = clienteYEmpresas(request)
        position = 1
        data = []
        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            for i in Cbtemp.objects.all():
                item = i.toJSON()
                if item['empresa'] in diccionario["empresas"] and item["cliente"] == diccionario["cliente"]:
                    item['position'] = position
                    item['pais'] = getPais(item['empresa'])
                    item["movimiento"] = Cbtcta.objects.filter(empresa = item['empresa'], cliente = diccionario["cliente"]).exists()
                    data.append(item)
                    position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Administracion de Empresas', "CBF14")
        return context

#************************* CBF15 - FORMULARIO DE USUARIOS *************************#

class ListaUsuarioView(ListView):
    model = Cbtusu
    template_name = 'cbtusu/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu != "S":
                return redirect("/")
        except:
            return redirect("/")
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            position = 1
            data = []
            diccionario = clienteYEmpresas(request)
            for i in Cbtusu.objects.all():
                if i.superusu != "S" and i.cliente == diccionario["cliente"]:
                    item = i.toJSON()
                    item['position'] = position
                    item["modificable"] = True
                    item["eliminable"] = True
                    if item["idusu1"] == request.user.username:
                        item["eliminable"] = False
                    if Cbrenc.objects.filter(idusucons=item["idusu1"]).exists():
                        item["modificable"] = False

                    data.append(item)
                    position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, "Administración de Usuarios", 'CBF15')
        return context

#************************* CBF16 - FORMULARIO DE USUARIOS Y EMPRESAS *************************#

class ListaCbtusueView(ListView):
    model = Cbtusue
    template_name = 'cbtusue/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")


    def post(self, request, *args, **kwargs):
        diccionario = clienteYEmpresas(request)

        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            position = 1
            data = []
            empresas = Cbtemp.objects.filter(
                cliente=diccionario["cliente"]).all()
            for usuario in Cbtusu.objects.filter(cliente=diccionario["cliente"]).all():
                for empresa in empresas:
                    if usuario.superusu != "S" and usuario.actpas == "A":
                        item = {}
                        item['superusuario'] = usuario.tipousu == "S"
                        item['position'] = position
                        item["usuario"] = usuario.idusu1
                        item["empresa"] = empresa.empresa
                        item["permiso"] = Cbtusue.objects.filter(
                            idtusu=usuario.idtusu, empresa=empresa.empresa).exists()
                        data.append(item)
                        position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Administración de Usuarios y Empresas', 'CBF16')
        return context

#************************* CBF17 - FORMULARIO DE BANCOS *************************#

class ListaBancoView(ListView):
    model = Cbtbco
    template_name = 'cbtbco/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        diccionario = clienteYEmpresas(request)
        position = 1
        data = []
        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            for i in Cbtbco.objects.all():
                item = i.toJSON()
                if item["cliente"] == diccionario["cliente"]:
                    item['position'] = position
                    item['pais'] = getPais(item['codbco'])
                    try:
                        item['desbco'] = Cbmbco.objects.filter(codbco=item["codbco"]).first().desbco
                    except:
                        item['desbco'] = ""
                    data.append(item)
                    position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Administracion de Bancos', 'CBF17')
        return context






 #

#************************* CBF18 - DETALLE DE TIPOS DE CONCILIACION *************************#

class DetalleTiposDeConciliacion(ListView):
    model = Cbttco
    template_name = 'cbttco/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            idrenc = request.POST['idrenc']
            data = []
            data2 = []
            position = 1
            listadoSumaDebeBco = []
            listadoSumaHaberBco = []
            listadoSumaDebeErp = []
            listadoSumaHaberErp = []
            listadoSumaDebeBcoNoSaldo = []
            listadoSumaHaberBcoNoSaldo = []
            listadoSumaDebeErpNoSaldo = []
            listadoSumaHaberErpNoSaldo = []

            datos = {}
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
                        
                else:
                    if tipo.erpbco == 1:
                        if tipo.inddebhab == "H":
                            listadoSumaDebeBcoNoSaldo.append(tipo.codtco)
                        elif tipo.inddebhab == "D":
                            listadoSumaHaberBcoNoSaldo.append(tipo.codtco)
                    elif tipo.erpbco == 2:
                        if tipo.inddebhab == "H":
                            listadoSumaDebeErpNoSaldo.append(tipo.codtco)
                        elif tipo.inddebhab == "D":
                            listadoSumaHaberErpNoSaldo.append(tipo.codtco)

            # calcula primero las del cbwres y si no existen las del cbsres


            for registro in Cbsres.objects.filter(idrenc=idrenc).order_by("idsres").all():

                if Cbwres.objects.filter(idsres=registro.idsres).exists():
                    registroAnalizado = Cbwres.objects.filter(
                        idsres=registro.idsres).first()
                else:
                    registroAnalizado = registro
                saldoBco = registroAnalizado.saldoacumesbco
                saldoErp = registroAnalizado.saldoacumeserp
                
                
                if registroAnalizado.codtcobco in listadoSumaDebeErp:
                    try:
                        datos[registroAnalizado.codtcobco] = [
                            "debe", registroAnalizado.haberbco + datos[registroAnalizado.codtcobco][1]]
                    except:
                        datos[registroAnalizado.codtcobco] = [
                            "debe", registroAnalizado.haberbco]
                elif registroAnalizado.codtcobco in listadoSumaHaberErp:
                    try:
                        datos[registroAnalizado.codtcobco] = [
                            "haber", registroAnalizado.debebco + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcobco] = [
                            "haber", registroAnalizado.debebco]
                if registroAnalizado.codtcoerp in listadoSumaDebeBco:
                    try:
                        datos[registroAnalizado.codtcoerp] = [
                            "debe", registroAnalizado.habererp + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcoerp] = [
                            "debe", registroAnalizado.habererp]
                elif registroAnalizado.codtcoerp in listadoSumaHaberBco:
                    try:
                        datos[registroAnalizado.codtcoerp] = [
                            "haber", registroAnalizado.debeerp + datos[registroAnalizado.codtcoerp][1]]
                    except Exception as e:
                        datos[registroAnalizado.codtcoerp] = [
                            "haber", registroAnalizado.debeerp]
                if registroAnalizado.codtcobco in listadoSumaDebeErpNoSaldo:
                    try:
                        datos[registroAnalizado.codtcobco] = [
                            "debeNoSaldo", registroAnalizado.haberbco + datos[registroAnalizado.codtcobco][1]]
                    except:
                        datos[registroAnalizado.codtcobco] = [
                            "debeNoSaldo", registroAnalizado.haberbco]
                elif registroAnalizado.codtcobco in listadoSumaHaberErpNoSaldo:
                    try:
                        datos[registroAnalizado.codtcobco] = [
                            "haberNoSaldo", registroAnalizado.debebco + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcobco] = [
                            "haberNoSaldo", registroAnalizado.debebco]
                if registroAnalizado.codtcoerp in listadoSumaDebeBcoNoSaldo:
                    try:
                        datos[registroAnalizado.codtcoerp] = [
                            "debeNoSaldo", registroAnalizado.habererp + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcoerp] = [
                            "debeNoSaldo", registroAnalizado.habererp]
                elif registroAnalizado.codtcoerp in listadoSumaHaberBcoNoSaldo:
                    try:
                        datos[registroAnalizado.codtcoerp] = [
                            "haberNoSaldo", registroAnalizado.debeerp + datos[registroAnalizado.codtcoerp][1]]
                    except Exception as e:
                        datos[registroAnalizado.codtcoerp] = [
                            "haberNoSaldo", registroAnalizado.debeerp]

            for i in Cbttco.objects.order_by("ordtco").order_by("-indsuma").all():
                item = i.toJSON()
                item['position'] = position
                item['ID'] = position
                item["debe"] = 0
                item["haber"] = 0
                item['indsum'] = True
                try:
                    if datos[i.codtco][0] == "debe":
                        if i.erpbco == 1:
                            saldoBco -= datos[i.codtco][1]
                            item["saldoacumulado"] = saldoBco
                        else:
                            saldoErp += datos[i.codtco][1]
                            item["saldoacumulado"] = saldoErp
                        item["debe"] = item["debe"] + datos[i.codtco][1]
                    elif datos[i.codtco][0] == "haber":
                        if i.erpbco == 1:
                            saldoBco += datos[i.codtco][1]
                            item["saldoacumulado"] = saldoBco
                        else:
                            saldoErp -= datos[i.codtco][1]
                            item["saldoacumulado"] = saldoErp
                        item["haber"] = item["haber"] + datos[i.codtco][1]
                    elif datos[i.codtco][0] == "debeNoSaldo":
                        item["debe"] = item["debe"] + datos[i.codtco][1]
                        item["indsum"] = False
                    elif datos[i.codtco][0] == "haberNoSaldo":
                        item["haber"] = item["haber"] + datos[i.codtco][1]
                        item["indsum"] = False
                except:
                    pass
                if i.erpbco == 1:
                    item["saldoacumulado"] = saldoBco
                else:
                    item["saldoacumulado"] = saldoErp

                # item['idrenc']=i.idrenc
                data.append(item)
                position += 1
            
            
            try:
                createCbrenct(request, idrenc.first(),7,"CBF18" )
                
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Tipos de Conciliacion', 'CBF18')
        context['idrenc'] = self.request.GET.get('idrenc')
        return context

#************************* CBF19 - DEFINIR VISIBILIDAD COLUMNAS *************************#

class definirColumnas(ListView):
    
    model = Cbtcol
    template_name = 'cbtusuc/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        #crea las cbtusuc por defecto
        idtusu = Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu
        
        Cbtusuc.objects.filter(idtusu=idtusu).delete()
        for aCbtcol in Cbtcol.objects.filter(inddef=1):
            aCbtusuc = Cbtusuc(idtusu=idtusu, codcol=aCbtcol.codcol)
            aCbtusuc.fechact = dt.datetime.now(tz=timezone.utc)
            aCbtusuc.idusu = request.user.username
            aCbtusuc.save()

        #carga el formulario
        
        position = 1
        data = []
        for i in Cbtcol.objects.all():
            item = i.toJSON()
            data.append(item)
            position += 1
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Formulario de Visibilidad de Columnas', 'CBF19')
        return context

#************************* CBF20 - NUEVA EDITAR EMPRESA *************************#
class CbtempCreateView(CreateView):
    model = Cbtemp
    form_class = CbtempForm
    template_name = 'cbtemp/add-edit.html'

    success_url = reverse_lazy('CBR:cbtemp-list')
    url_redirect = success_url

    def get_initial(self):
        cliente = clienteYEmpresas(self.request)["cliente"]
        aCbtcli = Cbtcli.objects.get(cliente=cliente)
        return{"diremail":aCbtcli.diremail}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                # Lee las respuetas al formulario
                diccionario = clienteYEmpresas(request)
                cliente = diccionario["cliente"]
                empresa = request.POST["empresa"]
                desemp = request.POST["desemp"]
                codhomerp = request.POST["codhomerp"]
                diremail = request.POST["diremail"]
                if codhomerp == Cbtcli.objects.get(cliente=diccionario["cliente"]).codhomerp:
                    codhomerp = ""
                try:
                    actpas = request.POST["actpas"]
                    if actpas == "on":
                        actpas = "A"
                    else:
                        actpas = "P"
                except:
                    actpas = "P"
                try:
                    getPais(empresa)
                except:
                    try:
                        data = {}
                        data["error"] = "el código de país " + \
                            empresa[0:2] + " no existe."
                        return JsonResponse(data)
                    except:
                        data = {}
                        data["error"] = "La Empresa debe tener más de dos digitos."
                        return JsonResponse(data)
                empresasMaximas = Cbtlic.objects.filter(
                    cliente=diccionario["cliente"]).first().nroempresa
                empresasActivas = Cbtemp.objects.filter(
                    cliente=diccionario["cliente"], actpas="A").count()
                if empresasActivas >= empresasMaximas and actpas == "A":
                    data = {}
                    data["error"] = "Se alcanzó el limite máximo de empresas activas: " + str(empresasMaximas)
                    return JsonResponse(data)
                if Cbtemp.objects.filter(empresa = empresa, cliente=cliente).exists():
                    data = {}
                    data["error"] = "No puede repetirse nombre de la Empresa"
                    return JsonResponse(data)
                aCbtusue = Cbtusue(idtusu=Cbtusu.objects.filter(
                    idusu1=request.user.username).first(), actpas="A", empresa=empresa)
                aCbtusue.idusu = request.user.username
                aCbtusue.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtusue.save()
                # CREATE
                aCbtemp = Cbtemp(empresa=empresa, desemp=desemp, actpas=actpas, codhomerp=codhomerp, diremail=diremail)
                aCbtemp.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtemp.idusu = request.user.username
                aCbtemp.cliente = diccionario["cliente"]
                aCbtemp.save()
        except Exception as e:
            data = {}
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Nueva Empresa', 'CBF20')
        context['editable'] = True
        context["inactiva"] = False
        context['empresas_url'] = reverse_lazy('CBR:cbtemp-list')
        homologadores = Cbthom.objects.filter(indhom="E").order_by("codhom").all()
        cbthom = []
        for aCbthom in homologadores:
            cbthom.append({"nombre":aCbthom.codhom, "selected":False})
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        aCbtcli = Cbtcli.objects.filter(cliente=aCbtusu.cliente).first()
        for acbthom in cbthom:
            if acbthom["nombre"]==aCbtcli.codhomerp:
                acbthom["selected"]=True
        context['codhomerp'] = cbthom
        return context

class CbtempEditView(CreateView):
    model = Cbtemp
    form_class = CbtempForm

    def get_initial(self):
        try:
            idtemp = self.request.GET.get('idtemp')
            aCbtemp = Cbtemp.objects.filter(idtemp=idtemp).first()
            actpas = aCbtemp.actpas == "A"
            return {'empresa': aCbtemp.empresa, 'desemp': aCbtemp.desemp, 'actpas': actpas, 'codhomerp' : aCbtemp.codhomerp, 'diremail' : aCbtemp.diremail}
        except Exception as e:
            print(e)

    template_name = 'cbtemp/add-edit.html'

    success_url = reverse_lazy('CBR:cbtemp-list')
    url_redirect = success_url

    def get_object(self):
        idtemp = self.kwargs.get('idtemp')
        return get_object_or_404(Cbtemp, idtemp=idtemp)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                diccionario = clienteYEmpresas(request)
                cliente = diccionario["cliente"]
                empresa = request.POST["empresa"]
                desemp = request.POST["desemp"]
                codhomerp = request.POST["codhomerp"]
                diremail = request.POST["diremail"]

                if codhomerp == Cbtcli.objects.get(cliente=diccionario["cliente"]).codhomerp:
                    codhomerp = ""
                try:
                    actpas = request.POST["actpas"]
                    if actpas == "on":
                        actpas = "A"
                    else:
                        actpas = "P"
                except:
                    actpas = "P"
                try:
                    getPais(empresa)
                except:
                    try:
                        data = {}
                        data["error"] = "el código de país " + \
                            empresa[0:2] + " no existe."
                        return JsonResponse(data)
                    except:
                        data = {}
                        data["error"] = "La Empresa debe tener más de dos digitos."
                        return JsonResponse(data)
                empresasMaximas = Cbtlic.objects.filter(
                    cliente=diccionario["cliente"]).first().nroempresa
                empresasActivas = Cbtemp.objects.filter(
                    cliente=diccionario["cliente"], actpas="A").count()
                idtemp = self.request.POST.get('idtemp')
                aCbtemp = Cbtemp.objects.filter(idtemp=idtemp).first()
                if (empresasActivas >= empresasMaximas and actpas == "A" and aCbtemp.actpas != "A") or (empresasActivas > empresasMaximas and actpas == "A" and aCbtemp.actpas == "A"):
                    data = {}
                    data["error"] = "Se alcanzó el limite máximo de empresas activas: " + str(empresasMaximas)
                    return JsonResponse(data)
                if Cbtemp.objects.filter(empresa = empresa, cliente=cliente).exists() and empresa != Cbtemp.objects.filter(idtemp=idtemp).first().empresa:
                    data = {}
                    data["error"] = "No puede repetirse nombre de la Empresa"
                    return JsonResponse(data)
                aCbtusue = Cbtusue(idtusu=Cbtusu.objects.filter(
                    idusu1=request.user.username).first(), actpas="A", empresa=empresa)
                aCbtusue.idusu = request.user.username
                aCbtusue.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtusue.save()
                # CREATE
                
                aCbtemp.diremail = diremail
                aCbtemp.empresa = empresa
                aCbtemp.desemp = desemp
                aCbtemp.actpas = actpas
                aCbtemp.codhomerp = codhomerp
                aCbtemp.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtemp.idusu = request.user.username
                aCbtemp.cliente = diccionario["cliente"]
                aCbtemp.save()
        except Exception as e:
            data = {}
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Editar Empresa', 'CBF20')
        context['action'] = 'edit'
        context['idtemp'] = self.request.GET.get('idtemp')
        context["editable"] = True
        context["inactiva"] = True
        empresa = Cbtemp.objects.filter(
            idtemp=context['idtemp']).first()
        if empresa.actpas == "A":
            context["inactiva"] = False
        else:
            context["inactiva"] = True
        if Cbrenc.objects.exclude(estado=3).filter(empresa=empresa.empresa).exists() or Cbtcta.objects.filter(empresa=empresa.empresa).exists():
            context["editable"] = False
        cbthom = []
        homologadores = Cbthom.objects.filter(indhom="E").order_by("codhom").all()
        for aCbthom in homologadores:
            if empresa.codhomerp == aCbthom.codhom:
                cbthom.append({"nombre":aCbthom.codhom, "selected":True})
            else:
                cbthom.append({"nombre":aCbthom.codhom, "selected":False})
            if empresa.codhomerp == "":
                aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
                aCbtcli = Cbtcli.objects.filter(cliente=aCbtusu.cliente).first()
                for acbthom in cbthom:
                    if acbthom["nombre"]==aCbtcli.codhomerp:
                        acbthom["selected"]=True
        context['codhomerp'] = cbthom
        
        context['empresas_url'] = reverse_lazy('CBR:cbtemp-list')
        return context

#************************* CBF21 - NUEVO EDITAR BANCO *************************#

class CbtbcoEditView(CreateView):
    model = Cbtbco
    form_class = CbtbcoForm

    def get_initial(self):
        try:
            idtbco = self.request.GET.get('idtbco')
            aCbtbco = Cbtbco.objects.filter(idtbco=idtbco).first()
            actpas = aCbtbco.actpas == "A"
            return {'codbco': aCbtbco.codbco, 'actpas': actpas}
        except Exception as e:
            print(e)

    template_name = 'cbtbco/add-edit.html'

    success_url = reverse_lazy('CBR:cbtbco-list')
    url_redirect = success_url

    def get_object(self):
        idtbco = self.kwargs.get('idtbco')
        return get_object_or_404(Cbtemp, idtbco=idtbco)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                diccionario = clienteYEmpresas(request)
                cliente = diccionario["cliente"]
                banco = request.POST["codbco"]
                try:
                    actpas = request.POST["actpas"]
                    if actpas == "on":
                        actpas = "A"
                    else:
                        actpas = "P"
                except:
                    actpas = "P"
                try:
                    getPais(banco)
                except:
                    try:
                        data = {}
                        data["error"] = "el código de país " + \
                            banco[0:2] + " no existe."
                        return JsonResponse(data)
                    except:
                        data = {}
                        data["error"] = "El Banco debe tener más de dos digitos."
                        return JsonResponse(data)
                ### Para colocar limite máximo de bancos:
                bancosMaximas = Cbtlic.objects.filter(
                    cliente=diccionario["cliente"]).first().nrocodbco
                bancosActivas = Cbtbco.objects.filter(
                    cliente=diccionario["cliente"], actpas="A").count()
                idtbco = self.request.POST.get('idtbco')
                aCbtbco = Cbtbco.objects.filter(idtbco=idtbco).first()
                if (bancosActivas > bancosMaximas and actpas == "A") or (bancosActivas == bancosMaximas and actpas == "A" and aCbtbco.actpas != "A"):
                    data = {}
                    data["error"] = "Se alcanzó el limite máximo de bancos activos. Bancos Máximos = "+ str(bancosActivas)
                    return JsonResponse(data)

                # CREATE
                
                if Cbtbco.objects.filter(codbco = banco, cliente=cliente).exists() and aCbtbco.codbco != banco:
                    data = {}
                    data["error"] = "No puede repetirse el Código de Banco"
                    return JsonResponse(data)


                aCbtbco.codbco = banco
                aCbtbco.actpas = actpas
                aCbtbco.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtbco.idusu = request.user.username
                aCbtbco.cliente = diccionario["cliente"]
                aCbtbco.save()
        except Exception as e:
            data = {}
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context,'Editar banco','CBF21')

        context['action'] = 'edit'
        context['idtbco'] = self.request.GET.get('idtbco')
        context["editable"] = True
        banco = Cbtbco.objects.filter(idtbco=context['idtbco']).first().codbco
        if Cbrenc.objects.exclude(estado=3).filter(codbco=banco, cliente = clienteYEmpresas(self.request)["cliente"]).exists() or Cbtcta.objects.filter(codbco=banco, cliente = clienteYEmpresas(self.request)["cliente"]).exists():
            context["editable"] = False
        return context

class CbtbcoCreateView(CreateView):
    model = Cbtbco
    form_class = CbtbcoForm
    template_name = 'cbtbco/add-edit.html'

    success_url = reverse_lazy('CBR:cbtbco-list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
                # Lee las respuetas al formulario
                diccionario = clienteYEmpresas(request)
                cliente = diccionario["cliente"]
                codbco = request.POST["codbco"]
                try:
                    actpas = request.POST["actpas"]
                    if actpas == "on":
                        actpas = "A"
                    else:
                        actpas = "P"
                except:
                    actpas = "P"
                try:
                    getPais(codbco)
                except:
                    try:
                        data = {}
                        data["error"] = "el código de país " + \
                            codbco[0:2] + " no existe."
                        return JsonResponse(data)
                    except:
                        data = {}
                        data["error"] = "La Empresa debe tener más de dos digitos."
                        return JsonResponse(data)
                bancosMaximas = Cbtlic.objects.filter(
                    cliente=diccionario["cliente"]).first().nrocodbco
                bancosActivas = Cbtbco.objects.filter(
                    cliente=diccionario["cliente"], actpas="A").count()
                if bancosActivas >= bancosMaximas and actpas == "A":
                    data = {}
                    data["error"] = "Se alcanzó el limite máximo de bancos activos. Bancos Máximos = "+ str(bancosActivas)
                    return JsonResponse(data)
                if Cbtbco.objects.filter(codbco = codbco, cliente=cliente).exists():
                    data = {}
                    data["error"] = "No puede repetirse el Código de Banco"
                    return JsonResponse(data)

                # CREATE
                aCbtbco = Cbtbco(codbco=codbco, actpas=actpas)
                aCbtbco.fechact = dt.datetime.now(tz=timezone.utc)
                aCbtbco.idusu = request.user.username
                aCbtbco.cliente = diccionario["cliente"]
                aCbtbco.save()
        except Exception as e:
            data = {}
            data['error'] = str(e)
            print(e)
            return JsonResponse(data)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Nuevo Banco', 'CBF21')
        context['editable'] = True
        return context

#************************* CBF22 - VISUALIZACION POR USUARIO *************************#

class visualizacionUsuarios (ListView):
    model = Cbtusu
    template_name = 'cbsusu/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")


    def post(self, request, *args, **kwargs):
        diccionario = clienteYEmpresas(request)

        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            position = 1
            data = []
            for i in Cbsusu.objects.filter(cliente=diccionario["cliente"]).order_by('-iniciologin').all():
                item = i.toJSON()
                aCbtusu = Cbtusu.objects.filter(idusu1=item["idusu1"]).first()
                try:
                    item["descusu"]=aCbtusu.descusu
                except:
                    item["descusu"]=""
                item["conectado"] = i.finlogin==None
                data.append(item)
                position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Log de Usuarios Conectados', 'CBF22')
        return context

#************************* CBF23 - CONFIGURACION PARA SEMIAUTOMATICAS *************************#

class ConciliacionSemiautomatica (ListView):
    model = Cbtcfge
    template_name = 'cbtcfg/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")


    def post(self, request, *args, **kwargs):
        diccionario = clienteYEmpresas(request)

        if Cbtusu.objects.filter(idusu1=request.user.username).first().tipousu == "S":
            position = 1
            data = []
            for i in Cbtcfge.objects.filter(cliente=diccionario["cliente"]).all():
                item = i.toJSON()
                if i.codcfg ==3:
                    aCbtcfgc = Cbtcfgc.objects.filter(idtcfg=i).first()
                    item["campobco"] = aCbtcfgc.campobco
                    item["campoerp"] = aCbtcfgc.campoerp
                    item["ordencfg"] =  aCbtcfgc.ordencfg
                else:
                    item["ordencfg"] = ""
                    item["campobco"] = ""
                    item["campoerp"] = ""
                
                data.append(item)
                position += 1
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Configuración de conciliaciones semi-automaticas', 'CBF23')
        empresa = []
        banco = []
        aCbtusu = Cbtusu.objects.filter(idusu1=self.request.user.username).first()
        if aCbtusu.tipousu == "S":
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("empresa"):
                empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        else:
            for empresaAAgregar in Cbtemp.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"],actpas="A"):
                if Cbtusue.objects.filter(idtusu=aCbtusu, empresa=empresaAAgregar.empresa).exists():
                    empresa.append({"nombre":empresaAAgregar.empresa, "descripcion":empresaAAgregar.desemp})
        for bancoAAgregar in Cbtbco.objects.filter(cliente=clienteYEmpresas(self.request)["cliente"], actpas="A").order_by("codbco"):
            try:
                descripcion = Cbmbco.objects.filter(codbco=bancoAAgregar.codbco).first().desbco
            except:
                descripcion = ""
            banco.append({"nombre":bancoAAgregar.codbco, "descripcion":descripcion})
        context["empresas"]=empresa
        context["bancos"]=banco
        
        return context

#************************* CBF24 - Detalle de No conciliados *************************#

class CbsresNoConciliados(ListView):
    model = Cbsres
    template_name = 'cbsresnc/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
        

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            idrenc = self.kwargs.get('idrenc')
            data = []
            position = 1
            DataSet = Cbsres.objects.order_by(
                "idsres").filter(idrenc=idrenc)
            for i in DataSet:
                fila = Cbwres.objects.filter(idsres=i.idsres).first()
                if fila is None:
                    fila = i
                if fila.estadobco== 0 and fila.codtcobco is not None and len(fila.codtcobco)>1:
                    item = {}
                    item["tipo"]="Banco"
                    item["codcon"]=fila.codtcobco
                    try:
                        item["indpend"]=Cbttco.objects.filter(codtco=fila.codtcobco, indtco=2).first().indpend
                    except:
                        item["indpend"]=""
                    item["fecha"]=fila.fechatrabco
                    item["id"]=fila.idrbcod
                    item["documento"]=fila.codtra
                    item["glosa"]=fila.desctra
                    item["debe"]=fila.debebco
                    item["haber"]=fila.haberbco
                    item['ID'] = position
                    item['position'] = position
                    data.append(item)
                    position += 1
                if fila.estadoerp== 0 and fila.codtcoerp is not None and len(fila.codtcoerp)>1:
                    item = {}
                    item["tipo"]="ERP"
                    item["codcon"]=fila.codtcoerp
                    try:
                        item["indpend"]=Cbttco.objects.filter(codtco=fila.codtcoerp, indtco=1).first().indpend
                    except:
                        item["indpend"]=""
                    item["fecha"]=fila.fechatraerp
                    item["id"]=fila.idrerpd
                    item["documento"]=fila.nrocomperp
                    item["glosa"]=fila.glosaerp
                    item["debe"]=fila.debeerp
                    item["haber"]=fila.habererp
                    item['ID'] = position
                    item['position'] = position
                    data.append(item)
                    position += 1

            #createCbrenct(request, idrenc, 2, "CBF23")
            
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context,'Detalle de no conciliados', 'CBF24')

        idrenca = self.request.GET.get('idrenc')
        
        if idrenca is None:
            idrenca = self.kwargs.get('idrenc')
        context['idrenc']=idrenca
        aCbrenc = Cbrenc.objects.get(idrenc = idrenca)
        context['moneda'] = Cbtcta.objects.filter(cliente = clienteYEmpresas(self.request)["cliente"], codbco=aCbrenc.codbco, empresa=aCbrenc.empresa, nrocta=aCbrenc.nrocta).first().monbasebco
        if self.request.GET["return"] == 'cbttco':
            context['return_url'] =  "/cbttco/?idrenc=" + str(idrenca)
        elif self.request.GET["return"] == 'cbsres':
            context['return_url'] =  "/cbsres/?idrenc=" + str(idrenca)
        elif self.request.GET["return"] == 'cbsresview':
            context['return_url'] =  "/cbsresview/?idrenc=" + str(idrenca)
        # Lee todo la tabla Cbttco y pasa la informacion al renderizaco de la tabla
        return context

def verLadoBancoHtml(request):
    idrenc = request.GET.get("idrenc")
    send_to, context = CreateContextNoConciliadosBancoHtml(request, idrenc)
    return render(request,'utils/paradescargarbanco.html', context)

def verLadoErpHtml(request):
    idrenc = request.GET.get("idrenc")
    
    send_to, context = CreateContextNoConciliadosErpHtml(request, idrenc)
    print(context)
    return render(request,'utils/paradescargarerp.html', context)
#************************* DETALLES *************************#

class CbrerpdDetailView(UpdateView):
    form_class = CbrerpdForm
    template_name = 'cbrerpd/detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            createCbrenct(request, self.kwargs.get('idrerpe'), 9, "CBF02")
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def get_object(self):
        idrerpd = self.kwargs.get('idrerpd')
        return get_object_or_404(Cbrerpd, idrerpd=idrerpd)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Registro original del archivo del ERP', "Detalle")
        context['id'] = self.kwargs.get('idrerpd')
        context['nombre_id'] = 'IDRERPD'
        context['idrenc'] = self.kwargs.get('idrerpe')
        context['return_url'] = self.request.GET['return_url']
        return context

class CbrbcodDetailView(UpdateView):
    form_class = CbrbcodForm
    template_name = 'cbrbcod/detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            #aCbrbcoe = Cbrbcoe.objects.get(idrenc=self.kwargs.get('idrbcoe'))
            createCbrenct(request, self.kwargs.get('idrbcoe'), 8, "CBF02")
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/")

    def get_object(self):
        idrbcod = self.kwargs.get('idrbcod')
        return get_object_or_404(Cbrbcod, idrbcod=idrbcod)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getContext(self.request, context, 'Registro original del archivo del Banco', "Detalles")
        context['id'] = self.kwargs.get('idrbcod')
        context['nombre_id'] = 'IDRBCOD'
        #aCbrbcoe = Cbrbcoe.objects.get(idrenc=self.kwargs.get('idrbcoe'))
        #context['idrenc'] = aCbrbcoe.idrenc.idrenc
        context['list_cbsres_url'] = reverse_lazy('CBR:cbsres-list')
        context['return_url'] = self.request.GET['return_url']
        return context

#************************* DESCARGAR ARCHIVO *************************#

class DescargarArchivoView(View):
    def get(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            idrbcoe = request.GET.get('idrbcoe')
            if idrbcoe is not None:
                aCbrbcoe = Cbrbcoe.objects.get(idrbcoe=idrbcoe)
                imgbco = Cbrenci.objects.filter(idrenc=aCbrbcoe.idrenc.idrenc).first().imgbco
                try:
                    os.remove(str(Path(__file__).resolve().parent.parent) +
                            "/media/" + 'temp/imagen.pdf')
                except:
                    pass
                file = open(str(Path(__file__).resolve().parent.parent) +
                            "/media/" + 'temp/imagen.pdf', 'wb')
                file.write(base64.b64decode(imgbco))
                file.close()
                wrapper = FileWrapper(open(str(Path(__file__).resolve(
                ).parent.parent) + "/media/" + 'temp/imagen.pdf', 'rb'))
                response = HttpResponse(wrapper, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=' + \
                    'imagenbanco.pdf'
                return response
            else:
                data = {}
                data['error'] = "No existe imagen del banco"
                return JsonResponse(data)
        else:
            return redirect("/")
        #   Para descargar imagen ERP
        #    imgerp = Cbrencierp.objects.filter(idrenc=idrerpe).first().imgerp
        #    try:
        #        os.remove(str(Path(__file__).resolve().parent.parent) +
        #                "/media/" + 'temp/imagen.pdf')
        #    except:
        #        pass
        #    file = open(str(Path(__file__).resolve().parent.parent) +
        #                "/media/" + 'temp/imagen.pdf', 'wb')
        #    file.write(base64.b64decode(imgerp))
        #    file.close()
        #    wrapper = FileWrapper(open(str(Path(__file__).resolve(
        #    ).parent.parent) + "/media/" + 'temp/imagen.pdf', 'rb'))
        #    response = HttpResponse(wrapper, content_type='application/pdf')
        #    response['Content-Disposition'] = 'inline; filename=' + \
        #        'imagenerp.pdf'
        #    return response

class verLadoBancoPdf(View):
    def get(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            crearPdfBanco(self.request)
            wrapper = FileWrapper(open(str(Path(__file__).resolve().parent.parent) + "/media/temp/ladobanco.pdf", 'rb'))
            response = HttpResponse(wrapper, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + \
                'imagenbanco.pdf'
            return response


class verLadoErpPdf(View):
    def get(self, request, *args, **kwargs):
        if chequearNoDobleConexion(request):
            crearPdferp(self.request)
            wrapper = FileWrapper(open(str(Path(__file__).resolve().parent.parent) + "/media/temp/ladoerp.pdf", 'rb'))
            response = HttpResponse(wrapper, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + \
                'imagenbanco.pdf'
            return response


#************************* CERRAR PESTAÑA *************************#

def cerrarOtraPestana(request):
    return render(request, "utils/cerrarotrapestana.html")
