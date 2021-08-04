from django.db.models.aggregates import Count
from CBR.models import Cbrbcoe, Cbrenc,Cbrenct, Cbrbcod, Cbrerpd, Cbrerpe, Cbtbco, Cbsres, Cbtcta, Cbrencl,Cbwres,Cbrenci,Cbttco,Cbterr
import ntpath
from django.views.generic import ListView, UpdateView, View, CreateView
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from CBR.forms import CbrencaForm, CbrbcodForm, CbrerpdForm, CbtctaForm, CbrencDeleteForm
from CBR.homologacion import *
import datetime as dt
import base64
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Func, F
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
import requests
huso = dt.timedelta(hours=0)


class CbrbcodView( View ):
    model=Cbrbcod
    form_class=CbrbcodForm
    template_name='cbrbcod/detail.html'

    def get_object(self, request):

        idrbcod=self.kwargs.get( 'idrbcod' )
        return get_object_or_404( Cbrbcod, idrbcod=idrbcod )

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )


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
        data={}
        try:
            #Lee las respuetas al formulario
            cliente= "PMA"
            empresa=request.POST['empresa']
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
                #Elimina el CBRENCI base por si hubo un error previo
                try:
                    Cbrenci.objects.filter(idrenc = 1005).delete()
                except:
                    pass
                #Homologa el Banco BOD, posteriormente debe verificar que es lo que se encuentra en request.POST.get( 'codbco') para saber que homologacion usar
                HomologacionBcoBOD(request, self.CbrencNew, data,saldobcoanterior )
                archivoerp=request.POST.get( 'archivoerp', None )
                try:
                    #Verifica la existencia de errores, si los hubiera elimina todas las bases, si no carga el erp
                    print( data['error'])
                    error=True
                except:
                    error=False
                #Homologa el ERP Gal, posteriormente debe verificar que es lo que se encuentra en request.POST.get( 'coderp') para saber que homologacion usar
                if error == False:
                    HomologacionErpGAL( request, self.CbrencNew, data, saldoerpanterior )
                try:
                    print( data['error'])
                    error=True
                except:
                    error=False
                if error == True:
                    Cbrbod.objects.filter(idrenc=self.CbrencNew.idrenc).delete()
                    Cbrgal.objects.filter(idrenc=self.CbrencNew.idrenc).delete()
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
                aCbrenct.accion = 1
                aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                aCbrenct.save()
                # Crea la imagen de banco correspondiente
                try:
                    aCbrenci = Cbrenci.objects.filter(imgbconame=self.CbrencNew.imgbcoroute).first() 
                    self.CbrencNew.imgbcoroute = str(self.CbrencNew.imgbcoroute)[:-4] + str(self.CbrencNew.idrenc) + ".pdf"
                    aCbrenci.imgbconame = str(self.CbrencNew.imgbcoroute)
                    aCbrenci.idrenc = self.CbrencNew.idrenc
                    aCbrenci.save()
                    Cbrenci.objects.filter(idrenc = 1005).delete()
                    self.CbrencNew.save()
                except:
                    pass
                

            else:
                if Cbrenc.objects.filter( codbco=codbco,
                                       nrocta=nrocta,
                                       ano=anoanterior,
                                       mes=mesanterior,
                                       #cliente=cliente,
                                       empresa=empresa,
                                       ).exists():
                    data['error']='El mes Anterior no está conciliado: (' \
                              + ' Cliente: ' + cliente \
                              + ' Empresa: ' + empresa \
                              + ' Banco: ' + codbco \
                              + ' Cuenta: ' + nrocta \
                              + ' Año: ' + str(anoanterior) \
                              + ' Mes: ' + str(mesanterior) + ')'
                else:
                    data['error']='El mes Anterior no existe: (' \
                              + ' Cliente: ' + cliente \
                              + ' Empresa: ' + empresa \
                              + ' Banco: ' + codbco \
                              + ' Cuenta: ' + nrocta \
                              + ' Año: ' + str(anoanterior) \
                              + ' Mes: ' + str(mesanterior) + ')'
        except Exception as e:
            data['error']=str( e )
            print(e)
            return JsonResponse( data )

        return JsonResponse( data )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
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
        data={}
        try:
            #Lee las respuetas al formulario

            empresa=request.POST['empresa']
            codbco=request.POST['codbco']
            nrocta=request.POST['nrocta']
            if Cbtcta.objects.filter(empresa=empresa,codbco=codbco,nrocta=nrocta).exists():
                data['error']="Cuenta Existente"
                return JsonResponse( data, safe=False)

            # CREATE
            form=self.get_form()
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
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'

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
        data={}
        try:
            #Lee las respuetas al formulario
            
            cliente= "PMA"
            idtcta=request.POST['idtcta']
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

            # CREATE
            form=self.get_form()
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
        context['title']='Nueva Cuenta'
        context['codigo']='CBF09'
        context['action']='edit'
        context['idtcta']=self.request.GET.get( 'idtcta' )
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbtcta-list' )
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
        # si no existe la base de datos de CBTTCO la crea, esto solo para pruebas, no mantener en produccion
        if Cbttco.objects.filter(codtco = "DPTR").exists() == False:
            aCbttco= Cbttco(2,1,"DPTR","Depositos en Transito (+)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(9,2,"CERR","Cargos Erroneos",0,0)
            aCbttco.save()
            aCbttco= Cbttco(8,2,"CHNC","Cheques no Contabilizados (-)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(7,2,"NDNC","Notas de Debito no Contabilizadas (-)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(6,2,"NCNC","Notas de Credito no Contabilizadas (+)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(5,2,"DNC","Deposito no Contabilizado (+)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(4,1,"NDTR","Notas de Debito en Transito (-)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(3,1,"NCTR","Notas de Credito en Transito (+)",0,0)
            aCbttco.save()
            aCbttco= Cbttco(10,2,"AERR","Abonos Erroneos",0,0)
            aCbttco.save()     
        data={}
        try:
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbrenc.objects.all():
                    item=i.toJSON()
                    item['position']=position
                    item['imgbcoroute']=i.imgbcoroute.name
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
            print(e)
            data['error']=str( e )
        return JsonResponse( data, safe=False )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        context['title']='Lista de Conciliaciones'
        context['codigo']='CBF01'
        context['create_url']=reverse_lazy( 'CBR:cbrenc_nueva' )
        context['account_url']=reverse_lazy( 'CBR:cbtcta-list' )
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
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
        data={}
        try:
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbtcta.objects.all():
                    item=i.toJSON()
                    item['position']=position
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
            if Cbwres.objects.filter(idrenc=idrenca).exists():
                return redirect('/verificar/?idrenc='+idrenca, idrenc= idrenca )
            else:
                if Cbsres.objects.filter(idrenc=idrenca).exists() == False:
                    print("automatico")
                    try:
                        conciliarSaldos(request)
                    except Exception as e:
                        print()
                        print(e)
                    print("hola")
                    
                return super().dispatch( request, *args, **kwargs )
        except:
            return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                # position=1
                DataSet=Cbsres.objects.filter( idrenc=idrenc )
                for i in DataSet:
                    item=i.toJSON()
                    # item['id']=position
                    # item['ID']=position
                    data.append( item )
                    # position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
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
        debebco = 0
        haberbco = 0
        try:
            listado = Cbsres.objects.filter(idrenc = self.request.GET.get( 'idrenc' ))
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
                    debebco = debebco + registro.debebco
                except:
                    pass
                try:
                    haberbco = haberbco + registro.haberbco
                except:
                    pass
        except Exception as e:
            print(e)
        context['habererp']="$"+'{:,}'.format(habererp)
        context['debeerp']="$"+'{:,}'.format(debeerp)
        context ['debebco']="$"+'{:,}'.format(debebco)
        context ['haberbco']="$"+'{:,}'.format(haberbco)
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )

        return context


            

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

class CbsresviewListView( ListView ):
    model=Cbsres
    template_name='cbsres/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                # position=1
                DataSet=Cbsres.objects.filter( idrenc=idrenc )
                for i in DataSet:
                    item=i.toJSON()
                    # item['id']=position
                    # item['ID']=position
                    data.append( item )
                    # position+=1
                if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
                    bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
                    bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
                    bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
                    bCbrenct.save()
                aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
                aCbrenct.idusu = request.user.username
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
        context['title']='Resultados'
        context['codigo']='CBF02'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['editable']= "No Editable"
        alertac = ""
        n = 0
        for i in Cbttco.objects.filter().all():
            if n>0:
                alertac = alertac +"\\n"
            alertac = alertac + i.codtco + " : " + i.destco
            n= n+1
        context['alertac'] = alertac
        debeerp = 0
        habererp = 0
        debebco = 0
        haberbco = 0
        try:
            listado = Cbsres.objects.filter(idrenc = self.request.GET.get( 'idrenc' ))
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
                    debebco = debebco + registro.debebco
                except:
                    pass
                try:
                    haberbco = haberbco + registro.haberbco
                except:
                    pass
        except Exception as e:
            print(e)
        context['habererp']="$"+'{:,}'.format(habererp)
        context['debeerp']="$"+'{:,}'.format(debeerp)
        context ['debebco']="$"+'{:,}'.format(debebco)
        context ['haberbco']="$"+'{:,}'.format(haberbco)

        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )

        return context

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
class CbrbcodDetailView( UpdateView ):
    form_class=CbrbcodForm
    template_name='cbrbcod/detail.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
            bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
            bCbrenct.save()
        aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = self.kwargs.get( 'idrbcoe' ) ).first())
        aCbrenct.idusu = request.user.username
        aCbrenct.accion = 8
        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.save()
        return super().dispatch( request, *args, **kwargs )

    def get_object(self):
        idrbcod=self.kwargs.get( 'idrbcod' )
        return get_object_or_404( Cbrbcod, idrbcod=idrbcod )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        print(self.kwargs)
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
        if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
            bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
            bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
            bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
            bCbrenct.save()
        aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = self.kwargs.get( 'idrerpe' ) ).first())
        aCbrenct.idusu = request.user.username
        aCbrenct.accion = 9
        aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
        aCbrenct.save()
        return super().dispatch( request, *args, **kwargs )

    def get_object(self):
        idrerpd=self.kwargs.get( 'idrerpd' )
        return get_object_or_404( Cbrerpd, idrerpd=idrerpd )

    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
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
        try:
            data={}
            idtcta=request.POST['idtcta']
            aCbtcta = Cbtcta.objects.get( idtcta
            =idtcta )
            
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
    print(request)
    print(request.POST)
    if request.method == 'POST':
        try:
            idrenc=request.POST.get( 'idrenc' )
            estado=Cbrenc.objects.get( idrenc=idrenc ).estado
            if (int(estado) < 2):
                existe=Cbsres.objects.filter( idrenc=idrenc ).count()
                sobreescribir=request.POST['sobreescribir']
                #Define si es posible conciliar(es primera vez, se acepto la sobreescritura y el estado no es conciliado ni eliminado)
                if ((sobreescribir == 'true') or (existe == 0)):

                    data={}
                    #Define los objetos a cargar y los saldos iniciales
                    bcoDataSet=Cbrbcod.objects.filter( idrbcoe=idrenc ).order_by( 'fechatra', 'horatra' )
                    erpDataSet=Cbrerpd.objects.filter( idrerpe=idrenc ).order_by( 'fechatra')
                    saldoacum_Dia_Bco=0
                    saldoacu_Mes_Bco=0
                    saldoacum_Dia_Erp=0
                    saldoacu_Mes_Erp=0

                    rowInicialbco=Cbrbcod.objects.filter( idrbcoe=idrenc).order_by( 'fechatra', 'horatra' ).first()
                    try:
                        saldoacu_Mes_Bco=rowInicialbco.saldo-rowInicialbco.haber+rowInicialbco.debe
                    except Exception as e:
                        print(e)
                        saldoacu_Mes_Bco=rowInicialbco.saldo
                    print("a")
                    rowInicialerp=Cbrerpd.objects.filter( idrerpe=idrenc ).order_by( 'fechatra').first()
                    try:
                        saldoacu_Mes_Erp=rowInicialerp.saldo-rowInicialerp.haber+rowInicialerp.debe
                    except Exception as e:
                        print(e)
                        saldoacu_Mes_Erp=rowInicialerp.saldo
                    print("b")
                    currentDay=rowInicialbco.fechatra
                    currentDayE=rowInicialerp.fechatra
                    Cbsres.objects.filter( idrenc=idrenc ).delete()
                    dia = 1
                    color = 0
                    cambio = False
                    while dia < 32:
                        #Para cada dia carga los registros del banco en orden, calculando los saldos
                        saldoacum_Dia_Bco = 0
                        fechatrabco = 0
                        for vwRow in bcoDataSet:
                            if vwRow.fechatra.day == dia:
                                fechatrabco=vwRow.fechatra
                                if (vwRow.fechatra is None):
                                    if (currentDay != vwRow.fechatra):
                                        currentDay=vwRow.fechatra
                                        saldoacum_Dia_Bco=0
                                saldoacum_Dia_Bco+= vwRow.haber - vwRow.debe
                                saldoacu_Mes_Bco+= vwRow.haber - vwRow.debe
                                try:
                                    saldoacu_Mes_Erp = Cbsres.objects.filter(idrenc=idrenc).order_by("-idsres").first().saldoacumeserp
                                except:
                                    pass
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
                                    saldodiferencia =saldoacu_Mes_Bco - saldoacu_Mes_Erp,
                                    saldoacumesbco=saldoacu_Mes_Bco,
                                    saldoacumeserp=saldoacu_Mes_Erp,
                                    saldoacumdiabco=saldoacum_Dia_Bco,
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
                                    blockcolor = color
                                    # --------------------
                                )
                                insCbsres.save()
                                cambio = True
                        for vwRow in erpDataSet:
                            #Para cada dia carga los registros del erp que coincilian
                            if vwRow.fechatra.day == dia:
                                    if Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).exists():
                                        insCbsres=Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco, debebco=vwRow.haber, haberbco=vwRow.debe).first()
                                        Unir(vwRow,insCbsres,saldoacu_Mes_Erp,saldoacum_Dia_Erp,idrenc,color)
                                        erpDataSet = erpDataSet.exclude(idrerpd=vwRow.idrerpd)
                        for vwRow in erpDataSet:
                            #Para cada dia carga los registros del erp que no concilian en  orden de cercania
                            if vwRow.fechatra.day == dia:
                                if fechatrabco != 0 and Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco ).exists():
                                    insCbsres=Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco ).first()
                                    insCbsres = Cbsres.objects.filter(idrenc=idrenc, idrerpd = 0, fechatrabco =fechatrabco).annotate(abs_diff=Func(F('debebco') - vwRow.haber + F('haberbco') - vwRow.debe, function='ABS')).order_by('abs_diff').first()
                                else:
                                    try:
                                        insCbsres=Cbsres(idrenc=Cbrenc.objects.get( idrenc=idrenc ), saldoacumesbco = saldoacu_Mes_Bco, blockcolor = color)
                                    except:
                                        insCbsres=Cbsres(idrenc=Cbrenc.objects.get( idrenc=idrenc ))
                                Unir(vwRow,insCbsres,saldoacu_Mes_Erp,saldoacum_Dia_Erp,idrenc,color)
                        saldoacum_Dia_Erp=0
                        dia = dia +1
                        if cambio == True:
                            if color == 0:
                                color = 1
                            else:
                                color = 0
                            cambio = False

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
                    aCbrenct.accion = 2
                    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
                    aCbrenct.save()
                    data={"idrenc": idrenc}
                else:
                    hist=Cbrenc.objects.get( idrenc=idrenc )
                    data={"existe_info": "¿Desea sobreescribir la conciliación anterior?"}
                    print("hola")
                    print(idrenc)
                    data['fechacons']=hist.fechacons.strftime( '%d-%m-%Y %H:%M:%S' )
                    print("chau")
                    data['idusucons']=hist.idusucons

            else:
                data={"info": "La conciliación ya fue cerrada"}
        except Exception as e:
            print(e)
            data['error']=str( e )
        return JsonResponse( data )
    else:
        return request

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
def Unir(vwRow,insCbsres,saldoacu_Mes_Erp,saldoacum_Dia_Erp,idrenc,color):
    #sistema que une el cbsres con banco cargado con un registro del cbrerpd
    saldoacu_Mes_Erp= saldoacu_Mes_Erp + vwRow.debe - vwRow.haber
    saldoacum_Dia_Erp+=vwRow.debe - vwRow.haber
    try:
        saldoacu_Mes_Bco = Cbsres.objects.filter(idrenc=idrenc).order_by("-idsres").first().saldoacumesbco
    except: 
        saldoacu_Mes_Bco = 0

    insCbsres.idrerpd=vwRow.idrerpd
    insCbsres.saldoacumeserp=saldoacu_Mes_Erp

    insCbsres.saldoacumdiaerp=saldoacum_Dia_Erp
    insCbsres.saldoerp=vwRow.saldo

        # estado=vwRow.esta,
        # historial=vwRow.,
        # --------------------
    insCbsres.fechatraerp=vwRow.fechatra
    insCbsres.debeerp=vwRow.debe
    insCbsres.habererp=vwRow.haber
    insCbsres.codtcoerp = " "
    try:
        insCbsres.saldodiferencia= insCbsres.saldoacumesbco - insCbsres.saldoacumeserp
    except:
        insCbsres.saldodiferencia= insCbsres.saldoacumeserp
    if insCbsres.saldodiferencia == 0:
        insCbsres.historial = 3
    insCbsres.nrotraerp = vwRow.nrotra
    insCbsres.fechatraerp = vwRow.fechatra
    insCbsres.nrocomperp = vwRow.nrocomp
    insCbsres.auxerp = vwRow.aux
    insCbsres.referp = vwRow.ref
    insCbsres.glosaerp = vwRow.glosa
    insCbsres.fechaconerp = vwRow.fechacon
    insCbsres.blockcolor = color


    if insCbsres.debeerp == insCbsres.haberbco and insCbsres.debebco == insCbsres.habererp:
        insCbsres.estadobco = 1
        insCbsres.estadoerp = 1
        insCbsres.linkconciliadobco = -2
        insCbsres.linkconciliadoerp = -2

    else:
        insCbsres.estadobco = 0
        insCbsres.estadoerp = 0

        # --------------------
    insCbsres.save()
    cambio = True

# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
def editCbwres(request):
        
        print(request)
        tabla = list(dict(request.POST).keys())[0][1:-1]
        while True:
            fila = tabla[:tabla.find("}")+1]
            comienzo = tabla[10:].find("{")
            if comienzo == -1:
                break
            tabla = tabla[comienzo+10:]
            print(fila)
            fila = json.loads(fila)
            print(fila["idsres"])

            idsres = fila["idsres"]
            idrenc = float(fila["idrenc"])
            try:
                debeerp = float(fila["debeerp"])
            except:
                debeerp = float(0)
            try:
                habererp = float(fila["habererp"])
            except:
                habererp = float(0)
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
                linkconciliadobco = int(fila["linkconciliadobco"])
            except:
                linkconciliadobco = int(0)
            try:
                linkconciliadoerp = int(fila["linkconciliadoerp"])
            except:
                linkconciliadoerp = int(0)
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
            blockcolor= aCbsres.blockcolor
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
            aCbwres = Cbwres(linkconciliadobco=linkconciliadobco,linkconciliadoerp=linkconciliadoerp,idsres=idsres, idrenc= idrenc, cliente=cliente, empresa=empresa, codbco=codbco, nrocta=nrocta, ano=ano, mes=mes, fechatrabco=fechatrabco, horatrabco=horatrabco, debebco=debebco, haberbco=haberbco, saldobco=saldobco, saldoacumesbco=saldoacumesbco, saldoacumdiabco=saldoacumdiabco, oficina=oficina, desctra=desctra, reftra=reftra, codtra=codtra, idrbcod=idrbcod,nrotraerp=nrotraerp,fechatraerp=fechatraerp,nrocomperp=nrocomperp, auxerp=auxerp, referp=referp,glosaerp=glosaerp,debeerp=debeerp,habererp=habererp, saldoerp=saldoerp, saldoacumeserp=saldoacumeserp, saldoacumdiaerp=saldoacumdiaerp,fechaconerp=fechaconerp,idrerpd=idrerpd, saldodiferencia=saldodiferencia, estadobco=estadobco,estadoerp=estadoerp, historial=historial, codtcobco=codtcobco, codtcoerp=codtcoerp)
            aCbwres.save()
        return HttpResponse("")
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #

