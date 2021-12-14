from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, reverse

from . import utils, views

app_name = 'CBR'

urlpatterns = [

    #************* INICIO DE SESION ********************

    path('login/', utils.login, name='login'),
    path('cerrarsesionusuario/', utils.cerrarsesionusuario, name='cerrarsesionusuario'),
    path('cbtusu/res/', views.resetPassword, name='reset-password'),
    #************* Útiles ********************

    path('getAnoMes/', utils.getanomes, name='getAnoMes'),
    path('getdesbco/', utils.getdesbco, name='getdesbco'),
    path('getcuenta', utils.getcuenta, name='getcuenta'),
    path('getGuardado/', utils.getguardado, name='getGuardado'),
    path('getTiposDeConciliacionpost/', utils.getTiposDeConciliacionpost, name='getTiposDeConciliacion'),  
    path('conciliarSaldos/', utils.conciliarSaldos, name='conciliarSaldos'),
    path('conciliarSaldosExistentes/', utils.conciliarSaldosExistentes, name='conciliarSaldosExistentes'),
    path('getColumnas/', utils.getColumnas, name='getColumnas'),


    #*********** Listas **********************

    #path( '', views.CbrencListView.as_view(), name='index' ),
    path('', views.CbrencListView.as_view(), name='cbrenc-list'),
    path('cbrgale/', views.DetalleErroresGalListView.as_view(),  name='DetalleErroresGalListView'),
    path('cbrbode/', views.DetalleErroresBodListView.as_view(),  name='DetalleErroresBodListView'),
    path('cbtcta/', views.CbtctaListView.as_view(), name='cbtcta-list'),
    path('cbsres/', views.CbsresListView.as_view(), name='cbsres-list'),
    path('cbsresview/', views.CbsresviewListView.as_view(), name='cbsresview-list'),
    path('cbtemp/', views.ListaEmpresaView.as_view(), name='cbtemp-list'),
    path('cbtbco/', views.ListaBancoView.as_view(), name='cbtbco-list'),
    path('cbtusu/', views.ListaUsuarioView.as_view(), name='cbtusu-list'),
    path('cbtusue/', views.ListaCbtusueView.as_view(), name='cbtusue-list'),
    path('log/', views.DetalleLogListView.as_view(), name='log-list'),
    path('tiempo/', views.DetalleTiempoListView.as_view(), name='tiempo-list'),
    path('cbttco/', views.DetalleTiposDeConciliacion.as_view(), name='DetalleTiposDeConciliacion'),
    path('cbrbcod/', views.DetalleBcoListView.as_view(), name='cbrbcod-list'),
    path('cbrerpd/', views.DetalleErpListView.as_view(), name='cbrerpd-list'),
    path('cbsusu/', views.visualizacionUsuarios.as_view(), name='visualizacion_usuarios'),
    path('cbtcfg/', views.ConciliacionSemiautomatica.as_view(), name='conciliacion_semiautomatica'),
    #*********** Crear Nuevo ***********

    path('cbtemp/new', views.CbtempCreateView.as_view(), name='empresa-nueva'),
    path('cbtbco/new', views.CbtbcoCreateView.as_view(), name='banco-nuevo'),
    path('cbtusu/new', views.CbtusuCreateView.as_view(), name='usuario-nuevo'),
    path('list/add/', views.CbrencCreateView.as_view(), name='cbrenc_nueva'),
    path('list/addaccount/', views.CbtctaCreateView.as_view(), name='cbtcta_nueva_cuenta'),
    path('cbtcfg/nuevo/', utils.CbtcfgCreate, name='cbtcfg_nueva_cbtcfg'),
    #*********** Eliminar ************
    path('cbrenc/del/', views.ConciliacionDeleteForm.as_view(), name='cbrenc-del'),
    path('cbtcta/del/', utils.cbtctaDelete, name='cbtcta_delete_cuenta'),
    path('cbtemp/del/', views.cbtempDelete, name='cbtemp_delete_empresa'),
    path('cbtbco/del/', views.cbtbcoDelete, name='cbtbco_delete_banco'),
    path('cbtusu/del/', views.cbtusuDelete, name='cbtusu-del'),
    path('cbrenc/desc/', utils.cbrencDesconciliar, name='cbrenc-desc'),

    #********* Editar Elementos *********

    path('cbtcta/edit/', views.CbtctaEditView.as_view(), name='cbtcta_edit_cuenta'),
    path('cbtusu/edit/', views.CbtusuEditView.as_view(), name='cbtusu_edit_usuario'),
    path('cbtemp/edit/', views.CbtempEditView.as_view(), name='cbtemp_edit_empresa'),
    path('cbtbco/edit/', views.CbtbcoEditView.as_view(), name='cbtbco_edit_banco'),
    path('uploadimage', views.Uploadimage.as_view(), name='uploadimage'),
    
    #********** Detalles ***************

    path('cbrbcod/<int:idrbcod>/<int:idrbcoe>/', views.CbrbcodDetailView.as_view(), name='cbrbcod-detail'),
    path('cbrerpd/<int:idrerpd>/<int:idrerpe>/', views.CbrerpdDetailView.as_view(), name='cbrerpd-detail'),
    path('noconciliados/<int:idrenc>/', views.CbsresNoConciliados.as_view(), name='noconciliados'),
    
    #*********** Enviar mails *******************
    path('verBancoHtml', views.verLadoBancoHtml, name='verLadoBancoHtml'),
    path('enviarmail/ladobancohtml', utils.enviarMailLadoBancoHtml, name='enviarMailLadoBancoHtml'),
    path('verBancopdf', views.verLadoBancoPdf.as_view(), name='verLadoBancoPdf'),
    path('enviarmail/ladobancopdf', utils.enviarMailLadoBancoPdf, name='enviarMailLadoBancoPdf'),
    path('verErpHtml', views.verLadoErpHtml, name='verLadoErpHtml'),
    path('enviarmail/ladoerphtml', utils.enviarMailLadoErpHtml, name='enviarMailLadoErpHtml'),
    path('vererppdf', views.verLadoErpPdf.as_view(), name='verLadoBancoPdf'),
    path('enviarmail/ladoerppdf', utils.enviarMailLadoErpPdf, name='enviarMailLadoErpHtml'),
    
    #* Otras Acciones
    path('getMailEmpresa/', utils.getMailEmpresa, name='getMailEmpresa'),
    path('cbtusu/check/', utils.chequearUsuarioConectado, name='chequearUsuarioConectado'),
    path('reiniciarusuario/', views.reiniciarUsuario, name='reiniciarUsuario'),
    path('cerrarConciliacion/', views.cerrarConciliacion, name='cerrarConciliacion'),
    path('definircolumnas/', views.definirColumnas.as_view(), name='definirColumnas'),
    path('cbtusuc/guardado/', views.CbtusucGuardar, name='cbtusuc_guardar'),
    path('verificarcarga/', views.verificarCarga, name='cbrenc-car'),
    path('verificarcarga/eliminar/', views.eliminarCarga, name='cbrenc-elicar'),
    path('cerrarotrapestana/', views.cerrarOtraPestana, name='cerrarOtraPestana'),
    path('verificar/', views.verificarGuardado, name='cbrenc-ver'),
    path('verificar/conservar/', utils.conservarGuardado, name='cbrenc-con'),
    path('verificar/eliminar/', views.eliminarGuardado, name='cbrenc-eli'),
    path('updateScript/', views.editCbwres, name='edit_cbwres'),
    path('updateCbtusue/', views.updateCbtusue, name='update-cbtusue'),
    path('descargarArchivos/', views.DescargarArchivoView.as_view(), name='descargar_archivo'),
    path('posibilidaddeconciliar/', utils.posibilidadDeConciliar, name='posibilidad_de_conciliar'),
    path('updatecbtusuc/', utils.updateCbtusuc, name='posibilidad_de_conciliar'),
    path('usercheck/', utils.userCheck, name='usercheck'),
    path('cierredeemergencia/', utils.cierreDeEmergencia, name='cierredeemergencia'),
    path('updatecbtcfg/', utils.updateCbtcfg, name='update_cbtcfg')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
