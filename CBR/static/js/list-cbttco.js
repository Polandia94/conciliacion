

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
            {"data": "position"},
            {"data": "erpbco"},
            {'data': 'indsum'},
            {"data": "codtco"},
            {'data': 'debe', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {'data': 'haber', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {'data': 'saldoacumulado', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            
        ],
        columnDefs: [
            {
                targets: [3, 4, 5,6],
                class: 'text-center pt-4',
                orderable: false,
                createdCell: function (cell){
                    var row = table.row(cell)
                    try{
                        var tr = $(cell);
                        if(row.data()["indsum"]){
                            tr.css('color', 'black');
                        }else{
                            tr.css('color', 'gray');
                        }
                    }
                    catch{}

                }
            },
            {   
                targets: [0,1,2],
                visible: false,
                searchable: false
            },
                
        ],
        rowCallback: function( row, data, index ) {
            if (data["erpbco"] == 2) {
                $(row).hide();
            }
}
    });
    let table2 = $('#data2').DataTable({
        targets: 'no-sort',
        bSort: false,
        order: [],
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
            {"data": "position"},
            {"data": "erpbco"},
            {'data': 'indsum'},
            {"data": "codtco"},
            {'data': 'debe', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {'data': 'haber', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            {'data': 'saldoacumulado', render: $.fn.dataTable.render.number(',', '.', 2, '$')},
            
        ],
        columnDefs: [
            {
                targets: [3, 4, 5,6],
                class: 'text-center pt-4',
                orderable: false,
                createdCell: function (cell){
                    var row = table2.row(cell)
                    try{
                        var tr = $(cell);
                        if(row.data()["indsum"]){
                            tr.css('color', 'black');
                        }else{
                            tr.css('color', 'gray');
                        }
                    }
                    catch{}

                }
            },
            {   
                targets: [0,1,2],
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
