
from django.db.models.query import prefetch_related_objects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from CBR.models import Cbrenci, Cbrbcoe, Cbrenc,Cbrenct, Cbrbcod, Cbrerpd, Cbrerpe, Cbsresc, Cbtbco, Cbsres, Cbtcol, Cbtcta, Cbrencl, Cbtemp, Cbtusu, Cbtusuc, Cbtusue,Cbwres,Cbttco,Cbterr,Cbrbode,Cbrgale, Cbtpai, Cbtcli, Cbsusu,Cbtlic, Cbmbco
from django.views.generic import ListView, UpdateView, View, CreateView
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from CBR.forms import CbrencaForm, CbrbcodForm, CbrerpdForm, CbtctaForm, CbrencDeleteForm, CbtusuForm, CbtempForm, CbtusucForm
from CBR.homologacion import *
import datetime as dt
import base64
import json
from django.db.models import Max, Func, F
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect, FileResponse, request
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
import requests
import os
from wsgiref.util import FileWrapper
from pathlib import Path
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.http import is_safe_url


huso = dt.timedelta(hours=0)

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    try:
        if request.POST.get("autocierre") != True:
            aCbsusu = Cbsusu.objects.filter(idusu1=request.user.username).order_by("corrusu").last()
            aCbsusu.finlogin =  dt.datetime.now(tz=timezone.utc)+huso
            aCbsusu.save()
        else:        
            data={}
            data['error']="Debe cerrar sesión en el otro navegador"
            return JsonResponse( data )
    except:
        pass

@csrf_exempt
def cerrarsesionusuario(request):
    usuario = request.POST.get("usuario")
    data = {}
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario).last()
    aCbsusu.finlogin = dt.datetime.now(tz=timezone.utc)+huso
    aCbsusu.save()
    return JsonResponse( data )

def login(request):
    usuario = request.GET.get("usuario")
    aCbtusu = Cbtusu.objects.filter(idusu1=usuario).first()
    aCbsusu = Cbsusu.objects.filter(idusu1=usuario).last()
    data= {}
    try:
        if aCbsusu.finlogin == None:
            data["yaconectado"]= True 
        else:
            data["yaconectado"]= False
    except Exception as e:
        data["yaconectado"]= False
        print(e)
    data["activo"]=aCbtusu.actpas=="A"
    conectados = Cbsusu.objects.filter(finlogin=None).filter(cliente=aCbtusu.cliente).count()
    conectadosMaximos = Cbtlic.objects.filter(cliente=aCbtusu.cliente)
    try:
        data["reinicia"] = aCbtusu.pasusu
    except:
        data["reinicia"] = False
    return JsonResponse( data )

def reiniciarUsuario(request):
    if request.method == "GET":
        usuario = request.GET.get("usuario")
        return render(request, "registration/reset.html", {"usuario":usuario})
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
    aCbtusu = Cbtusu.objects.filter(idusu1 = request.user.username).first()
    aCbsusu = Cbsusu.objects.filter(idusu1 = request.user.username).order_by("corrusu").last()
    try:
        cliente = aCbtusu.cliente
        idusu1 = request.user.username
        iniciologin = dt.datetime.now(tz=timezone.utc)+huso
        aCbsusu = Cbsusu(cliente=cliente,idusu1=idusu1,iniciologin=iniciologin,fechact=iniciologin, idusu=idusu1)
        aCbsusu.guardar(aCbsusu)
        request.session["iddesesion"]= aCbsusu.corrusu
    except Exception as e:
        try:
            cliente = aCbtusu.cliente
            idusu1 = request.user.username
            iniciologin = dt.datetime.now(tz=timezone.utc)+huso
            aCbsusu = Cbsusu(cliente=cliente,idusu1=idusu1,iniciologin=iniciologin,fechact=iniciologin, idusu=idusu1)
            aCbsusu.guardar(aCbsusu)
            request.session["iddesesion"]= aCbsusu.corrusu
            print(e)
        except Exception as e:
            print(e)
        #cliente = aCbtusu.cliente
        #idusu1 = request.user.username
        #iniciologin = dt.datetime.now(tz=timezone.utc)+huso
        #aCbsusu = Cbsusu(cliente=cliente,idusu1=idusu1,iniciologin=iniciologin,fechact=iniciologin, idusu=idusu1)
        #aCbsusu.guardar(aCbsusu)        
         

