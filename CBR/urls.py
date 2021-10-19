from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse
from numpy import False_
from . import views
from django.conf import settings
from django.conf.urls.static import static

# from django.views.generic.base import TemplateView #new
# from .views import ConciliacionNueva
from .models import Cbrenc

app_name='CBR'
    
urlpatterns=[
    path( 'login/', views.login, name='login' ),
    path( 'reiniciarusuario/', views.reiniciarUsuario, name='reiniciarUsuario' ),
    path( 'cerrarsesionusuario/', views.cerrarsesionusuario, name='cerrarsesionusuario' ),
    path( 'getAnoMes/', views.getanomes, name='getAnoMes' ),
    path( 'getGuardado/', views.getguardado, name='getGuardado' ),
    path( 'getTiposDeConciliacion/', views.getTiposDeConciliacion, name='getTiposDeConciliacion' ),
    path( 'conciliarSaldos/', views.conciliarSaldos, name='conciliarSaldos' ),
    path( 'cbrenc/del/', views.ConciliacionDeleteForm.as_view(), name='cbrenc-del' ),
    path( 'cbtcta/del/', views.cbtctaDelete, name='cbtcta_delete_cuenta' ),
    path( 'cbtemp/del/', views.cbtempDelete, name='cbtemp_delete_empresa' ),
    path( 'cbtbco/del/', views.cbtbcoDelete, name='cbtbco_delete_banco' ),
    path( 'cerrarConciliacion/', views.cerrarConciliacion, name='cerrarConciliacion' ),
    path( 'cbrgale/', views.DetalleErroresGalListView.as_view(), name='DetalleErroresGalListView' ),
    path( 'cbrbode/', views.DetalleErroresBodListView.as_view(), name='DetalleErroresBodListView' ),


    path( '', views.CbrencListView.as_view(), name='index' ),
    path( '', views.CbrencListView.as_view(), name='cbrenc-list' ),
    path( 'getColumnas/', views.getColumnas, name='getColumnas' ),
    path( 'definircolumnas/', views.definirColumnas.as_view(), name='definirColumnas' ),
    path( 'cbtcta/', views.CbtctaListView.as_view(), name='cbtcta-list' ),
    path( 'cbtcta/edit/', views.CbtctaEditView.as_view(), name='cbtcta_edit_cuenta' ),
    path( 'cbtusu/edit/', views.CbtusuEditView.as_view(), name='cbtusu_edit_usuario' ),
    path( 'cbtemp/edit/', views.CbtempEditView.as_view(), name='cbtemp_edit_empresa' ),
    path( 'cbtbco/edit/', views.CbtbcoEditView.as_view(), name='cbtbco_edit_banco' ),
    path( 'cbtusuc/guardado/', views.CbtusucGuardar, name='cbtusuc_guardar' ),
    path( 'cbsres/', views.CbsresListView.as_view(), name='cbsres-list' ),
    path( 'cbsresview/', views.CbsresviewListView.as_view(), name='cbsresview-list' ),
    path( 'verificarcarga/', views.verificarCarga, name='cbrenc-car' ),
    path( 'verificarcarga/eliminar/', views.eliminarCarga, name='cbrenc-elicar' ),
    path( 'cerrarotrapestana/', views.cerrarOtraPestana, name='cerrarOtraPestana' ),

    path( 'verificar/', views.verificarGuardado, name='cbrenc-ver' ),
    path( 'verificar/conservar/', views.conservarGuardado, name='cbrenc-con' ),
    path( 'verificar/eliminar/', views.eliminarGuardado, name='cbrenc-eli' ),

    path( 'cbtemp/', views.ListaEmpresaView.as_view(), name='cbtemp-list' ),
    path( 'cbtbco/', views.ListaBancoView.as_view(), name='cbtbco-list' ),
    path( 'cbtemp/new', views.CbtempCreateView.as_view(), name='empresa-nueva' ),
    path( 'cbtbco/new', views.CbtbcoCreateView.as_view(), name='banco-nuevo' ),

    path( 'cbtusu/', views.ListaUsuarioView.as_view(), name='cbtusu-list' ),
    path( 'cbtusue/', views.ListaCbtusueView.as_view(), name='cbtusue-list' ),
    path( 'cbtusu/new', views.CbtusuCreateView.as_view(), name='usuario-nuevo' ),
    path( 'cbtusu/res/', views.resetPassword, name='reset-password'),
    path( 'cbtusu/del/', views.cbtusuDelete, name='cbtusu-del' ),
    path( 'cbrbcod/', views.DetalleBcoListView.as_view(), name='cbrbcod-list' ),
    path( 'cbrerpd/', views.DetalleErpListView.as_view(), name='cbrerpd-list' ),
    path( 'log/', views.DetalleLogListView.as_view(), name='log-list' ),
    path( 'tiempo/', views.DetalleTiempoListView.as_view(), name='tiempo-list' ),
    path( 'cbttco/', views.DetalleTiposDeConciliacion.as_view(), name='DetalleTiposDeConciliacion' ),


    path( 'cbrbcod/<int:idrbcod>/<int:idrbcoe>/', views.CbrbcodDetailView.as_view(), name='cbrbcod-detail' ),
    path( 'cbrerpd/<int:idrerpd>/<int:idrerpe>/', views.CbrerpdDetailView.as_view(), name='cbrerpd-detail' ),



    path( 'list/add/', views.CbrencCreateView.as_view(), name='cbrenc_nueva' ),
    path( 'list/addaccount/', views.CbtctaCreateView.as_view(), name='cbtcta_nueva_cuenta' ),
    path('updateScript/', views.editCbwres, name='edit_cbwres'),
    path('updateCbtusue/', views.updateCbtusue, name='update-cbtusue'),
    path('descargarArchivos/', views.DescargarArchivoView.as_view(), name='descargar_archivo')
    #path( 'log/<int:idrenc>/', views.CbrecnlListView.as_view(), name='cbrecnl-list' ),


]  + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )
