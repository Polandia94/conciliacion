$(function () {
    "use strict"
    const urlParams = new URLSearchParams(window.location.search);
    const idrbcoe = urlParams.get('idrbcoe');
    $('#data').DataTable({
        targets: 'no-sort',
        //bSort: false,
        order: [],
        responsive: true,
        autoWidth: true,
        destroy: true,
        hover: true,
        deferRender: true,
        colReorder: true,
        orderFixed: [ 0, 'asc' ],
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
                'idrbcoe': idrbcoe
            },
            dataSrc: ""
        },
        columns: [
            {"data": "idrbcod"},
            {"data": "fechatra"},
            {"data": "horatra"},
            {"data": "oficina"},
            {"data": "desctra"},
            {"data": "reftra"},
            {"data": "codtra"},
            {"data": "debe", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {"data": "haber", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {"data": "saldo", render: $.fn.dataTable.render.number(',', '.', 2, '$')}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                class: 'text-center pt-4',
                orderable: false
            }
        ],
    });
});