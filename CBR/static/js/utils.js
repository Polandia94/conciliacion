"use strict"
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function number_format (number, decimals, dec_point, thousands_sep) { number = (number + '').replace(/[^0-9+-Ee.]/g, ''); var n = !isFinite(+number) ? 0 : +number, prec = !isFinite(+decimals) ? 0 : Math.abs(decimals), sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep, dec = (typeof dec_point === 'undefined') ? '.' : dec_point, s = '', toFixedFix = function (n, prec) { var k = Math.pow(10, prec); return '' + Math.round(n * k) / k; }; parseFloat(0.55).toFixed(0) = 0; s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.'); if (s[0].length > 3) { s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep); } if ((s[1] || '').length < prec) { s[1] = s[1] || ''; s[1] += new Array(prec - s[1].length + 1).join('0'); } return s.join(dec); }
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function _ajax(url, parameters, callback){

    $.ajax({
            url: url, //window.location.pathname
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            data: parameters,
            dataType: 'json',
            processData: false,
            contentType: false,
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                  if (data.hasOwnProperty('msgInfo')) {
                      message_info(data.msgInfo, callback, data);
                      return false;
                  }

                  if ( data.hasOwnProperty('msgConfirmar') ){

                      message_info(data.msgConfirmar, function (data){


                            parameters.set("confirmado", true);

                            _ajax( url, parameters, callback(data));
                      }, data);
                      return false;
                  }
                  callback(data);
                  return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function submit_(url, title, content, parameters, callback,contador) {
    let error=false;
    function start(counter){
        if(counter < 300){
            setTimeout(function(){
            counter++;
            
            if(error){
                cargando.innerHTML = "Carga err??nea"
            }else{
            cargando.innerHTML = "Cargando " + counter + " segundos"
            start(counter)}},1000)};
    };
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'large',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    try{
                        if(contador){
                            start(0)
                        }
                    }
                    catch{console.log("falla")}
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        beforeSend: function(request) {
                            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        },
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                              if (data.hasOwnProperty('msgInfo')) {

                                  message_info(data.msgInfo, callback, data);
                                  return false;
                              }

                              if ( data.hasOwnProperty('msgArchivoCargado') ){
                                  message_info(data.msgArchivoCargado, function (data){
                                        parameters.set("sobreescribir", true);
                                        submit_(window.location.pathname, 'Notificaci??n', '??Sobre escribir carga anterior? ', parameters, function (data) {
                                            location.href = '/';
                                        });
                                  }, data);
                                  return false;
                              }
                              callback(data);
                              return false;
                        }
                        message_error(data.error);
                        error = true
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function ajax_confirm(url, title, content, parameters, callback,contador) {
    let cargadoIncompleto = true;
    function start(counter){
        if(counter < 300){
            setTimeout(function(){
            counter++;
            if(cargadoIncompleto){
            cargando.innerHTML = "Conciliando " + counter + " segundos"
            start(counter)};
            }, 1000);
        }else{
        
            if(cargadoIncompleto){
            cargando.innerHTML = "Hubo un problema. Recargue la p??gina"}
        }
    };
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    try{
                    if(contador){
                    start(0)}}
                    catch{}
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        beforeSend: function(request) {
                            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        },
                        data: parameters,
                        // dataType: 'json',
                        // processData: false,
                        // contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function message_info(obj, callback, data) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Aviso!',
        html: html,
        icon: 'info',
        confirmButtonText: 'Aceptar',
        allowOutsideClick: false
    }).then( function(result){
            if (callback != null)
                callback(data);
          });
}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });

}
// # ***************************************************************************************************************** #
// # ***************************************************************************************************************** #
function confirmar_accion(title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    // cancel();
                }
            },
        }
    })
}







async function primeraCargaCbsres(){
        let cargadoIncompleto = true
        const csrftoken = getCookie('csrftoken');
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
        const idrencparam = String(parseInt(idrenc))
        start(0)
        
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "../conciliarSaldos/",
            data: {'idrenc': idrencparam, "sobreescribir": 'false'},
            success: function (respons) {
                    console.log(respons)
                    if(respons.hasOwnProperty('existe_info') == false) {
                        //window.location = window.location + '#loaded';
                        window.location.reload();
                    }
                    cargadoIncompleto = false

        
            }})
            
            function start(counter){
                if(counter < 300){
                    setTimeout(function(){
                    counter++;
                    if(cargadoIncompleto){
                    cargando.innerHTML = "Conciliando " + counter + " segundos"
                    start(counter)};
                    }, 1000);
                }else{
                
                    if(cargadoIncompleto){
                    cargando.innerHTML = "Hubo un problema. Recargue la p??gina"}
                }
            }

            
    }