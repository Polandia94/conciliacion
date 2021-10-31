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
            {"data": "codcol"},
            {"data": "descol"},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [0],
                visible:false,
            },
            {
                targets: [1],
                class: 'text-center pt-4',
            },
            {
                targets: [2],
                class: 'text-center pt-1',
                render: function (data, type, row) {

                        if(data.inddef == 1){
                            return '<input id="'+ data.codcol+'"type="checkbox"class="form-control" checked >'
                        }else{
                            return '<input id="'+ data.codcol+'"type="checkbox" class="form-control"  >'
                        }
                    }
                


            }
            

        ],
        initComplete: function (settings, json) {
            var inputs = document.getElementsByTagName("input");
            const csrftoken = getCookie('csrftoken');
            $(document).on("click", inputs, function (event) {
                let data={}
                data["codcol"] = event.target["id"]
                data["checked"] = document.getElementById(data["codcol"]).checked
                $.ajax({
                    type: "POST",
                    url: '/updatecbtusuc/',
                    data: data,
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                })
            })
        }
        
            
    })
    
        
})
