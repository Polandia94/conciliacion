function getdesbco(){
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    var codbco = '';
    codbco = $("#id_codbco").val();
    if ((codbco != '')) {
        $.ajax({
            method: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/getdesbco',
            data: {'codbco': codbco},
            success: function (respons) {
                if (respons) {
                    $("#id_desbco").val(respons.desbco);
                } else {
                    $("#id_desbco").val('2021');
                }
            },
            error: function (data) {
            }
        });
    }
}
function getAnoMes(){
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    var bco = '';
    var cta = '';
    var emp = '',
    bco = $("#id_codbco").val();
    cta = $("#id_nrocta").val();
    emp = $("#id_empresa").val();
    if ((bco != '') && ((cta != ''))) {
        $.ajax({
            method: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/getAnoMes',
            data: {'banco': bco, 'cuenta': cta, 'empresa': emp},
            success: function (respons) {
                if (respons) {
                    $("#id_ano").val(respons.ano);
                    $("#id_mes").val(respons.mes);
                } else {
                    $("#id_ano").val('2021');
                    $("#id_mes").val('4')
                }
            },
            error: function (data) {
            }
        });
    }
}

function getMailEmpresa(){
    const csrftoken = getCookie('csrftoken');
    var emp = '';
    var cli = '';
    emp = $("#id_empresa").val();
    cli = $("#cliente").val();
    $.ajax({
        method: 'GET',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: '/getMailEmpresa',
        data: {'empresa': emp, 'cliente': cli},
        success: function (respons) {
            if (respons) {
                $("#id_diremail").val(respons.diremail);
            } else {
                $("#id_diremail").val('');
            }
        },
        error: function (data) {
        }
    });
    
}

function getCuenta(){
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    var bco = '';
    var emp = '',
    bco = $("#id_codbco").val();
    emp = $("#id_empresa").val();
    var select = document.getElementById('id_nrocta');
    if (true) {
        $("#id_nrocta").empty();
        $.ajax({
            method: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/getcuenta',
            data: {'banco': bco, 'empresa': emp},
            
            success: function (respons) {
                if (respons) {
                    
                    for (var i = 0; i<respons.cuentas.length; i++){
                        var opt = document.createElement('option');
                        opt.value = respons.cuentas[i].nombre;
                        opt.innerHTML = respons.cuentas[i].nombre + " : " + respons.cuentas[i].descripcion;
                        select.appendChild(opt);
                    }
                    if(respons.cuentas.length != 0 && $("#id_archivoerp").val() != "" && $("#id_archivobco").val() != ""){
                        $('#btnCargar').attr('disabled', false);
                    }else{
                        $('#btnCargar').attr('disabled', true);
                    }
                    getAnoMes()
                } 
            },
            error: function (data) {
            }
        });
    }
}


function getCuentaSemi(){
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    var bco = '';
    var emp = '',
    bco = $("#id_codbco").val();
    emp = $("#id_empresa").val();
    var select = document.getElementById('id_nrocta');
    if (true) {
        $("#id_nrocta").empty();
        $.ajax({
            method: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/getcuenta',
            data: {'banco': bco, 'empresa': emp},
            
            success: function (respons) {
                if (respons) {
                    
                    for (var i = 0; i<respons.cuentas.length; i++){
                        var opt = document.createElement('option');
                        opt.value = respons.cuentas[i].nombre;
                        opt.innerHTML = respons.cuentas[i].nombre;
                        select.appendChild(opt);
                    }
                    if(respons.cuentas.length != 0 && $("#id_archivoerp").val() != "" && $("#id_archivobco").val() != ""){
                        $('#btnCargar').attr('disabled', false);
                    }else{
                        $('#btnCargar').attr('disabled', true);
                    }
                    getConfigSemi()
                } 
            },
            error: function (data) {
            }
        });
    }
}