class CbrbcodView( View ):
    model=Cbrbcod
    form_class=CbrbcodForm
    template_name='cbrbcod/detail.html'

    def get_object(self, request):

        idrbcod=self.kwargs.get( 'idrbcod' )
        return get_object_or_404( Cbrbcod, idrbcod=idrbcod )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        return super().dispatch( request, *args, **kwargs )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Detalle de Anotación en Banco'


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbrencCreateView( CreateView ):
    model=Cbrenc
    form_class=CbrencaForm
    template_name='cbrenc/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbrenc-list' )
    url_redirect=success_url

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            diccionario = clienteYEmpresas(request)
            #Lee las respuetas al formulario
            cliente= diccionario["cliente"]
            empresa=request.POST['empresa']
            if empresa not in diccionario["empresas"]:
                data["error"] = "Empresa no habilitada"
                return JsonResponse(data)
            codbco=request.POST['codbco']
            nrocta=request.POST['nrocta']
            ano=request.POST['ano']
            mes=request.POST['mes']
            #verifica que el registro anterior sea del mes y año correspondiente(o del siguiente a cbttca)
            if mes == 1:
                mesanterior = 12
                anoanterior = int(ano)-1
            else:
                mesanterior = int(mes) -1
                anoanterior = int(ano)
            #Si existe un registro con esa información    
            if Cbrenc.objects.exclude(estado = "3").filter( codbco=codbco,
                                       nrocta=nrocta,
                                       ano=ano,
                                       mes=mes,
                                       #cliente=cliente,
                                       empresa=empresa,
                                       ).exists():

                data['error']='Ya existe un registro con esa información: (' \
                              + ' Cliente ' + cliente \
                              + ' Empresa ' + empresa \
                              + ' Banco: ' + codbco \
                              + ' Cuenta: ' + nrocta \
                              + ' Año: ' + ano \
                              + ' Mes: ' + mes + ')'
            # Si existe la conciliación del mes anterior o no existe la cuenta sigue
            elif Cbrenc.objects.filter( codbco=codbco,
                                       nrocta=nrocta,
                                       ano=anoanterior,
                                       mes=mesanterior,
                                       #cliente=cliente,
                                       empresa=empresa,
                                       estado = 2,
                                       ).exists() or Cbrenc.objects.exclude(estado = "3").filter( codbco=codbco,
                                                                            nrocta=nrocta,
                                                                           #cliente=cliente,
                                                                           empresa=empresa,
                                       ).exists() == False:                  
                if Cbrenc.objects.filter( codbco=codbco,
                        nrocta=nrocta,
                        ano=anoanterior,
                        mes=mesanterior,
                        #cliente=cliente,
                        empresa=empresa,
                        ).exists() == False:
                        if Cbtcta.objects.filter(codbco=codbco, nrocta=nrocta, empresa=empresa).exists():
                            aCbtcta=Cbtcta.objects.filter(codbco=codbco, nrocta=nrocta, empresa=empresa).first()
                            if (int(aCbtcta.ano) == int(ano) and int(aCbtcta.mes) == int(mes)-1) or (int(aCbtcta.ano) == int(ano)-1 and int(aCbtcta.mes) == 12 and int(mes == 1)):
                                saldobcoanterior = aCbtcta.saldoinibco
                                saldoerpanterior = aCbtcta.saldoinierp
                            else:
                                data['error']="No existe el mes anterior en el listado de cuentas"
                                return JsonResponse( data )
                        else:
                            data['error']="No existe la cuenta"
                            return JsonResponse( data )

                else: 
                    #Verifica el saldo anterior
                    saldobcoanterior = Cbrenc.objects.exclude(estado = "3").get( codbco=codbco,
                        nrocta=nrocta,
                        ano=anoanterior,
                        mes=mesanterior,
                        #cliente=cliente,
                        empresa=empresa,
                        ).saldobco
                    saldoerpanterior = Cbrenc.objects.exclude(estado = "3").get( codbco=codbco,
                        nrocta=nrocta,
                        ano=anoanterior,
                        mes=mesanterior,
                        #cliente=cliente,
                        empresa=empresa,
                        ).saldoerp

                
                # Crea el CBRENC
                form=self.get_form()
                form.fechact=dt.datetime.now(tz=timezone.utc)+huso
                form.idusualt=request.user.username
                self.CbrencNew=form.save()
                archivobco=request.POST.get( 'archivobco', None )
                #Homologa el Banco BOD, posteriormente debe verificar que es lo que se encuentra en request.POST.get( 'codbco') para saber que homologacion usar
                HomologacionBcoBOD(request, self.CbrencNew, data,saldobcoanterior )
                archivoerp=request.POST.get( 'archivoerp', None )
                #Homologa el ERP Gal, posteriormente debe verificar que es lo que se encuentra en request.POST.get( 'coderp') para saber que homologacion usar
                HomologacionErpGAL( request, self.CbrencNew, data, saldoerpanterior )
                self.CbrencNew.cliente = diccionario["cliente"]
                self.CbrencNew.save()
                try:
                    imgbco = base64.b64encode(open(str(Path(__file__).resolve().parent.parent)+ "/media/"+ str( self.CbrencNew.archivoimg ), 'rb').read())
                    aCbrenci = Cbrenci(idrenc = self.CbrencNew.idrenc, imgbco= imgbco)
                    aCbrenci.save()
                    time.sleep(2)
                    os.remove(str(Path(__file__).resolve().parent.parent)+ "/media/"+ str( self.CbrencNew.archivoimg ))
                except:
                    print("No hay imagen de banco")
                try:
                    print( data['error'])
                    error=True
                except:
                    error=False

                if error == True:
                    Cbrbod.objects.filter(idrenc = self.CbrencNew.idrenc).delete()
                    Cbrgal.objects.filter(idrenc = self.CbrencNew.idrenc).delete()
                    Cbrbcod.objects.filter(idrbcoe=self.CbrencNew.idrenc).delete()
                    Cbrerpd.objects.filter(idrerpe=self.CbrencNew.idrenc).delete()
                    Cbrbcoe.objects.filter(idrenc=self.CbrencNew.idrenc).delete()
                    Cbrerpe.objects.filter(idrenc=self.CbrencNew.idrenc).delete()
                    Cbrenc.objects.filter(idrenc=self.CbrencNew.idrenc).delete()
                    return JsonResponse(data)
                #Crea el log correspondiente
                aCbrencl = Cbrencl(
                    idrenc = self.CbrencNew,
                    status = 0,
                    saldobco = self.CbrencNew.saldobco,
                    saldoerp = self.CbrencNew.saldoerp,
                    difbcoerp = self.CbrencNew.difbcoerp,
                    idusu = request.user.username)
                
                aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrencl.save(aCbrencl)
                #Crea el archivo de tiempo correspondiente
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF03", idrenc = aCbrencl.idrenc)
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 1
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
                # Crea la imagen de banco correspondiente
             

            else:
                if Cbrenc.objects.filter( codbco=codbco,
                                       nrocta=nrocta,
                                       ano=anoanterior,
                                       mes=mesanterior,
                                       #cliente=cliente,
                                       empresa=empresa,
                                       ).exists():
                    data['error']='El Mes anterior no se encuentra conciliado'
                else:
                    data['error']='Error desconocido'
        except Exception as e:
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Carga de Datos'
        context['codigo']='CBF03'

        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbtctaCreateView( CreateView ):
    model=Cbtcta
    form_class=CbtctaForm
    template_name='cbtcta/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtcta-list' )
    url_redirect=success_url

    def get_initial(self):
        try:
            idtcta = Cbtcta.objects.order_by('-idtcta')[0].idtcta +1
            return {'idtcta': idtcta}
        except:
            idtcta = 1
            return {'idtcta': idtcta}

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            empresa=request.POST['empresa']
            if empresa not in diccionario["empresas"]:
                data['error'] = "Empresa no habilitada"
                return JsonResponse(data)
            codbco=request.POST['codbco']
            aCbtbco = Cbtbco.objects.filter(cliente= diccionario["cliente"], codbco=codbco).first()
            if aCbtbco== None:
                data['error'] = "El código de banco no existe"
                return JsonResponse( data, safe=False)
            if aCbtbco.actpas!="A":
                data['error'] = "El código de banco se encuentra inactivo"
                return JsonResponse( data, safe=False)
            nrocta=request.POST['nrocta']
            if Cbtcta.objects.filter(empresa=empresa,codbco=codbco,nrocta=nrocta).exists():
                data['error']="Cuenta Existente"
                return JsonResponse( data, safe=False)

            # CREATE
            form=self.get_form()
            form.cliente = diccionario["cliente"]
            form.idtcta = 25
            form.fechalt=dt.datetime.now(tz=timezone.utc)+huso
            form.idusualt=request.user.username

            self.CbrencNew=form.save()
        except Exception as e:

            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'
        context['action']='edit'
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtcta-list' )
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbtctaEditView( CreateView ):
    model=Cbtcta
    form_class=CbtctaForm
    def get_initial(self):
        try:
            idtcta=self.request.GET.get( 'idtcta' )
            aCbtcta = Cbtcta.objects.filter(idtcta=idtcta).first()
            return {'empresa': aCbtcta.empresa, 'codbco': aCbtcta.codbco, 'idtcta': idtcta, 'nrocta': aCbtcta.nrocta,'descta':aCbtcta.descta, 'monbasebco':aCbtcta.monbasebco, 'monbaseerp':aCbtcta.monbaseerp, 'ano':aCbtcta.ano, 'mes':aCbtcta.mes, 'saldoinibco':aCbtcta.saldoinibco, 'saldoinierp': aCbtcta.saldoinierp}
        except:
            pass
    
    template_name='cbtcta/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtcta-list' )
    url_redirect=success_url
    def get_object(self):
        idtcta=self.kwargs.get( 'idtcta' )
        return get_object_or_404( Cbtcta, idtcta=idtcta )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            cliente= diccionario["cliente"]
            idtcta=request.POST['idtcta']
            empresa = request.POST["empresa"]
            if empresa not in diccionario["empresas"]:
                data={}
                data['error']= "Empresa no habilitada"
                return JsonResponse( data )
            try:
                getPais(empresa)
            except:
                try:
                    data={}
                    data['error']="El código de pais"+ empresa[0:2] + "no existe."
                    return JsonResponse( data )
                except:
                    data={}
                    data['error']="La empresa debe tener al menos dos dígitos."
                    return JsonResponse( data )                    
            Cbtcta.objects.filter( idtcta = idtcta ).delete()
            codbco=request.POST['codbco']
            nrocta=request.POST['nrocta']
            descta=request.POST['descta']
            monbasebco=request.POST['monbasebco']
            monbaseerp=request.POST['monbaseerp']
            ano=request.POST['ano']
            mes=request.POST['mes']
            saldoinibco=request.POST['saldoinibco']
            saldoinierp=request.POST['saldoinierp']
            aCbtbco = Cbtbco.objects.filter(cliente= diccionario["cliente"], codbco=codbco).first()
            if aCbtbco== None:
                data['error'] = "El código de banco no existe"
                return JsonResponse( data, safe=False)
            if aCbtbco.actpas!="A":
                data['error'] = "El código de banco se encuentra inactivo"
                return JsonResponse( data, safe=False)

            # CREATE
            form=self.get_form()
            form.fechalt=dt.datetime.now(tz=timezone.utc)+huso
            form.idusualt=request.user.username

            self.CbrencNew=form.save()
        except Exception as e:
            data={}
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'
        context["editable"]=True
        context['idtcta']=self.request.GET.get( 'idtcta' )
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtcta-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbtusuEditView( CreateView ):
    model=Cbtusu
    form_class=CbtusuForm
    def get_initial(self):
        try:
            idusu1=self.request.GET.get( 'idusu1' )
            aCbtusu = Cbtusu.objects.filter(idusu1=idusu1).first()
            if aCbtusu.tipousu == "S":
                tipousu=True
            else:
                tipousu=False
            return {'idusu1': aCbtusu.idusu1, 'descusu': aCbtusu.descusu, 'tipousu': tipousu}
        except:
            pass
    
    template_name='cbtusu/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtusu-list' )
    url_redirect=success_url
    def get_object(self):
        idusu1=self.kwargs.get( 'idusu1' )
        return get_object_or_404( Cbtusu, idusu1=idusu1 )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            
            idusu1=request.POST['idusu1']
            descusu=request.POST['descusu']
            tipusu=request.POST.get('tipousu')

            Cbtusu.objects.filter(idusu1=idusu1).delete()
            cliente = clienteYEmpresas(request)["cliente"]
            licencias = Cbtlic.objects.filter(cliente=cliente).first().nrousuario
            usuariosActivos = Cbtusu.objects.filter(actpas="A", cliente=cliente).count()
            if licencias <= usuariosActivos:
                data['error']="Máximo número de usuarios activos alcanzados"
                return JsonResponse( data, safe=False)
            # CREATE
            CbtusuNew=Cbtusu(idusu1=idusu1, descusu=descusu,actpas="A")
            if tipusu == "on":
                CbtusuNew.tipousu = "S"
            else:
                CbtusuNew.tipousu = ""
            CbtusuNew.pasusu = True
            CbtusuNew.fechact=dt.datetime.now(tz=timezone.utc)+huso
            CbtusuNew.idusu=request.user.username
            CbtusuNew.cliente = Cbtusu.objects.filter(idusu1 = request.user.username).first().cliente
            CbtusuNew.save()
        except Exception as e:

            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'
        context['modificable']=True
        idusu1 = self.request.GET.get("idusu1")
        if Cbrenc.objects.filter(idusucons=idusu1).exists():
            context['modificable']=False
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtusu-list' )
        return context


