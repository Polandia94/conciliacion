$(function () {
    "use strict"
    const urlParams = new URLSearchParams(window.location.search);
    const idrenc = urlParams.get('idrenc');
    $('#data').DataTable({
        targets: 'no-sort',
        bSort: false,
        order: [],
        responsive: true,
        autoWidth: true,
        destroy: true,
        hover: true,
        deferRender: true,
        colReorder: true,
        stateSave: true,
        stateDuration: 60 * 60 * 24 * 30,
        fixedHeader: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            data: {
                'action': 'searchdata',
                'idrenc': idrenc
            },
            dataSrc: ""
        },
        columns: [
            {"data": "idusu"},
            {'data': 'fechoraini', "render":function(data){
                return moment(data).format('DD/MM/YYYY HH:mm:ss')}},
            {"data": "fechorafin", "render":function(data){
                return moment(data).format('DD/MM/YYYY HH:mm:ss')}},
            {"data": "tiempodif", "render":function(data){
                return String(data).replace("day","día")}},
            {"data": "formulario"},
            {"data": "accion", 'sClass': 'text-center pt-4', "render": function (data) {
                var zone_html = "";
                if (data === 1) {
                    zone_html = 'Cargar'
                }
                if (data === 2) {
                    zone_html = 'Conciliar'
                }
                if (data === 3) {
                    zone_html = 'Cambio de Datos'
                }
                if (data === 4) {
                    zone_html = 'Guardar'
                }
                if (data === 5) {
                    zone_html = 'Renumerar Páginas'
                }
                if (data === 6) {
                    zone_html = 'Cambiar Vista de Columnas'
                }
                if (data === 7) {
                    zone_html = 'Ver'
                }
                if (data === 8) {
                    zone_html = 'Ver Detalle Bco'
                }
                if (data === 9) {
                    zone_html = 'Ver Detalle ERP'
                }
                if (data === 10) {
                    zone_html = 'No Conservar Guardado'
                }
                return zone_html;
            }},
            {"data": "tiempodifacum", "render":function(data){
                return String(data).replace("day","día")}}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5,6],
                class: 'text-center pt-4',
                orderable: false
            }
        ],
    });
});