function getConfigSemi(){
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    var bco = '';
    var emp = '',
    bco = $("#id_codbco").val();
    emp = $("#id_empresa").val();
    cta = $("#id_nrocta").val();
    var aproasi= document.getElementById('id_aproasi');
    var act= document.getElementById('id_activo');
    var banerp= document.getElementById('id_banerp');
    var erpban= document.getElementById('id_erpban');
    var idcam= document.getElementById('id_cam');
    var idmas= document.getElementById('nuevoConfiguracionAuto');

    
    if (true) {
        //$("#id_nrocta").empty();
        $.ajax({
            method: 'GET',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/getconfigsemi',
            data: {'banco': bco, 'empresa': emp, 'cuenta':cta},
            
            success: function (respons) {
                if (respons) {
                    
                    console.log(respons.actpas);
                    if(respons.actpas=='A'){
                        act.checked=true;
                    }else{
                        act.checked=false; 
                    }
                    if(respons.indas=='S'){
                        aproasi.checked=true;
                    }else{
                        aproasi.checked=false;
                    }
                    if(respons.bancoerp=='A'){
                        banerp.checked=true;
                    }else{
                        banerp.checked=false;
                    }
                    if(respons.erpbanco=='A'){
                        erpban.checked=true;
                    }else{
                        erpban.checked=false;
                    }
                    if(respons.campos=='A'){
                        idcam.checked=true;
                        idmas.disabled=false;
                        // for (var i = 0; i<respons.semis.length; i++){
                        // }     
                    }else{
                        idcam.checked=false;
                        idmas.disabled=true;
                    }                    
                } 
            },
            error: function (data) {
            }
        });
    }
}



