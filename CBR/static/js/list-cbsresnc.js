$(function () {
    "use strict"
    var table = $('#data').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        responsive: true,
        autoWidth: true,
        destroy: true,
        hover: true,
        select: true,
        deferRender: true,
        searching: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "tipo"},
            {"data": "codcon"},
            {"data": "indpend",  "render": function (data, type, full, meta) {

                if(data==0){
                    return "No"
                    }
                else if(data==1){
                    return "Si"
                }else{
                    return data
                }
            
                }
            },
            {"data": "fecha"},
            {"data": "id"},
            {"data": "documento"},
            {"data": "glosa"},
            {"data": "debe"},
            {"data": "haber"},
        ],
        columnDefs: [
            {
                targets: [0,1,2,3,4,5,6],
                class: 'text-center pt-4',
            },
            {
                targets: [7,8],
                class: 'text-center pt-4',
                render: function (data, type, row) {
                    return globalVariable.moneda + parseFloat(data).toLocaleString('en-US', {minimumFractionDigits:2})
                }
            },
            
            
            

        ],
        
        
             
    })
    
        
})
