$(function () {
    "use strict"
    const urlParams = new URLSearchParams(window.location.search);
    const idrerpe = urlParams.get('idrerpe');
    $('#data').DataTable({
        targets: 'no-sort',
        //bSort: false,
        order: [],
        responsive: true,
        autoWidth: true,
        orderFixed: [ 0, 'asc' ],
        destroy: true,
        hover: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            data: {
                'action': 'searchdata',
                'idrerpe': idrerpe
            },
            dataSrc: ""
        },
        columns: [
            {"data": "idrerpd"},
            {"data": "nrotra"},
            {"data": "fechatra"},
            {"data": "nrocomp"},
            {"data": "aux"},
            {"data": "ref"},
            {"data": "glosa"},
            {"data": "debe", render: $.fn.dataTable.render.number(',', '.', 2, globalVariable.moneda)},
            {"data": "haber", render: $.fn.dataTable.render.number(',', '.', 2, globalVariable.moneda)},
            {"data": "saldo", render: $.fn.dataTable.render.number(',', '.', 2, globalVariable.moneda)},
            {"data": "fechacon"}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                class: 'text-center pt-4',
                orderable: false
            }
        ],
        initComplete: function (settings, json) {
        }
    });
});