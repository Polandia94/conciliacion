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
        orderFixed: [ 0, 'asc' ],
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
            {"data": "fechact", "render":function(data){
                return moment(data).format('DD/MM/YYYY')}},
            {"data": "fechact", "render":function(data){
                return moment(data).format('HH : mm')}},
            {"data": "idusu"},
            {'data': 'status', 'sClass': 'text-center pt-4', "render": function (data, type, full, meta) {
                var zone_html = "";
                if (data == "0") {
                    zone_html = 'Cargado'
                }
                if (data == "1") {
                    zone_html = 'Editado'
                }
                if (data == "2") {
                    zone_html = 'Conciliado'
                }
                if (data == "3") {
                    zone_html = 'Eliminado'
                }
                return zone_html;
                }
            },
            {"data": "saldobco", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {"data": "saldoerp", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {"data": "difbcoerp", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {"data": "glosa"}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6,7],
                class: 'text-center pt-4',
                orderable: false
            }
        ],
    });
});