# ******************************************************************************************************************** #
# ***************************************************************************
class CbtempEditView( CreateView ):
    model=Cbtemp
    form_class=CbtempForm
    def get_initial(self):
        try:
            idtemp=self.request.GET.get( 'idtemp' )
            aCbtemp = Cbtemp.objects.filter(idtemp=idtemp).first()
            actpas = aCbtemp.actpas == "A"
            return {'empresa': aCbtemp.empresa, 'desemp': aCbtemp.desemp, 'actpas': actpas}
        except Exception as e:
            print("error de get initial en cbtemp")
            print(e)
    
    template_name='cbtemp/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtemp-list' )
    url_redirect=success_url
    def get_object(self):
        idtemp=self.kwargs.get( 'idtemp' )
        return get_object_or_404( Cbtemp, idtemp=idtemp )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            cliente= diccionario["cliente"]
            empresa = request.POST["empresa"]
            desemp = request.POST["desemp"]
            actpas = request.POST["actpas"]
            if actpas == "on":
                actpas = "A"
            else:
                actpas = "P"
            try:
                getPais(empresa)
            except:
                try:
                    data={}
                    data["error"]="el código de país "+ empresa[0:2]+ " no existe."
                    return JsonResponse(data)
                except:
                    data={}
                    data["error"]="La Empresa debe tener más de dos digitos."
                    return JsonResponse(data)
            empresasMaximas = Cbtlic.objects.filter(cliente=diccionario["cliente"]).first().nroempresa
            empresasActivas = Cbtemp.objects.filter(cliente=diccionario["cliente"], actpas = "A").count()
            if empresasActivas >= empresasMaximas and actpas == "A":
                data={}
                data["error"]="Se alcanzó el limite máximo de empresas activas"
                return JsonResponse(data)
            aCbtusue=Cbtusue(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first(), actpas="A", empresa=empresa)            
            aCbtusue.idusu = request.user.username
            aCbtusue.fechact = dt.datetime.now(tz=timezone.utc)+huso
            aCbtusue.save()
            # CREATE
            idtemp=self.request.POST.get( 'idtemp' )
            Cbtemp.objects.filter(idtemp=idtemp).delete()
            aCbtemp = Cbtemp(empresa=empresa, desemp=desemp,actpas=actpas )
            aCbtemp.fechact=dt.datetime.now(tz=timezone.utc)+huso
            aCbtemp.idusu=request.user.username
            aCbtemp.cliente=diccionario["cliente"]
            aCbtemp.save()
        except Exception as e:
            data={}
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Editar Empresa'
        context['codigo']='CBF20'
        context['action']='edit'
        context['idtemp']=self.request.GET.get( 'idtemp' )
        context["editable"]=True
        empresa = Cbtemp.objects.filter(idtemp=context['idtemp']).first().empresa
        if Cbrenc.objects.exclude(estado=3).filter(empresa=empresa).exists():
            context["editable"]=False
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtemp-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class CbrencListView( ListView ):
    model=Cbrenc
    template_name='cbrenc/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        # si no existe la base de datos de CBTTCO la crea, esto solo para pruebas, no mantener en produccion
        if Cbtcli.objects.filter(cliente="pablo").exists() == False:
            aCbtcli = Cbtcli(cliente="pablo", descli="describo a pablo")
            aCbtcli.save()
        if Cbtcol.objects.filter(codcol=1).exists() == False:
            aCbtcol = Cbtcol(codcol = 0, descol="idsres", inddef=1)
            aCbtcol.save()
            aCbtcol = Cbtcol(codcol = 1, descol="Fecha Transaccion del Banco", inddef=1)
            aCbtcol.save()
        if Cbttco.objects.filter(codtco = "DPTR").exists() == False:
            aCbttco= Cbttco(1,1,"DPTR","Depositos en Transito (+)",0,1,"H",1)
            aCbttco.save()
            aCbttco= Cbttco(2,2,"CERR","Cargos Erroneos",0,2,"D",0)
            aCbttco.save()
            aCbttco= Cbttco(3,2, "CHNC","Cheques no Contabilizados (-)",0,2,"H",1)
            aCbttco.save()
            aCbttco= Cbttco(4,2,"NDNC","Notas de Debito no C (-)",0,2,"H",1)
            aCbttco.save()
            aCbttco= Cbttco(5,2,"NCNC","Notas de Credito no C(+)",0,2,"D",1)
            aCbttco.save()
            aCbttco= Cbttco(6,2,"DNC","Deposito no Contabilizado (+)",0,2,"D",1)
            aCbttco.save()
            aCbttco= Cbttco(7,1,"NDTR","Notas de Debito en T (-)",0,1,"D",1)
            aCbttco.save()
            aCbttco= Cbttco(8,1,"NCTR","Notas de Credito en T (+)",0,1,"H",1)
            aCbttco.save()
            aCbttco= Cbttco(9,2,"AERR","Abonos Erroneos",0,2,"H",0)
            aCbttco.save()
        if Cbterr.objects.filter(coderr = 99).exists() == False:
            aCbterr = Cbterr(coderr = 1, descerr = "Día Fuera de Calendario")
            aCbterr.save()
            aCbterr = Cbterr(coderr = 2, descerr = "Sin Código de Oficina")
            aCbterr.save()
            aCbterr = Cbterr(coderr = 3, descerr = "Debe Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr = 4, descerr = "Haber Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr = 5, descerr = "Saldo Inválido")
            aCbterr.save()
            aCbterr = Cbterr(coderr = 99, descerr = "Error Desconocido")
            aCbterr.save()
        if Cbterr.objects.filter(coderr = 6).exists() == False:
            aCbterr = Cbterr(coderr = 6, descerr = "Incumple Logica de aplicación")
            aCbterr.save()
        data={}
        try:
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position=1
                diccionario = clienteYEmpresas(request)
                for i in Cbrenc.objects.all():
                    item=i.toJSON()
                    if item['empresa'] in diccionario["empresas"] and item["cliente"] == diccionario["cliente"]:
                        item['position']=position
                        item['archivobco']=i.archivobco.name
                        item['archivoerp']=i.archivoerp.name
                        data.append( item )
                        position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data={}
            print(e)
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Lista de Conciliaciones'
        context['codigo']='CBF01'
        context['create_url']=reverse_lazy( 'CBR:cbrenc_nueva' )
        context['account_url']=reverse_lazy( 'CBR:cbtcta-list' )
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['usuarios_url']=reverse_lazy('CBR:cbtusu-list')
        context['empresas_url']=reverse_lazy('CBR:cbtemp-list')
        aCbtusu = Cbtusu.objects.filter(idusu1 = self.request.user.username).first()
        if aCbtusu.tipousu == "S":
            context['superusuario']=True

        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbtctaListView( ListView ):
    model=Cbtcta
    template_name='cbtcta/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbtcta.objects.all():
                    diccionario = clienteYEmpresas(request)
                    item=i.toJSON()
                    if item["empresa"] in diccionario["empresas"] and item["cliente"] in diccionario["cliente"]:
                        item['position']=position
                        aCbmbco = Cbmbco.objects.filter(codbco=item["codbco"]).first()
                        try:
                            item["codbco"] = item["codbco"] + " : " + aCbmbco.desbco
                        except Exception as e:
                            print(e)
                        if Cbrenc.objects.exclude(estado = "3").filter( codbco=i.codbco,
                            nrocta=i.nrocta,
                            empresa=i.empresa,
                            ).exists():
                            item['modificable']= False
                        else:
                            item['modificable']= True
                        data.append( item )
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Lista de Cuentas'
        context['codigo']='CBF08'
        context['create_url']=reverse_lazy( 'CBR:cbrenc_nueva' )
        context['create_account_url']=reverse_lazy( 'CBR:cbtcta_nueva_cuenta' )
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class CbsresListView( ListView ):
    model=Cbsres
    template_name='cbsres/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        try:
            idrenca=request.GET['idrenc']  
            diccionario = clienteYEmpresas(request)
            if Cbwres.objects.filter(idrenc=idrenca).exists():
                aCbwres = Cbwres.objects.filter(idrenc=idrenca).first()
                if aCbwres.cliente == diccionario["cliente"] and aCbwres.empresa in diccionario["empresas"]:
                    return redirect('/verificar/?idrenc='+idrenca, idrenc= idrenca )
            else:
                if Cbsres.objects.filter(idrenc=idrenca).exists() == False:
                    try:
                        conciliarSaldos(request)
                    except Exception as e:
                        print(e)
                aCbsres = Cbsres.objects.filter(idrenc=idrenca).first()
                if aCbsres.cliente == diccionario["cliente"] and aCbsres.empresa in diccionario["empresas"]:
                    return super().dispatch( request, *args, **kwargs )
        except:
            return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                position=1
                DataSet=Cbsres.objects.order_by("idsres").filter( idrenc=idrenc )
                for i in DataSet:
                    item=i.toJSON()
                    #item['id']=position
                    item['ID']=position
                    item['position'] = position
                    data.append( item )
                    position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )

        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Resultados'
        context['codigo']='CBF02'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['editable']= "Editable"
        # Lee todo la tabla Cbttco y pasa la informacion al renderizaco de la tabla
        from CBR.models import Cbttco
        n = 0
        indtco_erp = ""
        for i in Cbttco.objects.filter(indtco = "1").all():
            if n>0:
                indtco_erp = indtco_erp +","
            indtco_erp = indtco_erp + i.codtco
            n= n+1
        context['indtco_erp'] = indtco_erp
        indtco_bco = ""        
        n= 0
        n = 0
        for i in Cbttco.objects.filter(indtco = "2").all():
            if n>0:
                indtco_bco = indtco_bco +","
            indtco_bco = indtco_bco + i.codtco
            n = n+1
        alertaa = ""
        n = 0
        for i in Cbttco.objects.filter(indtco = "1").all():
            if n>0:
                alertaa = alertaa +"\\n"
            alertaa = alertaa  + i.codtco + " : " + i.destco
            n= n+1
        context['alertaa'] = alertaa
        alertab = ""
        n = 0
        for i in Cbttco.objects.filter(indtco = "2").all():
            if n>0:
                alertab = alertab +"\\n"
            alertab = alertab  + i.codtco + " : " + i.destco
            n= n+1
        context['alertab'] = alertab
        alertac = ""
        n=0
        for i in Cbttco.objects.filter().all():
            if n>0:
                alertac = alertac +"\\n"
            alertac = alertac + i.codtco + " : " + i.destco

            n= n+1
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
            listado = Cbsres.objects.order_by("idsres").filter(idrenc = self.request.GET.get( 'idrenc' ))
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

        tiposDeConciliacion = json.loads(getTiposDeConciliacion(self.request).content)
        context['debebcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["debebcototal"]))
        context['haberbcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["haberbcototal"]))
        context['saldobcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldobcototal"]))
        context['debeerptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["debeerptotal"]))
        context['habererptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["habererptotal"]))
        context['saldoerptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldoerptotal"]))
        context['saldodiferenciatotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldodiferenciatotal"]))
        context['habererp']="$"+'{:,}'.format(habererp)
        context['debeerp']="$"+'{:,}'.format(debeerp)
        context ['debebco']="$"+'{:,}'.format(debebco)
        context ['haberbco']="$"+'{:,}'.format(haberbco)
        context ['saldobco']="$"+'{:,}'.format(saldobco)
        context ['saldoerp']="$"+'{:,}'.format(saldoerp)
        context ['saldodiferencia']="$"+'{:,}'.format(saldodiferencia)
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )

        return context


            

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class CbsresviewListView( ListView ):
    model=Cbsres
    template_name='cbsres/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        idrenca=request.GET['idrenc']  
        diccionario = clienteYEmpresas(request)
        aCbsres = Cbsres.objects.filter(idrenc=idrenca).first()
        if aCbsres.cliente == diccionario["cliente"] and aCbsres.empresa in diccionario["empresas"]:
            return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                position=1
                DataSet=Cbsres.objects.order_by("idsres").filter( idrenc=idrenc )
                for i in DataSet:
                    item=i.toJSON()
                    # item['id']=position
                    item['ID']=position
                    item['position'] = position
                    data.append( item )
                    position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )

        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Resultados'
        context['codigo']='CBF02'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['editable']= "No Editable"
        # Lee todo la tabla Cbttco y pasa la informacion al renderizaco de la tabla
        from CBR.models import Cbttco
        n = 0
        indtco_erp = ""
        for i in Cbttco.objects.filter(indtco = "1").all():
            if n>0:
                indtco_erp = indtco_erp +","
            indtco_erp = indtco_erp + i.codtco
            n= n+1
        context['indtco_erp'] = indtco_erp
        indtco_bco = ""        
        n= 0
        n = 0
        for i in Cbttco.objects.filter(indtco = "2").all():
            if n>0:
                indtco_bco = indtco_bco +","
            indtco_bco = indtco_bco + i.codtco
            n = n+1
        alertaa = ""
        n = 0
        for i in Cbttco.objects.filter(indtco = "1").all():
            if n>0:
                alertaa = alertaa +"\\n"
            alertaa = alertaa  + i.codtco + " : " + i.destco
            n= n+1
        context['alertaa'] = alertaa
        alertab = ""
        n = 0
        for i in Cbttco.objects.filter(indtco = "2").all():
            if n>0:
                alertab = alertab +"\\n"
            alertab = alertab  + i.codtco + " : " + i.destco
            n= n+1
        context['alertab'] = alertab
        alertac = ""
        n=0
        for i in Cbttco.objects.filter().all():
            if n>0:
                alertac = alertac +"\\n"
            alertac = alertac + i.codtco + " : " + i.destco

            n= n+1
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
            listado = Cbsres.objects.order_by("idsres").filter(idrenc = self.request.GET.get( 'idrenc' ))
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

        tiposDeConciliacion = json.loads(getTiposDeConciliacion(self.request).content)
        context['debebcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["debebcototal"]))
        context['haberbcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["haberbcototal"]))
        context['saldobcototal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldobcototal"]))
        context['debeerptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["debeerptotal"]))
        context['habererptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["habererptotal"]))
        context['saldoerptotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldoerptotal"]))
        context['saldodiferenciatotal'] = "$"+'{:,}'.format(float(tiposDeConciliacion["saldodiferenciatotal"]))
        context['habererp']="$"+'{:,}'.format(habererp)
        context['debeerp']="$"+'{:,}'.format(debeerp)
        context ['debebco']="$"+'{:,}'.format(debebco)
        context ['haberbco']="$"+'{:,}'.format(haberbco)
        context ['saldobco']="$"+'{:,}'.format(saldobco)
        context ['saldoerp']="$"+'{:,}'.format(saldoerp)
        context ['saldodiferencia']="$"+'{:,}'.format(saldodiferencia)
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )

        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbrbcodDetailView( UpdateView ):
    form_class=CbrbcodForm
    template_name='cbrbcod/detail.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
            bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
            bCbrenct.save()
        aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = self.kwargs.get( 'idrbcoe' ) ).first())
        aCbrenct.idusu = request.user.username
        aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.accion = 8
        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.save()
        return super().dispatch( request, *args, **kwargs )

    def get_object(self):
        idrbcod=self.kwargs.get( 'idrbcod' )
        return get_object_or_404( Cbrbcod, idrbcod=idrbcod )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Registro original del archivo del Banco'
        context['id']=self.kwargs.get( 'idrbcod' )
        context['nombre_id']='IDRBCOD'
        context['idrenc']=self.kwargs.get( 'idrbcoe' )
        context['list_url']=reverse_lazy( 'CBR:cbsres-list' )
        context['return_url']=self.request.GET['return_url']
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbrerpdDetailView( UpdateView ):
    form_class=CbrerpdForm
    template_name='cbrerpd/detail.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
            bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
            bCbrenct.save()
        aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = self.kwargs.get( 'idrerpe' ) ).first())
        aCbrenct.idusu = request.user.username
        aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.accion = 9
        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.save()
        return super().dispatch( request, *args, **kwargs )

    def get_object(self):
        idrerpd=self.kwargs.get( 'idrerpd' )
        return get_object_or_404( Cbrerpd, idrerpd=idrerpd )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Registro original del archivo del ERP'
        context['id']=self.kwargs.get( 'idrerpd' )
        context['nombre_id']='IDRERPD'
        context['idrenc']=self.kwargs.get( 'idrerpe' )
        context['list_url']=reverse_lazy( 'CBR:cbsres-list' )
        context['return_url']=self.request.GET['return_url']
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def cbtctaDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data={}
            idtcta=request.POST['idtcta']
            aCbtcta = Cbtcta.objects.get( idtcta=idtcta )
            diccionario = clienteYEmpresas(request)
            if aCbtcta.empresa in diccionario["empresas"] and aCbtcta.cliente == diccionario["cliente"]:
                
                #verifica que no haya registros posteriores
                if Cbrenc.objects.exclude(estado = "3").filter( codbco=aCbtcta.codbco,
                            nrocta=aCbtcta.nrocta,
                            empresa=aCbtcta.empresa,
                            ).exists():
                                data['error']="Existen meses posteriores cargados"
                                return JsonResponse( data, safe=False)
                else:
                    aCbtcta.delete()

        
        except Exception as e:
            print(e)
            data={}
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def cbtusuDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data={}
            idusu1=request.POST['idusu1']
            aCbtusu = Cbtusu.objects.get( idusu1=idusu1 )
            diccionario = clienteYEmpresas(request)
            aCbtusurequest = Cbtusu.objects.filter(idusu1 = request.user.username).first()
            if aCbtusu.cliente == diccionario["cliente"] and aCbtusurequest.tipousu == "S":
                
                #verifica que no haya registros posteriores
                if Cbrenc.objects.filter(idusucons=idusu1).exists() == False:
                    aCbtusu.delete()

        
        except Exception as e:
            print(e)
            data={}
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request


# ******************************************************************************************************************** #
# ********************
@login_required
def cbtempDelete(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            data={}
            idtemp=request.POST['idtemp']
            aCbtemp = Cbtemp.objects.get( idtemp=idtemp )
            diccionario = clienteYEmpresas(request)
            if aCbtemp.empresa in diccionario["empresas"] and aCbtemp.cliente == diccionario["cliente"]:
                
                #verifica que no haya registros Cargados
                if Cbrenc.objects.exclude(estado = "3").filter( 
                            empresa=aCbtemp.empresa,
                            ).exists():
                                data['error']="Existen meses cargados con esta empresa"
                                return JsonResponse( data, safe=False)
                else:
                    aCbtemp.delete()

        
        except Exception as e:
            print(e)
            data={}
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@csrf_exempt
def conciliarSaldos(request):
    if request.method == 'POST':
        chequearNoDobleConexion(request)
        try:
            idrenc=request.POST.get( 'idrenc' )
            try:
                estado=Cbrenc.objects.get( idrenc=idrenc ).estado
            except:
                estado = 1
            if (int(estado) < 2):
                existe=Cbsres.objects.filter( idrenc=idrenc ).count()
                sobreescribir=request.POST['sobreescribir']
                #Define si es posible conciliar(es primera vez, se acepto la sobreescritura y el estado no es conciliado ni eliminado)
                if ((sobreescribir == 'true') or (existe == 0)):

                    data={}
                    #Define los objetos a cargar y los saldos iniciales
                    bcoDataSet=Cbrbcod.objects.filter( idrbcoe=idrenc ).order_by( 'fechatra', 'horatra' )
                    erpDataSet=Cbrerpd.objects.filter( idrerpe=idrenc ).order_by( 'fechatra')


                    rowInicialbco=Cbrbcod.objects.filter( idrbcoe=idrenc).order_by( 'fechatra', 'horatra' ).first()

                    rowInicialerp=Cbrerpd.objects.filter( idrerpe=idrenc ).order_by( 'fechatra').first()

                    currentDay=rowInicialbco.fechatra
                    Cbsres.objects.filter( idrenc=idrenc ).delete()
                    dia = 1
                    color = 0
                    cambio = False
                    while dia < 32:
                        #Para cada dia carga los registros del banco en orden, calculando los saldos
                        fechatrabco = None
                        for vwRow in bcoDataSet:
                            if vwRow.fechatra.day == dia:
                                fechatrabco=vwRow.fechatra
                                if (vwRow.fechatra is None):
                                    if (currentDay != vwRow.fechatra):
                                        currentDay=vwRow.fechatra

                                insCbsres=Cbsres(
                                    idrenc=Cbrenc.objects.get( idrenc=idrenc ),
                                    cliente=Cbrenc.objects.get( idrenc=idrenc).cliente,
                                    empresa=Cbrenc.objects.get( idrenc=idrenc).empresa,
                                    saldobco=vwRow.saldo,
                                    idrbcod=vwRow.idrbcod,
                                    oficina=vwRow.oficina,
                                    desctra=vwRow.desctra,
                                    reftra=vwRow.reftra,
                                    codtra=vwRow.codtra,
                                    #isconciliado=vwRow.isconciliado,
                                    # estado=vwRow.esta,
                                    # historial=vwRow.,
                                    # --------------------
                                    fechatrabco=vwRow.fechatra,
                                    horatrabco=vwRow.horatra,
                                    debebco=vwRow.debe,
                                    haberbco=vwRow.haber,
                                    codbco=Cbrenc.objects.get( idrenc=idrenc).codbco,
                                    nrocta=Cbrenc.objects.get( idrenc=idrenc).nrocta,
                                    ano = Cbrenc.objects.get( idrenc=idrenc).ano,
                                    mes = Cbrenc.objects.get( idrenc=idrenc).mes,
                                    estadobco = 0,
                                    codtcobco = " ",
                                    pautado = color
                                    # --------------------
                                )
                                insCbsres.fechact=dt.datetime.now(tz=timezone.utc)+huso
                                insCbsres.idusualt=request.user.username
                                insCbsres.save()
                                cambio = True
                        #for vwRow in erpDataSet:
                        #    #Para cada dia carga los registros del erp que coincilian
                        #    if vwRow.fechatra.day == dia:
                        #            if Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).exists():
                        #                insCbsres=Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).first()
                        #                Unir(vwRow,insCbsres,idrenc,color)
                        #                erpDataSet = erpDataSet.exclude(idrerpd=vwRow.idrerpd)
                        for vwRow in erpDataSet:
                            #Para cada dia carga los registros del erp que no concilian en  orden de cercania
                            if vwRow.fechatra.day == dia:
                                if fechatrabco != 0 and Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco ).exists():
                                    insCbsres=Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco ).first()
                        #            insCbsres = Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco).annotate(abs_diff=Func(F('debebco') - vwRow.haber + F('haberbco') - vwRow.debe, function='ABS')).order_by('abs_diff').first()
                                else:
                                    try:
                                        insCbsres=Cbsres(idrenc=Cbrenc.objects.get( idrenc=idrenc ), pautado = color)
                                    except:
                                        insCbsres=Cbsres(idrenc=Cbrenc.objects.get( idrenc=idrenc ))
                                Unir(vwRow,insCbsres,idrenc,color)
                        dia = dia +1
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
                            
                            saldoacumesbco=float(aCbsres.saldobco or 0)
                            saldoacumdiabco=float(aCbsres.haberbco or 0)-float(aCbsres.debebco or 0)
                            saldoacumeserp=float(aCbsres.saldoerp or 0)
                            saldoacumdiaerp=float(aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
                            saldodiferencia= saldoacumesbco - saldoacumeserp
                            diabcoant=aCbsres.fechatrabco
                            diaerpant=aCbsres.fechatraerp     
                            aCbsres.saldodiferencia = saldodiferencia                     
                            aCbsres.saldoacumesbco=saldoacumesbco
                            aCbsres.saldoacumdiabco=saldoacumdiabco
                            aCbsres.saldoacumeserp=saldoacumeserp
                            aCbsres.saldoacumdiaerp=saldoacumdiaerp
                            aCbsres.fechact=dt.datetime.now(tz=timezone.utc)+huso
                            aCbsres.idusualt=request.user.username
                            aCbsres.save()
                        else:
                            diabco=aCbsres.fechatrabco
                            diaerp=aCbsres.fechatraerp    
                            saldoacumesbco= saldoacumesbco + float(aCbsres.haberbco or 0)- float(aCbsres.debebco or 0)
                            if diabco == diabcoant or diaerp ==diaerpant:
                                saldoacumdiabco=saldoacumdiabco + float(aCbsres.haberbco or 0)-float(aCbsres.debebco or 0)
                                saldoacumdiaerp=float(saldoacumdiaerp or 0)+float(aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
                            else:
                                saldoacumdiabco = float(aCbsres.haberbco or 0)-float(aCbsres.debebco or 0)
                                saldoacumdiaerp=float(aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)
                            saldoacumeserp= saldoacumeserp + float(aCbsres.debeerp or 0)-float(aCbsres.habererp or 0)  
                            saldodiferencia= saldoacumesbco - saldoacumeserp
                            aCbsres.saldoacumesbco=saldoacumesbco
                            aCbsres.saldoacumdiabco=saldoacumdiabco
                            aCbsres.saldoacumeserp=saldoacumeserp
                            aCbsres.saldoacumdiaerp=saldoacumdiaerp
                            aCbsres.saldodiferencia= saldodiferencia
                            diabcoant=diabco
                            diaerpant=diaerp
                            aCbsres.fechact=dt.datetime.now(tz=timezone.utc)+huso
                            aCbsres.idusualt=request.user.username
                            aCbsres.save()
                    n = 0
                    while n < Cbsres.objects.filter(idrenc=idrenc).count():
                        aCbsres = Cbsres.objects.filter(idrenc=idrenc).order_by('idsres')[n]
                        if Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco,debebco=aCbsres.debebco,haberbco=aCbsres.haberbco).count() == 1:
                            if Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco,debeerp=aCbsres.haberbco,habererp=aCbsres.debebco).count() == 1:
                                bCbsres = Cbsres.objects.filter(idrenc=idrenc, fechatrabco=aCbsres.fechatrabco,debeerp=aCbsres.haberbco,habererp=aCbsres.debebco).first()
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

                    CbrencUpd=Cbrenc.objects.get( idrenc=idrenc )
                    CbrencUpd.fechacons=dt.datetime.now(tz=timezone.utc)+huso
                    CbrencUpd.idusucons=request.user.username
                    CbrencUpd.save()
                    if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                        bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                        bCbrenct.save()
                    aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
                    aCbrenct.idusu = request.user.username
                    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                    aCbrenct.accion = 2
                    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                    aCbrenct.save()
                    data={"idrenc": idrenc}
                else:
                    hist=Cbrenc.objects.get( idrenc=idrenc )
                    data={"existe_info": "¿Desea sobreescribir la conciliación anterior?"}
                    data['fechacons']=hist.fechacons.strftime( '%d-%m-%Y %H:%M:%S' )
                    data['idusucons']=hist.idusucons

            else:
                data={"info": "La conciliación ya fue cerrada"}
        except Exception as e:
            data={}
            print(e)
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
def Unir(vwRow,insCbsres,idrenc,color):
    #sistema que une el cbsres con banco cargado con un registro del cbrerpd

    insCbsres.idrerpd=vwRow.idrerpd

    insCbsres.saldoerp=vwRow.saldo

        # estado=vwRow.esta,
        # historial=vwRow.,
        # --------------------
    insCbsres.fechatraerp=vwRow.fechatra
    insCbsres.debeerp=vwRow.debe
    insCbsres.habererp=vwRow.haber
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
                idrenc= Cbrenc.objects.filter(idrenc = idrenc).first()
                if Cbwres.objects.filter(idsres=int(idsres)).exists():
                    aCbsres = Cbwres.objects.filter(idsres=int(idsres)).first()
                else:
                    aCbsres = Cbsres.objects.filter(idsres=int(idsres)).first()
                estadobco= fila["estadobco"]
                estadoerp= fila["estadoerp"]
                cliente= aCbsres.cliente
                empresa= aCbsres.empresa
                codbco= aCbsres.codbco
                nrocta= aCbsres.nrocta
                ano= aCbsres.ano
                mes= aCbsres.mes
                fechatrabco= aCbsres.fechatrabco
                horatrabco= aCbsres.horatrabco
                pautado= aCbsres.pautado
                debebco= aCbsres.debebco
                haberbco= aCbsres.haberbco
                saldobco= aCbsres.saldobco
                saldoacumesbco= aCbsres.saldoacumesbco
                saldoacumdiabco= aCbsres.saldoacumdiabco
                oficina= aCbsres.oficina
                desctra= aCbsres.desctra
                reftra= aCbsres.reftra
                codtra= aCbsres.codtra
                idrbcod= aCbsres.idrbcod
                nrotraerp= aCbsres.nrotraerp
                fechatraerp= aCbsres.fechatraerp
                nrocomperp= aCbsres.nrocomperp
                auxerp= aCbsres.auxerp
                referp= aCbsres.referp
                glosaerp= aCbsres.glosaerp
                saldoerp= aCbsres.saldoerp
                fechaconerp= aCbsres.fechaconerp
                idrerpd= aCbsres.idrerpd   
                Cbwres.objects.filter( idsres = idsres ).delete()
                aCbwres = Cbwres(idrbcodl=idrbcodl,idrerpdl=idrerpdl,idsres=idsres, idrenc= idrenc, cliente=cliente, empresa=empresa, codbco=codbco, nrocta=nrocta, ano=ano, mes=mes, fechatrabco=fechatrabco, horatrabco=horatrabco, debebco=debebco, haberbco=haberbco, saldobco=saldobco, saldoacumesbco=saldoacumesbco, saldoacumdiabco=saldoacumdiabco, oficina=oficina, desctra=desctra, reftra=reftra, codtra=codtra, idrbcod=idrbcod,nrotraerp=nrotraerp,fechatraerp=fechatraerp,nrocomperp=nrocomperp, auxerp=auxerp, referp=referp,glosaerp=glosaerp,debeerp=debeerp,habererp=habererp, saldoerp=saldoerp, saldoacumeserp=saldoacumeserp, saldoacumdiaerp=saldoacumdiaerp,fechaconerp=fechaconerp,idrerpd=idrerpd, saldodiferencia=saldodiferencia, estadobco=estadobco,estadoerp=estadoerp, historial=historial, codtcobco=codtcobco, codtcoerp=codtcoerp)
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
            idrenc=request.POST.get( 'idrenc' )
            CbrencUpd=Cbrenc.objects.get( idrenc=idrenc )
            diccionario = clienteYEmpresas(request)
            if CbrencUpd.empresa in diccionario["empresas"] and CbrencUpd.cliente == diccionario["cliente"]:
                CbrencUpd.estado=2
                CbrencUpd.save()
                data={"idrenc": idrenc}
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 2
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()

        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
@login_required
def getanomes(request):
    chequearNoDobleConexion(request)
    codbco=request.GET.get( 'banco' )
    nrocta=request.GET.get( 'cuenta' )
    try:
        maxAno=Cbrenc.objects.exclude(estado = "3").filter( codbco=codbco, nrocta=nrocta ).aggregate( Max( 'ano' ) )
        maxAno=maxAno['ano__max']
        if maxAno is None:
            aCbtcta=Cbtcta.objects.filter( codbco=codbco, nrocta=nrocta ).first()
            if aCbtcta is None:
                data={'ano': 0, 'mes': 0}
            maxAno = aCbtcta.ano
            maxMes = aCbtcta.mes
            if maxMes < 12:
                data={'ano': maxAno, 'mes': maxMes + 1}
            else:
                data={'ano': maxAno + 1, 'mes': 1}            
        else:
            maxMes=Cbrenc.objects.exclude(estado = "3").filter( codbco=codbco, nrocta=nrocta, ano=maxAno ).aggregate(
                Max( 'mes' ) )
            maxMes=maxMes['mes__max']
            if maxMes < 12:
                data={'ano': maxAno, 'mes': maxMes + 1}
            else:
                data={'ano': maxAno + 1, 'mes': 1}
    finally:
        return JsonResponse( data )


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

@login_required
def getguardado(request):
    chequearNoDobleConexion(request)
    data={"guardado":"si"} 
    idrenc=request.GET.get( 'idrenc' )
    if Cbwres.objects.filter(idrenc=idrenc,debeerp=0,habererp=0).exists():
        alertaGuardado = str(Cbwres.objects.filter(idrenc=idrenc,debeerp=0,habererp=0).first().idsres)
        data={"guardado": "Debe y Haber no pueden ser 0 en IDSRES = " + alertaGuardado}
    else:
        for registro in Cbwres.objects.filter(idrenc=idrenc).all():
            aCbsres = Cbsres.objects.filter(idsres = registro.idsres).first()
            if (aCbsres.debeerp != registro.debeerp or aCbsres.habererp != registro.habererp) and (registro.codtcoerp == " " or registro.codtcoerp == None):
                data={"guardado": "Explique la modificacion en IDSRES =" + str(registro.idsres)}
    return JsonResponse( data )



# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


class DetalleBcoListView( ListView ):
    model=Cbrbcod
    template_name='cbrbcod/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrbcoe=request.POST['idrbcoe']

            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbrbcod.objects.filter( idrbcoe=idrbcoe ):
                    item=i.toJSON()
                    item['position']=position
                    item['ID']=position
                    data.append( item )
                    position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF06", idrenc = Cbrenc.objects.filter(idrenc = idrbcoe).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
            print(e)
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        idrenc=self.request.GET['idrbcoe']
        context['title']='Detalle de carga del archivo de Banco'
        context['codigo']='CBF06'
        context['idrbcoe']=self.request.GET.get( 'idrbcoe' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        aCbrenc= Cbrenc.objects.filter(idrenc=idrenc).first()
        context['imagen']=False
        if aCbrenc.archivoimg != "":
            context['imagen']=True
        return context


# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class DetalleErpListView( ListView ):
    model=Cbrerpd
    template_name='cbrerpd/list.html'
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrerpe=request.POST['idrerpe']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbrerpd.objects.filter( idrerpe=idrerpe ):
                    item=i.toJSON()
                    item['position']=position
                    item['ID']=position
                    # item['idrenc']=i.idrenc
                    data.append( item )
                    position+=1                
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF07", idrenc = Cbrenc.objects.filter(idrenc = idrerpe).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Detalle de carga del archivo del ERP'
        context['codigo']='CBF07'
        context['idrerpe']=self.request.GET.get( 'idrerpe' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class DetalleTiempoListView( ListView ):
    model=Cbrenct
    template_name='cbrenct/list.html'
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                position=1
                tiempoacum = dt.timedelta(0)
                largo = Cbrenct.objects.filter( idrenc=idrenc ).count()
                for i in Cbrenct.objects.filter( idrenc=idrenc )[:largo-1]:
                    item=i.toJSON()
                    item['position']=position
                    item['ID']=position
                    try:
                        tiempoacum = tiempoacum + item['tiempodif']
                    except:
                        pass
                    item['tiempodif'] = str(i.tiempodif)[:-7]
                    item['tiempodifacum'] = str(tiempoacum)[:-7]
                    # item['idrenc']=i.idrenc
                    data.append( item )
                    position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF05", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Log de Tiempo'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['codigo']='CBF05'
        idrenc=self.request.GET['idrenc']
        tiempototal = dt.timedelta(0)
        for i in Cbrenct.objects.filter( idrenc=idrenc ):
            try:
                tiempototal += i.tiempodif
            except:
                pass
        tiempototal = str(tiempototal)[:-7].replace("day","día")
        context["tiempototal"]=tiempototal
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class DetalleLogListView( ListView ):
    model=Cbrencl
    template_name='cbrencl/list.html'
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbrencl.objects.filter( idrenc=idrenc ):
                    item=i.toJSON()
                    item['position']=position
                    item['ID']=position
                    # item['idrenc']=i.idrenc
                    data.append( item )
                    position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF04", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
                    
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Log'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['codigo']='CBF04'
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


class ConciliacionDeleteForm( CreateView ):
    model=Cbrencl
    form_class=CbrencDeleteForm
    def get_initial(self):
        try:
            idrenc=self.request.GET.get( 'idrenc' )
            return {'idrenc': idrenc}
        except:
            pass
    
    template_name='cbrenc/delete-form.html'

    success_url=reverse_lazy( 'CBR:cbrenc-list' )
    url_redirect=success_url
    def get_object(self):
        idrenc=self.kwargs.get( 'idrenc' )
        return get_object_or_404( Cbrenc, idrenc=idrenc )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            
            idrenc=request.POST['idrenc']
            aCbrenc = Cbrenc.objects.get( idrenc=idrenc )
            #verifica que no haya registros posteriores
            if Cbrenc.objects.exclude(estado = "3").filter( codbco=aCbrenc.codbco,
                        nrocta=aCbrenc.nrocta,
                        ano__startswith = aCbrenc.ano+1,
                        cliente=aCbrenc.cliente,
                        empresa=aCbrenc.empresa,
                        ).exists() or Cbrenc.objects.exclude(estado = "3").filter( codbco=aCbrenc.codbco,
                        nrocta=aCbrenc.nrocta,
                        ano = aCbrenc.ano,
                        mes__startswith = aCbrenc.mes+1,
                        cliente=aCbrenc.cliente,
                        empresa=aCbrenc.empresa,
                        ).exists():
                            data['error']="Existen meses posteriores cargados"
                            return JsonResponse( data, safe=False)
            if Cbwres.objects.filter(idrenc=idrenc).exists():
                data['error']="No es posible eliminar, el folio se encuentra en uso"
                return JsonResponse( data, safe=False)


            # CREATE
            if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                bCbrenct.save()
            aCbrenct = Cbrenct(formulario = "CBF10", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
            aCbrenct.idusu = request.user.username
            aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
            aCbrenct.accion = 7
            aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
            aCbrenct.save()
            form=self.get_form()
            self.Cbrencl=form.save()
            if self.Cbrencl != {'error': {'glosa': ['Este campo es obligatorio.']}}:


                self.Cbrencl.status = 3
                self.Cbrencl.saldobco = aCbrenc.saldobco
                self.Cbrencl.saldoerp = aCbrenc.saldoerp
                self.Cbrencl.difbcoerp = aCbrenc.difbcoerp
                self.Cbrencl.idusu = request.user.username
                self.Cbrencl.fechact=dt.datetime.now(tz=timezone.utc)+huso
                self.Cbrencl.save()
                aCbrenc.estado = 3
                aCbrenc.save()




        except Exception as e:
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='eliminar'
        context['codigo']='CBF10'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

def verificarGuardado(request):
    return render(request, "cbrenc/confirmation-form.html")
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def verificarCarga(request):
    aCbrenc = Cbrenc.objects.order_by('-idrenc').first()
    idrenc = aCbrenc.idrenc
    ano=aCbrenc.ano
    mes=aCbrenc.mes
    nrocta = aCbrenc.nrocta
    empresa = aCbrenc.empresa
    codbco = aCbrenc.codbco
    #verifica que el registro anterior sea del mes y año correspondiente(o del siguiente a cbttca)
    if mes == 1:
        mesanterior = 12
        anoanterior = int(ano)-1
    else:
        mesanterior = int(mes) -1
        anoanterior = int(ano)
    aCberencAnterior =Cbrenc.objects.filter( codbco=codbco,
                        nrocta=nrocta,
                        ano=anoanterior,
                        mes=mesanterior,
                        #cliente=cliente,
                        empresa=empresa,
                        ).first()
    if aCberencAnterior == None:
        aCbtcta = Cbtcta.objects.filter(codbco=codbco, nrocta=nrocta, empresa=empresa).first()
        saldobcoanterior = aCbtcta.saldoinibco
        saldoerpanterior = aCbtcta.saldoinierp
    else:
        saldobcoanterior = aCberencAnterior.saldobco
        saldoerpanterior = aCberencAnterior.saldoerp
    primerRegistroBco = Cbrbcod.objects.filter(idrbcoe=idrenc).order_by("idrbcod").order_by("fechatra").first()
    saldobco = primerRegistroBco.saldo + primerRegistroBco.debe - primerRegistroBco.haber
    primerRegistroErp = Cbrerpd.objects.filter(idrerpe=idrenc).order_by("idrerpd").order_by("fechatra").first()
    saldoerp = primerRegistroErp.saldo - primerRegistroErp.debe + primerRegistroErp.haber
    if saldoerp == saldoerpanterior and saldobco == saldobcoanterior:
        return redirect("../../")
    errorBco = False
    errorERP = False
    if saldoerp != saldoerpanterior:
        errorERP = True
    if saldobco != saldobcoanterior:
        errorBco = True
    saldoerp = "$"+'{:,}'.format(float(saldoerp))
    saldobco = "$"+'{:,}'.format(float(saldobco))
    saldoerpanterior = "$"+'{:,}'.format(float(saldoerpanterior))
    saldobcoanterior = "$"+'{:,}'.format(float(saldobcoanterior))
    return render(request, "cbrenc/confirmarcarga.html",{"saldobcoanterior":saldobcoanterior,  "saldoerpanterior": saldoerpanterior, "saldobco": saldobco, "saldoerp":saldoerp, "errorBco":errorBco, "errorERP":errorERP})

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def eliminarCarga(request):
    aCbrenc = Cbrenc.objects.order_by('-idrenc').first()
    idrenc = aCbrenc.idrenc
    Cbrbod.objects.filter(idrenc = idrenc).delete()
    Cbrgal.objects.filter(idrenc = idrenc).delete()
    Cbrbcod.objects.filter(idrbcoe=idrenc).delete()
    Cbrerpd.objects.filter(idrerpe=idrenc).delete()
    Cbrbcoe.objects.filter(idrenc=idrenc).delete()
    Cbrerpe.objects.filter(idrenc=idrenc).delete()
    Cbrencl.objects.filter(idrenc=idrenc).delete()
    Cbrenct.objects.filter(idrenc=idrenc).delete()
    Cbrenc.objects.filter(idrenc=idrenc).delete()
    return redirect("../../")
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def conservarGuardado(request):
    idrenca = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
        bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenca ).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
    aCbrenct.accion = 4
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
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
            aCbsresc = Cbsresc(idsres = idsres, codtco = dato[0], debebco = dato[4], haberbco = dato[5], saldoacumesbco = dato[6], saldoacumeserp = dato[7])
            aCbsresc.save()
        if dato[1] != "":
            aCbsresc = Cbsresc(idsres = idsres, codtco = dato[1], debeerp = dato[2], habererp = dato[3], saldoacumesbco = dato[6], saldoacumeserp = dato[7])
            aCbsresc.save()
    try:
        aCbsres = Cbsres.objects.filter(idrenc=idrenca).order_by('-idsres').first()
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
        aCbrenc.saldobco = tiposDeConciliacion["saldobcototal"]
        aCbrenc.saldoerp= tiposDeConciliacion["saldoerptotal"]
        aCbrenc.difbcoerp = tiposDeConciliacion["saldodiferenciatotal"]
        aCbrenc.save()
        aCbrencl = Cbrencl(
            idrenc = Cbrenc.objects.filter(idrenc=idrenca).first(),
            status = 1,
            saldobco = Cbrenc.objects.filter(idrenc=idrenca).first().saldobco,
            saldoerp = aCbsres.saldoacumeserp+aCbsres.debeerp-aCbsres.habererp,
            difbcoerp = Cbrenc.objects.filter(idrenc=idrenca).first().saldobco - aCbsres.saldoacumeserp+aCbsres.debeerp-aCbsres.habererp,
            idusu = request.user.username)
        aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)+huso
        aCbrencl.save(aCbrencl)
        if Cbsres.objects.filter(idrenc=idrenca, idrbcodl = 0).exists() or Cbsres.objects.filter(idrenc=idrenca, idrerpdl = 0).exists():
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

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


def eliminarGuardado(request):
    idrenc = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
        bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
    aCbrenct.accion = 10
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
    aCbrenct.save()
    
    Cbwres.objects.filter(idrenc=idrenc).delete()


    return redirect("../../cbsres/?idrenc="+idrenc)

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class DetalleErroresBodListView(ListView):
    model=Cbrbode
    template_name= 'cbrbode/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            data=[]
            position=1
            for i in Cbrbode.objects.all():
                detalle = i.idrbod
                item=i.toJSON()
                item['diatra'] = detalle.diatra
                item['oficina'] = detalle.oficina
                item['desctra'] = detalle.desctra
                item['debe'] = detalle.debe
                item['haber'] = detalle.haber
                item['saldo'] = detalle.saldo
                item['position']=position
                aCbterr = Cbterr.objects.filter(coderr = i.coderr).first()
                item['coderr']= aCbterr.descerr
                item['ID']=position
                data.append( item )
                position+=1
        except Exception as e:
            print(e)
        return JsonResponse( data, safe=False )
    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Detalle de Errores Banco'
        context['codigo']='CBF10'
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


class DetalleErroresGalListView(ListView):
    model=Cbrgale
    template_name= 'cbrgale/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            action=request.POST['action']
            data=[]
            position=1
            for i in Cbrgale.objects.all():
                detalle = i.idrgal
                item=i.toJSON()
                item['aux'] = detalle.aux
                item['fechatra'] = detalle.fechatra
                item['nrocomp'] = detalle.nrocomp
                item['ref'] = detalle.ref
                item['glosa'] = detalle.glosa
                item['debe'] = detalle.debe
                item['haber'] = detalle.haber
                item['saldo'] = detalle.saldo
                item['fechacon'] = detalle.fechacon
                item['position']=position
                aCbterr = Cbterr.objects.filter(coderr = i.coderr).first()
                item['coderr']= aCbterr.descerr
                item['fechact']= detalle.fechact
                item['ID']=position
                data.append( item )
                position+=1
        except Exception as e:
            print(e)
        return JsonResponse( data, safe=False )
    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Detalle de Errores ERP'
        context['codigo']='CBF11'
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


@login_required
def getTiposDeConciliacion(request):
    chequearNoDobleConexion(request)
    idrenc = request.GET["idrenc"]
    data = {"debebcototal":0, "haberbcototal":0,"saldobcototal":0,"debeerptotal":0,"habererptotal":0, "saldoerptotal":0,"saldodiferenciatotal":0 }
    yaTomadas = []
    n = 0
    m = 0
    #calcula que codigos suman a cada lado
    listadoSumaDebeBco = []
    listadoSumaHaberBco = []
    listadoSumaDebeErp= []
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
    #Listado de quienes tienen codigo para la tabla de respectiva
    data["listado"] = []
    
    #calcula primero las del cbwres y si no existen las del cbsres
    
    for registro in Cbsres.objects.filter(idrenc=idrenc).order_by("idsres").all():
        if Cbwres.objects.filter(idsres = registro.idsres).exists():
            registroAnalizado = Cbwres.objects.filter(idsres = registro.idsres).first()
        else:
            registroAnalizado = registro

        try:
            data["debeerptotal"] = registroAnalizado.debeerp + data["debeerptotal"]        
        except:
            pass
        try:
            data["habererptotal"] = registroAnalizado.habererp + data["habererptotal"]
        except:
            pass
        try:
            data["debebcototal"] = registroAnalizado.debebco + data["debebcototal"]
        except:
            pass
        try:
            data["haberbcototal"] = registroAnalizado.haberbco + data["haberbcototal"]
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
                data["debeerptotal"] = registroAnalizado.haberbco + data["debeerptotal"]
                data[str(registroAnalizado.idsres)] = [registroAnalizado.codtcobco,"", 0,0,registroAnalizado.haberbco,0,registroAnalizado.saldoacumesbco,registroAnalizado.saldoacumeserp]
                data["listado"].append(registroAnalizado.idsres)
                saldoextraerp = saldoextraerp + registroAnalizado.haberbco
            except Exception as e:
                pass
        elif registroAnalizado.codtcobco in listadoSumaHaberErp:
            try:
                data["habererptotal"] = registroAnalizado.debebco + data["habererptotal"]
                data["listado"].append(registroAnalizado.idsres)
                data[str(registroAnalizado.idsres)] = [registroAnalizado.codtcobco,"", 0,0,0,registroAnalizado.debebco,registroAnalizado.saldoacumesbco,registroAnalizado.saldoacumeserp]
                saldoextraerp = saldoextraerp - registroAnalizado.debebco
            except Exception as e:
                pass
        if registroAnalizado.codtcoerp in listadoSumaDebeBco:
            try:
                data["debebcototal"] = registroAnalizado.habererp + data["debebcototal"]
                data["listado"].append(registroAnalizado.idsres)
                try:
                    data[str(registroAnalizado.idsres)][1] = registroAnalizado.codtcoerp
                    data[str(registroAnalizado.idsres)][2] = registroAnalizado.habererp
                    data[str(registroAnalizado.idsres)][6] = registroAnalizado.saldoacumesbco
                    data[str(registroAnalizado.idsres)][7] = registroAnalizado.saldoacumeserp
                except:
                    data[str(registroAnalizado.idsres)] = ["",registroAnalizado.codtcoerp, registroAnalizado.habererp,0,0,0,registroAnalizado.saldoacumesbco,registroAnalizado.saldoacumeserp]
                saldoextrabco = saldoextrabco + registroAnalizado.habererp
            except:
                pass
        elif registroAnalizado.codtcoerp in listadoSumaHaberBco:
            try:
                data["haberbcototal"] = registroAnalizado.debeerp + data["haberbcototal"]
                data["listado"].append(registroAnalizado.idsres)
                try:
                    data[str(registroAnalizado.idsres)][1] = registroAnalizado.codtcoerp
                    data[str(registroAnalizado.idsres)][3] = registroAnalizado.debeerp
                    data[str(registroAnalizado.idsres)][6] = registroAnalizado.saldoacumesbco
                    data[str(registroAnalizado.idsres)][7] = registroAnalizado.saldoacumeserp
                except:
                    data[str(registroAnalizado.idsres)] = ["",registroAnalizado.codtcoerp, 0,registroAnalizado.debeerp,0,0,registroAnalizado.saldoacumesbco,registroAnalizado.saldoacumeserp]
                saldoextrabco = saldoextrabco + registroAnalizado.debeerp
            except Exception as e:
                pass
    data["saldobcototal"] = data["saldobcototal"] + saldoextrabco
    data["saldoerptotal"] = data["saldoerptotal"] + saldoextraerp
    data["saldodiferenciatotal"] = data["saldobcototal"] - data["saldoerptotal"]

    return JsonResponse( data )



# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class DetalleTiposDeConciliacion( ListView ):
    model=Cbttco
    template_name='cbttco/list.html'
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            idrenc=request.POST['idrenc']
            data=[]
            data2=[]
            position=1
            listadoSumaDebeBco = []
            listadoSumaHaberBco = []
            listadoSumaDebeErp= []
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
                    
            #calcula primero las del cbwres y si no existen las del cbsres
            for registro in Cbsres.objects.filter(idrenc=idrenc).order_by("idsres").all():
                
                if Cbwres.objects.filter(idsres = registro.idsres).exists():
                    registroAnalizado = Cbwres.objects.filter(idsres = registro.idsres).first()
                else:
                    registroAnalizado = registro
                saldoBco = registroAnalizado.saldoacumesbco
                saldoErp = registroAnalizado.saldoacumeserp
                
                if registroAnalizado.codtcobco in listadoSumaDebeErp:
                    try:
                        datos[registroAnalizado.codtcobco]=["debe", registroAnalizado.haberbco + datos[registroAnalizado.codtcobco][1]]
                    except:
                        datos[registroAnalizado.codtcobco]=["debe", registroAnalizado.haberbco]
                elif registroAnalizado.codtcobco in listadoSumaHaberErp:
                    try:
                        datos[registroAnalizado.codtcobco]=["haber", registroAnalizado.debebco + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcobco]=["haber", registroAnalizado.debebco]
                if registroAnalizado.codtcoerp in listadoSumaDebeBco:
                    try:
                        datos[registroAnalizado.codtcoerp]=["debe", registroAnalizado.habererp + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcoerp]=["debe", registroAnalizado.habererp]
                elif registroAnalizado.codtcoerp in listadoSumaHaberBco:
                    try:
                        datos[registroAnalizado.codtcoerp]=["haber", registroAnalizado.debeerp + datos[registroAnalizado.codtcoerp][1]]
                    except Exception as e:
                        datos[registroAnalizado.codtcoerp]=["haber", registroAnalizado.debeerp]
                if registroAnalizado.codtcobco in listadoSumaDebeErpNoSaldo:
                    try:
                        datos[registroAnalizado.codtcobco]=["debeNoSaldo", registroAnalizado.haberbco + datos[registroAnalizado.codtcobco][1]]
                    except:
                        datos[registroAnalizado.codtcobco]=["debeNoSaldo", registroAnalizado.haberbco]
                elif registroAnalizado.codtcobco in listadoSumaHaberErpNoSaldo:
                    try:
                        datos[registroAnalizado.codtcobco]=["haberNoSaldo", registroAnalizado.debebco + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcobco]=["haberNoSaldo", registroAnalizado.debebco]
                if registroAnalizado.codtcoerp in listadoSumaDebeBcoNoSaldo:
                    try:
                        datos[registroAnalizado.codtcoerp]=["debeNoSaldo", registroAnalizado.habererp + datos[registroAnalizado.codtcoerp][1]]
                    except:
                        datos[registroAnalizado.codtcoerp]=["debeNoSaldo", registroAnalizado.habererp]
                elif registroAnalizado.codtcoerp in listadoSumaHaberBcoNoSaldo:
                    try:
                        datos[registroAnalizado.codtcoerp]=["haberNoSaldo", registroAnalizado.debeerp + datos[registroAnalizado.codtcoerp][1]]
                    except Exception as e:
                        datos[registroAnalizado.codtcoerp]=["haberNoSaldo", registroAnalizado.debeerp]

            for i in Cbttco.objects.order_by("ordtco").order_by("-indsuma").all():
                item=i.toJSON()
                item['position']=position
                item['ID']=position
                item["debe"] = 0
                item["haber"] = 0
                item['indsum'] = True
                try:
                    if datos[i.codtco][0]=="debe":
                        if i.erpbco==1:
                            saldoBco -= datos[i.codtco][1]
                            item["saldoacumulado"] = saldoBco
                        else:
                            saldoErp += datos[i.codtco][1]
                            item["saldoacumulado"] = saldoErp
                        item["debe"] = item["debe"] + datos[i.codtco][1]
                    elif datos[i.codtco][0]=="haber":
                        if i.erpbco==1:
                            saldoBco += datos[i.codtco][1]
                            item["saldoacumulado"] = saldoBco
                        else:
                            saldoErp -= datos[i.codtco][1]
                            item["saldoacumulado"] = saldoErp
                        item["haber"] = item["haber"] + datos[i.codtco][1]
                    elif datos[i.codtco][0]=="debeNoSaldo":
                        item["debe"] = item["debe"] + datos[i.codtco][1]
                        item["indsum"] = False
                    elif datos[i.codtco][0]=="haberNoSaldo":
                        item["haber"] = item["haber"] + datos[i.codtco][1]
                        item["indsum"] = False
                except:
                    pass
                if i.erpbco==1:
                    item["saldoacumulado"] = saldoBco
                else:
                    item["saldoacumulado"] = saldoErp
                
                # item['idrenc']=i.idrenc
                data.append( item )
                position+=1
            try:
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF11", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
                aCbrenct.fechact = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.accion = 7
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
            except:
                pass
        except Exception as e:
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Tipos de Conciliacion'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['codigo']='CBF11'
        return context

class DescargarArchivoView(View):
    def get(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        idrenc = request.GET['idrenc']
        imgbco = Cbrenci.objects.filter(idrenc=idrenc).first().imgbco
        try:
            os.remove(str(Path(__file__).resolve().parent.parent)+ "/media/"+ 'temp/imagen.pdf')
        except:
            pass
        file = open(str(Path(__file__).resolve().parent.parent)+ "/media/"+ 'temp/imagen.pdf', 'wb')
        file.write(base64.b64decode(imgbco))
        file.close()
        wrapper = FileWrapper(open(str(Path(__file__).resolve().parent.parent)+ "/media/"+ 'temp/imagen.pdf', 'rb'))
        response = HttpResponse(wrapper, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + 'imagenbanco.pdf'
        return response

def getPais(codigo):
    idpais = codigo[0:2]
    aCbtpai = Cbtpai.objects.filter(codpai=idpais).first()
    return aCbtpai.despai

def getCliente(request, context):
    try:
        aCbtusu = Cbtusu.objects.filter(idusu1 = request.user.username).first()
        aCbtcli = Cbtcli.objects.filter(cliente = aCbtusu.cliente).first()
        context["cliente"]=aCbtcli.cliente + "-" + aCbtcli.descli
    except Exception as e:
        print(e)



# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class ListaUsuarioView( ListView ):
    model=Cbtusu
    template_name='cbtusu/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        if Cbtusu.objects.filter(idusu1 = request.user.username).first().tipousu == "S":
            position=1
            data=[]
            for i in Cbtusu.objects.all():
                item=i.toJSON()
                item['position']=position
                item["modificable"]=True
                if Cbrenc.objects.filter(idusucons=item["idusu1"]).exists():
                    item["modificable"]=False
                
                data.append( item )
                position+=1
            return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        context['title']='Usuarios'
        context['codigo']='CBF15'
        getCliente(self.request, context)
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['new_user_url'] = reverse_lazy( 'CBR:usuario-nuevo' )
        return context

#  ********************************************************************************************************************

class ListaEmpresaView( ListView ):
    model=Cbtemp
    template_name='cbtemp/list.html'

    # @method_decorator( csrf_exempt )
    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        diccionario = clienteYEmpresas(request)
        position=1
        data=[]
        for i in Cbtemp.objects.all():
            item=i.toJSON()
            if item['empresa'] in diccionario["empresas"] and item["cliente"] == diccionario["cliente"]:
                item['position']=position
                item['pais']=getPais(item['empresa'])
                data.append( item )
                position+=1
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        context['title']='Administracion de Empresas'
        context['codigo']='CBF14'
        getCliente(self.request, context)
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['new_empresa_url'] = reverse_lazy( 'CBR:empresa-nueva' )
        return context
#  ********************************************************************************************************************
@login_required
def resetPassword(request):
    usuario = request.GET.get("usuario")

    aCbtusu = Cbtusu.objects.filter(idusu1=usuario).first()
    aCbtusu.pasusu = True
    aCbtusu.save()
    return redirect("../")

def CbtusucGuardar(request):
    print(request)
    try:
        Cbtusuc.objects.filter(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu).delete()
        i = 0
        while i < 34:
            clave = 'cbtusuc['+str(i)+']'
            
            if request.POST[clave]=="true":
                aCbtusuc=Cbtusuc(codcol=i)
                aCbtusuc.fechact =dt.datetime.now(tz=timezone.utc)+huso
                aCbtusuc.idusu=request.user.username
                aCbtusuc.idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu
                aCbtusuc.save()
            i=i+1
    except Exception as e:
        print(e)
        pass
    return JsonResponse({})

class CbtusuCreateView( CreateView ):
    model=Cbtusu
    form_class=CbtusuForm
    template_name='cbtusu/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtusu-list' )
    url_redirect=success_url

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            
            idusu1=request.POST['idusu1']
            descusu=request.POST['descusu']
            tipusu=request.POST.get('tipousu')

            if Cbtusu.objects.filter(idusu1=idusu1).exists():
                data['error']="Nombre de Usuario Existente"
                return JsonResponse( data, safe=False)
            cliente = clienteYEmpresas(request)["cliente"]
            licencias = Cbtlic.objects.filter(cliente=cliente).first().nrousuario
            usuariosActivos = Cbtusu.objects.filter(actpas="A", cliente=cliente).count()
            if licencias <= usuariosActivos:
                data['error']="Máximo número de usuarios activos alcanzados"
                return JsonResponse( data, safe=False)
            # CREATE
            CbtusuNew=Cbtusu(idusu1=idusu1, descusu=descusu,actpas="A")
            if tipusu == "on":
                CbtusuNew.tipousu = "S"
            else:
                CbtusuNew.tipousu = ""
            CbtusuNew.pasusu = True
            CbtusuNew.fechact=dt.datetime.now(tz=timezone.utc)+huso
            CbtusuNew.idusu=request.user.username
            CbtusuNew.cliente = Cbtusu.objects.filter(idusu1 = request.user.username).first().cliente
            CbtusuNew.save()
            usuario = User(username = idusu1, password=make_password("ninguno"))
            usuario.save()
        except Exception as e:

            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['modificable']= True
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'

        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtusu-list' )
        return context


class CbtempCreateView( CreateView ):
    model=Cbtemp
    form_class=CbtempForm
    template_name='cbtemp/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbtemp-list' )
    url_redirect=success_url

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            cliente= diccionario["cliente"]
            empresa = request.POST["empresa"]
            desemp = request.POST["desemp"]
            actpas = request.POST["actpas"]
            if actpas == "on":
                actpas = "A"
            else:
                actpas = "P"
            try:
                getPais(empresa)
            except:
                try:
                    data={}
                    data["error"]="el código de país "+ empresa[0:2]+ " no existe."
                    return JsonResponse(data)
                except:
                    data={}
                    data["error"]="La Empresa debe tener más de dos digitos."
                    return JsonResponse(data)
            empresasMaximas = Cbtlic.objects.filter(cliente=diccionario["cliente"]).first().nroempresa
            empresasActivas = Cbtemp.objects.filter(cliente=diccionario["cliente"], actpas = "A").count()
            if empresasActivas >= empresasMaximas and actpas == "A":
                data={}
                data["error"]="Se alcanzó el limite máximo de empresas activas"
                return JsonResponse(data)
            aCbtusue=Cbtusue(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first(), actpas="A", empresa=empresa)            
            aCbtusue.idusu = request.user.username
            aCbtusue.fechact = dt.datetime.now(tz=timezone.utc)+huso
            aCbtusue.save()
            # CREATE
            aCbtemp = Cbtemp(empresa=empresa, desemp=desemp,actpas=actpas )
            aCbtemp.fechact=dt.datetime.now(tz=timezone.utc)+huso
            aCbtemp.idusu=request.user.username
            aCbtemp.cliente=diccionario["cliente"]
            aCbtemp.save()
        except Exception as e:
            data={}
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        getCliente(self.request, context)
        context['title']='Nueva Empresa'
        context['codigo']='CBF20'
        context['editable']=True
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtemp-list' )
        return context


def chequearNoDobleConexion(request):
    aCbsusu = Cbsusu.objects.filter(idusu1=request.user.username).order_by("corrusu").last()
    if request.session["iddesesion"] < aCbsusu.corrusu:
        logout(request)
        return redirect("/")


def cerrarOtraPestana(request):
    return render(request, "utils/cerrarotrapestana.html")

def clienteYEmpresas(request):
    aCbtusu = Cbtusu.objects.filter(idusu1 = request.user.username).first()
    empresasHabilitadas = []
    if aCbtusu.tipousu == "S":
        empresas = Cbtemp.objects.filter(cliente= aCbtusu.cliente).all()
        for empresa in empresas:
            empresasHabilitadas.append(empresa.empresa)
    else:
        for empresa in Cbtusue.objects.filter(idtusu=aCbtusu.idtusu).all():
            empresasHabilitadas.append(empresa.empresa)
    return{"cliente":aCbtusu.cliente, "empresas":empresasHabilitadas}

def getColumnas(request):
    n = 0
    columnas = {}
    while n < 33:
        if Cbtusuc.objects.filter(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu,codcol=n).exists():
            columnas[n]=True
        else:
            columnas[n]=False
        n = n+1
    print(request)
    print(request.POST)
    print(request.user.username)
    print(columnas)
    return JsonResponse(columnas)


class definirColumnas( CreateView ):
    model=Cbtusuc
    form_class=CbtusucForm
    template_name='cbtusuc/add-edit.html'

    success_url=reverse_lazy( 'CBR:cbrenc-list' )
    url_redirect=success_url

    def get_initial(self):

        diccionario = {}
        columnas = Cbtcol.objects.all()
        for columna in columnas:
            if columna.inddef == 1:
                diccionario[columna.descol]=True
            else:
                diccionario[columna.descol]=False
        return diccionario


    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )
    
    def post(self, request, *args, **kwargs):
        chequearNoDobleConexion(request)
        data={}
        try:
            #Lee las respuetas al formulario
            diccionario = clienteYEmpresas(request)
            columnas = Cbtcol.objects.all()
            resultado = {}
            print("sa")
            Cbtusuc.objects.filter(idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu).delete()
            print("pe")
            for columna in columnas:
                print("di")
                print(request.POST)
                print(columna.descol)
                print(request.POST.get(columna.descol))
                if request.POST.get(columna.descol)=="on":
                    aCbtusuc=Cbtusuc(codcol=columna.codcol)
                    aCbtusuc.fechact =dt.datetime.now(tz=timezone.utc)+huso
                    aCbtusuc.idusu=request.user.username
                    aCbtusuc.idtusu=Cbtusu.objects.filter(idusu1=request.user.username).first().idtusu
                    aCbtusuc.save()
            print("aca")
            print(resultado)
            # CREATE
            form=self.get_form()
            
            form.fechalt=dt.datetime.now(tz=timezone.utc)+huso
            form.idusu=request.user.username

            self.CbrencNew=form.save()
        except Exception as e:

            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        lista = []
        columnas = Cbtcol.objects.all()
        for columna in columnas:
            lista.append(columna.descol)
        #context=super().get_context_data( **kwargs )
        context={}
        context["columnas"]=lista
        getCliente(self.request, context)
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'
        context['action']='edit'
        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtcta-list' )
        return context
