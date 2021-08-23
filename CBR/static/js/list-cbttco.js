

$(function () {
    "use strict"
    const urlParams = new URLSearchParams(window.location.search);
    const idrenc = urlParams.get('idrenc');
    let table = $('#data').DataTable({
        searching: false, 
        paging: false, 
        info: false,
        responsive: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,
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
                'idrenc': idrenc
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "erpbco"},
            {"data": "codtco"},
            {'data': 'debe'},
            {'data': 'haber'},
            {'data': 'saldoacumulado'}
        ],
        columnDefs: [
            {
                targets: [2, 3, 4, 5],
                class: 'text-center pt-4',
                orderable: false
            },
            {   
                targets: [0,1],
                visible: false,
                searchable: false}
        ],
        rowCallback: function( row, data, index ) {
            if (data["erpbco"] == 2) {
                $(row).hide();
            }
}
    });
    let table2 = $('#data2').DataTable({
        searching: false, 
        paging: false, 
        info: false,
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
                'idrenc': idrenc
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "erpbco"},
            {"data": "codtco"},
            {'data': 'debe'},
            {'data': 'haber'},
            {'data': 'saldoacumulado'}
        ],
        columnDefs: [
            {
                targets: [2, 3, 4, 5],
                class: 'text-center pt-4',
                orderable: false
            },
            {   
                targets: [0,1],
                visible: false,
                searchable: false}
        ],
        rowCallback: function( row, data, index ) {
            if (data["erpbco"] == 1) {
                $(row).hide();
            }
}
    });
});
