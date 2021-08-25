$(function () {
    "use strict"
    $('#data').DataTable({
        targets: 'no-sort',
        bSort: false,
        order: [],
        responsive: true,
        autoWidth: true,
        destroy: true,
        hover: true,
        deferRender: true,
        orderFixed: [ 0, 'asc' ],
        colReorder: true,
        stateSave: true,
        fixedHeader: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            data: {
                'action': 'searchdata',
            },
            dataSrc: ""
        },
        columns: [

            {"data": "diatra"},
            {"data": "oficina"},
            {"data": "desctra"},
            {"data": "debe"},
            {"data": "haber"},
            {"data": "saldo"},
            {"data": "coderr"}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6],
                class: 'text-center pt-4',
                orderable: false
            }
        ],
    });
});