(function ($) {
    "use strict"
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    
    $(".usercheck").on('click', function(e) {
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/usercheck/',
            success: function (respons) {                    
                if (respons.cerrar){
                    location.href = `/`
                }
            }
        })
    })

    $("#id_empresa").on('change', function (e) {
        getMailEmpresa()
    })
    
    function enviarMail(idrenc, url){
        var sigue = true
        mailLadoBancoHTML.disabled = true;
        mailLadoBancoPDF.disabled = true;
        mailLadoErpHTML.disabled = true;
        mailLadoErpPDF.disabled = true;
        
        function start(counter){
            if(sigue){
                setTimeout(function(){
                counter++;
                
                cargando.innerHTML = "Cargando " + counter + " segundos. Puede cerrar la pagina"
                start(counter);
                }, 1000);
            }else{
                cargando.innerHTML = ""
            }
        }
        start(0)
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: url,
            data : {"idrenc":idrenc},
            success: function (respons) {               
                sigue=false
                mailLadoBancoHTML.disabled = false;
                mailLadoBancoPDF.disabled = false;
                mailLadoErpHTML.disabled = false;
                mailLadoErpPDF.disabled = false;
                message_info(respons['info'], null, null)
        }

        });
    }
    $("#mailLadoBancoHTML").on('click', function (e) {
        console.log("enviar")
        const idrenc = document.getElementById('idrenc').innerHTML;
        const url = '/enviarmail/ladobancohtml'
        enviarMail(idrenc, url)
    });
    $("#mailLadoBancoPDF").on('click', function (e) {
        console.log("enviar")
        const idrenc = document.getElementById('idrenc').innerHTML;
        const url = '/enviarmail/ladobancopdf'
        enviarMail(idrenc, url)
    });
    $("#mailLadoErpHTML").on('click', function (e) {
        console.log("enviar")
        const idrenc = document.getElementById('idrenc').innerHTML;
        const url = '/enviarmail/ladoerphtml'
        enviarMail(idrenc, url)
    });
    $("#mailLadoErpPDF").on('click', function (e) {
        console.log("enviar")
        const idrenc = document.getElementById('idrenc').innerHTML;
        const url = '/enviarmail/ladoerppdf'
        enviarMail(idrenc, url)
    });

    $("#nuevoConfiguracionAuto").on('click', function (e) {

                $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/cbtcfg/nuevo/',
                    success: function (respons) {                    
                        location.reload();
                }

            });
    });
    

    

    /******************************************************************************************************************/
    /******************************************************************************************************************/

    $("#btnResetColumns").on('click', function (e) {
        confirmar_accion('Confirmación', '¿Reiniciar el orden de las columnas?',
            function () {
                const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
                let enviar = {}
                for(let i=0; i<visibilidad.length;i++){
                    enviar[i]=true
                }
                $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/cbtusuc/guardado/',
                    data: {'cbtusuc': enviar},
                    success: function (respons) {                    
                        location.reload();
                }
            });
                var table = $('#data').DataTable();
                table.colReorder.reset();
            });
    });
    /******************************************************************************************************************/
    /******************************************************************************************************************/

    
    $("#btnSalir").on('click', function (e) {
        const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
        let enviar = {}
        for(let i=0; i<visibilidad.length;i++){
            enviar[i]=visibilidad[i]["visible"]
        }

        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if(globalVariable.bloqueado){
            window.alert("Espere a que termine de guardar")
        }else{
        if (globalVariable.editado == 1){
            ajax_confirm("../verificar/eliminar/?idrenc="+idrenc, 'Notificación',
                'Se han modificado datos en la grilla, ¿desea salir sin guardar?', parameters,
                function () {
                    $.ajax({
                        method: 'POST',
                        beforeSend: function (request) {
                            request.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        url: '/cbtusuc/guardado/',
                        data: {'cbtusuc': enviar},
                        success: function (respons) {                    
                            globalVariable.editado = 0
                            location.href = `../`;
                    }
                });

                    return false;
                });
            }else{
                    $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/cbtusuc/guardado/',
                    data: {'cbtusuc': enviar},
                    success: function (respons) {                    
                        globalVariable.editado = 0
                        location.href = `../`;
                        }
                    });
                };
            }
            
    });


        /******************************************************************************************************************/
    /******************************************************************************************************************/


            /******************************************************************************************************************/
    /******************************************************************************************************************/
 
            /******************************************************************************************************************/
    /******************************************************************************************************************/
 
    $("#btnGuardar").click(function () {      
        const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
        let enviar = {}
        for(let i=0; i<visibilidad.length;i++){
            enviar[i]=visibilidad[i]["visible"]
        }  
        const idrenc = urlParams.get('idrenc');
        if(globalVariable.bloqueado){
            window.alert("Espere a que termine de guardar")
        }else{
        if(cargando.innerHTML == ""){
                $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/cbtusuc/guardado/',
                    data: {'cbtusuc': enviar},
                    success: function (respons) {                    
                        $.ajax({
                            method: 'GET',
                            beforeSend: function (request) {
                                request.setRequestHeader("X-CSRFToken", csrftoken);
                            },
                            url: '/getGuardado',
                            data: {'idrenc': idrenc},
                            success: function (respons) {
                                if (respons.guardado=="si") {
                                    globalVariable.bloqueado = true;
                                    globalVariable.editado = 0;
                                    location.href = "../verificar/conservar/?idrenc=" + idrenc;
                                } else {
                                    alert(respons.guardado)
                                }}
                        });
                }
            });
            
        }else{
            alert("Espere a que termine de cargar")
        }}
});

            /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnCerrar").on('click', function () {        
        window.close()
    });


        /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnRecargar").on('click', function (e) {
        const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
        let enviar = {}
        for(let i=0; i<visibilidad.length;i++){
            enviar[i]=visibilidad[i]["visible"]
        }
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if(globalVariable.bloqueado){
            window.alert("Espere a que termine de guardar")
        }else{
        if (globalVariable.editado == 1){
            ajax_confirm("../verificar/eliminar/?idrenc="+idrenc, 'Notificación',
                'Ud. Perderá las modificaciones de conciliación realizadas, desea continuar ?', parameters,
                function () {
                    globalVariable.editado = 0
                    $.ajax({
                        method: 'POST',
                        beforeSend: function (request) {
                            request.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        url: '/cbtusuc/guardado/',
                        data: {'cbtusuc': enviar},
                        success: function (respons) {                    
                            location.href =   `/cbsres/?idrenc=`+idrenc;
                    }
                });
                });
            }else{
                $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/cbtusuc/guardado/',
                    data: {'cbtusuc': enviar},
                    success: function (respons) {                    
                        globalVariable.editado = 0
                        location.href = `/cbsres/?idrenc=`+idrenc;
                }
            });
                };
            }
    });
        /******************************************************************************************************************/
    /******************************************************************************************************************/

    $("#btnCerrarConciliacion").on('click', function (e) {
        const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
        let enviar = {}
        for(let i=0; i<visibilidad.length;i++){
            enviar[i]=visibilidad[i]["visible"]
        }
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if(globalVariable.bloqueado){
            window.alert("Espere a que termine de guardar")
        }else{
        
                globalVariable.bloqueado = true;
                $.ajax({
                    method: 'GET',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    url: '/getGuardado',
                    data: {'idrenc': idrenc},
                    success: function (respons) {
                        if (respons.guardado=="si") {
                            globalVariable.bloqueado = false;
                            globalVariable.editado = 0;
                            ajax_confirm("../cerrarConciliacion/", 'Notificación',
                            '¿Cerrar conciliación? La conciliación se pasará a estus Conciliado y revisado.', parameters,
                            function () {
                                $.ajax({
                                    method: 'POST',
                                    beforeSend: function (request) {
                                        request.setRequestHeader("X-CSRFToken", csrftoken);
                                    },
                                    url: '/cbtusuc/guardado/',
                                    data: {'cbtusuc': enviar},
                                    success: function (respons) {
                                        location.href = "/"
                                }
                            });
                        });
                        } else {
                            globalVariable.bloqueado = false;
                            alert(respons.guardado)
                        }}
                });
        
                
        
        
    }

    });
        /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnNoConciliados").on('click', function () {
       
        const idrenc = urlParams.get('idrenc');
        var url = '/noconciliados/';
        var form = $('<form action="' + url + '"type="hidden" method="post">' +
        '<input type="text" name="idrenc" value="' + idrenc + '" /><input type="hidden" name="csrfmiddlewaretoken" value="'+csrftoken+'" />' +
        '</form>');
        $('body').append(form);
        form.submit();
        
        

            
    });
    /******************************************************************************************************************/
    /******************************************************************************************************************/

    /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnConciliar").on('click', function () {
        const visibilidad = JSON.parse(localStorage.getItem("DataTables_data_/cbsres/"))["columns"]
        let enviar = {}
        globalVariable.editado = 0;
        for(let i=0; i<visibilidad.length;i++){
            enviar[i]=visibilidad[i]["visible"]
        }  
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc, "sobreescribir": 'false'};
        if(globalVariable.bloqueado){
            window.alert("Espere a que termine de guardar")
        }else{
            function start(counter){
                if(counter < 300){
                    setTimeout(function(){
                    counter++;
                    cargando.innerHTML = "Conciliando " + counter + " segundos"
                    start(counter);
                    }, 1000);
                }
            }
            start(0)
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: '/cbtusuc/guardado/',
            data: {'cbtusuc': enviar},
            success: function (respons) {
            console.log("PASO POR AQUI")
             // Si se quiere que solo concilie los saldos exitentes, en vez de volver desde cero la url es ../conciliarSaldosExistentes/, no battle tested., solo mandar un post con los parameters ahi, y en done un reload
            $.ajax({
                url: "../conciliarSaldos/", //window.location.pathname
                type: 'POST',
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                data: parameters,
                // dataType: 'json',
                // processData: false,
                // contentType: false,
            }).done(function (response) {
                //location.reload()
                if (response.hasOwnProperty('idrenc')) {
                    location.href = `../cbsres/?idrenc=${response['idrenc']}`;
                    return false;
                }
                if (response.hasOwnProperty('existe_info')) {
                    const mensaje = `<label> ${response['existe_info']}</label><p class="m-0">Generado por:</p>  <label class="m-0">Usuairo: <strong> ${response['idusucons']}</strong></label><label>Fecha: <strong> ${response['fechacons']}</strong></label> `
                    ajax_confirm("../conciliarSaldos/", 'Confirmación',
                        mensaje, {'idrenc': idrenc, "sobreescribir": 'true'},
                        
                        function (response) {  
                            location.href = `../cbsres/?idrenc=${response['idrenc']}`;
                        },
                        true
                        )
                    
                    return false;
                }
                if (response.hasOwnProperty('info')) {
                    message_info(response['info'], null, null)
                    return false;
                }
            })
        
            }

        });
    }
            
    });
    /******************************************************************************************************************/
    /******************************************************************************************************************/
    


    $(".getanomes").change(getAnoMes);

        
    $(".getcuenta").change(getCuenta);

    $(".getcuentasemi").change(getCuentaSemi);

    $(".getdesbco").change(function () {
        getdesbco()
    });

})(jQuery);




