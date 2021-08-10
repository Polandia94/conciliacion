$(function () {
    "use strict"
    $('#data').DataTable({
        responsive: true,
        autoWidth: true,
        destroy: true,
        hover: true,
        deferRender: true,
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
            {"data": "idrgale"},
            {"data": "fechact"},
            {"data": "fechatra"},
            {"data": "ref"},
            {"data": "glosa"},
            {"data": "debe"},
            {"data": "haber"},
            {"data": "saldo"},
            {"data": "fechacon"},
            {"data": "coderr"}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6, 7,8,9],
                class: 'text-center pt-4',
            }
        ],
    });
});