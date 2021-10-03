(function ($) {
    "use strict"
    const csrftoken = getCookie('csrftoken');
    const urlParams = new URLSearchParams(window.location.search);
    $("#btnResetColumns").on('click', function (e) {
        confirmar_accion('Confirmación', '¿Reiniciar el orden de las columnas?',
            function () {
                var table = $('#data').DataTable();
                table.colReorder.reset();
            });
    });
    /******************************************************************************************************************/
    /******************************************************************************************************************/

    $("#btnSalir").on('click', function (e) {
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if (globalVariable.editado == 1){
            ajax_confirm("../verificar/eliminar/?idrenc="+idrenc, 'Notificación',
                'Se han modificado datos en la grilla, ¿desea salir sin guardar?', parameters,
                function () {
                    globalVariable.editado = 0
                    location.href = `../`;
                    return false;
                });
            }else{
                    location.href = `../`;
                    return false;
                };
            
    });


        /******************************************************************************************************************/
    /******************************************************************************************************************/


            /******************************************************************************************************************/
    /******************************************************************************************************************/
 
            /******************************************************************************************************************/
    /******************************************************************************************************************/
 
    $("#btnGuardar").click(function () {        
        const idrenc = urlParams.get('idrenc');
        if(cargando.innerHTML == ""){
            $.ajax({
                method: 'GET',
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", csrftoken);
                },
                url: '/getGuardado',
                data: {'idrenc': idrenc},
                success: function (respons) {
                    if (respons.guardado=="si") {
                        globalVariable.editado = 0;
                        location.href = "../verificar/conservar/?idrenc=" + idrenc;
                    } else {
                        alert(respons.guardado)
                    }}
            });
        }else{
            alert("Espere a que termine de cargar")
        }
});

            /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnCerrar").on('click', function () {        
        window.close()
    });


        /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnRecargar").on('click', function (e) {
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if (globalVariable.editado == 1){
            ajax_confirm("../verificar/eliminar/?idrenc="+idrenc, 'Notificación',
                'Ud. Perderá las modificaciones de conciliación realizadas, desea continuar ?', parameters,
                function () {
                    globalVariable.editado = 0
                    location.href = `/cbsres/?idrenc=`+idrenc;
                    return false;
                });
            }else{
                    globalVariable.editado = 0
                    location.href = `/cbsres/?idrenc=`+idrenc;
                    return false;
                };
    });
        /******************************************************************************************************************/
    /******************************************************************************************************************/

    $("#btnCerrarConciliacion").on('click', function (e) {
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc};
        if (globalVariable.SaldoDiferenciaTotal == 0){
        ajax_confirm("../cerrarConciliacion/", 'Notificación',
            '¿Cerrar conciliación? La conciliación se pasará a estus Conciliado y revisado.', parameters,
            function () {
                location.href = `../cbsres/?idrenc=`+idrenc;
                return false;
            });
        }

    });
        /******************************************************************************************************************/
    /******************************************************************************************************************/

    /******************************************************************************************************************/
    /******************************************************************************************************************/
    $("#btnConciliar").on('click', function () {
        const idrenc = urlParams.get('idrenc');
        var parameters = {'idrenc': idrenc, "sobreescribir": 'false'};
        
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
            console.log(response)
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

        });
            
    });
    /******************************************************************************************************************/
    /******************************************************************************************************************/
    $(".getanomes").change(function () {
        var bco = '';
        var cta = '';
        bco = $("#id_codbco").val();
        cta = $("#id_nrocta").val();
        if ((bco != '') && ((cta != ''))) {
            $.ajax({
                method: 'GET',
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", csrftoken);
                },
                url: '/getAnoMes',
                data: {'banco': bco, 'cuenta': cta},
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
    });

})(jQuery);

async function primeraCargaCbsres(){
        let cargadoIncompleto = true
        const csrftoken = getCookie('csrftoken');
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
        const idrencparam = String(parseInt(idrenc))
        console.log("1")
        console.log("2")
        
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                console.log("3")
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "../conciliarSaldos/",
            data: {'idrenc': idrencparam, "sobreescribir": 'false'},
            success: function (respons) {
                    console.log("falla aca:")
                    if(!window.location.hash && respons.hasOwnProperty('existe_info') == false) {
                        window.location = window.location + '#loaded';
                        window.location.reload();
                    }
                    cargadoIncompleto = false
        
            }})
        console.log("4")
        if(cargadoIncompleto){
                            console.log("9");
                            // var contador = 0;
                            console.log("b");
                            //start(0)
                            console.log("c");
                            }
        function start(contador){
            contador = contador +3
            console.log("a");
            if(cargadoIncompleto && contador < 100){
                console.log("cuenta")
                cargando.innerHTML = "Conciliando " + contador.toString() + " segundos"
                setTimeout(function(){
                    start(contador); 
                 },3000)
            }else{
                cargando.innerHTML = ""
            };
        }
    }