@login_required
def cerrarConciliacion(request):
    if request.method == 'POST':
        try:
            idrenc=request.POST.get( 'idrenc' )
            CbrencUpd=Cbrenc.objects.get( idrenc=idrenc )
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
class DetalleBcoListView( ListView ):
    model=Cbrbcod
    template_name='cbrbcod/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
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
        context['title']='Detalle de carga del archivo de Banco'
        context['codigo']='CBF06'
        context['idrbcoe']=self.request.GET.get( 'idrbcoe' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
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
        data={}
        try:
            action=request.POST['action']
            idrenc=request.POST['idrenc']
            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbrenct.objects.filter( idrenc=idrenc ):
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
                aCbrenct = Cbrenct(formulario = "CBF05", idrenc = Cbrenc.objects.filter(idrenc = idrenc).first())
                aCbrenct.idusu = request.user.username
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
        context['title']='Tiempo'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        context['codigo']='CBF05'
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
        context['title']='eliminar'
        context['codigo']='CBF10'
        context['idrenc']=self.request.GET.get( 'idrenc' )
        #context['idtcta']=self.object.idtcta


        # context['create_url'] = reverse_lazy('CBR:cbrenc_nueva')
        context['list_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context


def verificarGuardado(request):
    return render(request, "cbrenc/confirmation-form.html")





def conservarGuardado(request):
    idrenca = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
        bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenca ).first())
    aCbrenct.idusu = request.user.username
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
        aCbsres.linkconciliadobco = aCbwres.linkconciliadobco
        aCbsres.codtcobco = aCbwres.codtcobco
        aCbsres.estadobco = aCbwres.estadobco
        aCbsres.linkconciliadoerp = aCbwres.linkconciliadoerp
        aCbsres.codtcoerp = aCbwres.codtcoerp
        aCbsres.estadoerp = aCbwres.estadoerp
        aCbsres.save()
        aCbwres.delete()
    try:
        print("hola")
        aCbsres = Cbsres.objects.filter(idrenc=idrenca).order_by('-idsres').first()
        aCbrenc = Cbrenc.objects.filter(idrenc=idrenca).first()
        aCbrenc.saldoerp=aCbsres.saldoacumeserp
        aCbrenc.difbcoerp = aCbrenc.saldobco - aCbrenc.saldoerp
        print("chau")
        aCbrenc.save()
        print("a")
        aCbrencl = Cbrencl(
            idrenc = Cbrenc.objects.filter(idrenc=idrenca).first(),
            status = 1,
            saldobco = Cbrenc.objects.filter(idrenc=idrenca).first().saldobco,
            saldoerp = aCbsres.saldoacumeserp+aCbsres.debeerp-aCbsres.habererp,
            difbcoerp = Cbrenc.objects.filter(idrenc=idrenca).first().saldobco - aCbsres.saldoacumeserp+aCbsres.debeerp-aCbsres.habererp,
            idusu = request.user.username)
        aCbrencl.fechact = dt.datetime.now(tz=timezone.utc)+huso
        print("b")
        aCbrencl.save(aCbrencl)
        if Cbsres.objects.filter(idrenc=idrenca, isconciliado = 1).exists():
            aCbrenc.estado = 1
            aCbrenc.save()
            return redirect("../../cbsres/?idrenc="+idrenca)
        

        else:
            if Cbsres.objects.filter(idrenc=idrenca, historial = 4, tipoconciliado = " ").exists():
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


