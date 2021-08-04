$(function () {
    "use strict"
    const urlParams = new URLSearchParams(window.location.search);
    const tabla = urlParams.get('tabla');
    $('#data').DataTable({
        responsive: true,
        autoWidth: true,
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
                'tabla': tabla
            },
            dataSrc: ""
        },
        columns: [
            {"data": "idterr"},
            {"data": "coderr"},
            {"data": "fechact"},
            {"data": "idusu"}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3],
                class: 'text-center pt-4',
            }
        ],
        initComplete: function (settings, json) {
        }
    });
});