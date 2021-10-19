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
            {"data": "superusuario"},
            {"data": "usuario"},
            {"data": "empresa"},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [0],
                visible:false,
            },
            {
                targets: [1, 2],
                class: 'text-center pt-4',
            },
            {
                targets: [3],
                render: function (data, type, row) {
                    if(data.superusuario){
                        return '<input type="checkbox" class="form-control" checked disabled>'
                    }else{
                        if(data.permiso){
                            return '<input id="'+ data.usuario+'--'+data.empresa+'"type="checkbox" class="form-control" checked >'
                        }else{
                            return '<input id="'+ data.usuario+'--'+data.empresa+'"type="checkbox" class="form-control"  >'
                        }
                    }
                }


            }
            

        ],
        initComplete: function (settings, json) {
            var inputs = document.getElementsByTagName("input");
            console.log(inputs)
            const csrftoken = getCookie('csrftoken');
            $(document).on("click", inputs, function (event) {
                let data={}
                data["fila"] = event.target["id"]
                data["checked"] = document.getElementById(data["fila"]).checked
                console.log(data)
                $.ajax({
                    type: "POST",
                    url: '/updateCbtusue/',
                    data: data,
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                })
            })
        }
        
            
    })
    
        
})