def eliminarGuardado(request):
    idrenc = request.GET['idrenc']
    if Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).exists():
        bCbrenct = Cbrenct.objects.filter(idusu = request.user.username, fechorafin = None).first()
        bCbrenct.fechorafin = dt.datetime.now(tz=timezone.utc)+huso
        bCbrenct.tiempodif = bCbrenct.fechorafin - bCbrenct.fechoraini
        bCbrenct.save()
    aCbrenct = Cbrenct(formulario = "CBF02", idrenc = Cbrenc.objects.filter(idrenc = idrenc ).first())
    aCbrenct.idusu = request.user.username
    aCbrenct.accion = 10
    aCbrenct.fechoraini = dt.datetime.now(tz=timezone.utc)+huso
    aCbrenct.save()
    
    Cbwres.objects.filter(idrenc=idrenc).delete()


    return redirect("../../cbsres/?idrenc="+idrenc)

class DetalleErroresListView(ListView):
    model=Cbterr
    template_name= 'cbterr/list.html'

    @method_decorator( login_required )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            tabla=request.POST['tabla']

            if action == 'searchdata':
                data=[]
                position=1
                for i in Cbterr.objects.filter( tabla=tabla ):
                    item=i.toJSON()
                    item['position']=position
                    item['ID']=position
                    data.append( item )
                    position+=1
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str( e )
            print(e)
        return JsonResponse( data, safe=False )
    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs )
        context['title']='Detalle de Errores'
        context['codigo']='CBF10'
        context['tabla']=self.request.GET.get( 'tabla' )
        context['return_url']=reverse_lazy( 'CBR:cbrenc-list' )
        return context
