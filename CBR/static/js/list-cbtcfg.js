$(function () {
   

    "use strict"
    var table = $('#data').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        responsive: true,
        //order:[],
        autoWidth: true,
        destroy: true,
        hover: true,
        select: true,
        deferRender: true,
        searching: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
                },
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "ordencfg"},
            {"data": "codcfg"},
            {"data": "campobco"},
            {"data": "campoerp"},
            {"data": "actpas"}
        ],
        columnDefs: [

            {
                targets: [0, 1, 2, 3, 4],
                class: 'text-center pt-4',
                //orderable: false
            },
            {
                targets: [0],
                    createdCell: function (cell) {
                        var row = table.row(cell)
                        cell.id = 'prioridad'+row.data()["idtcfg"]
                        cell.setAttribute('contenteditable', true)
                            }
            },
            {
                targets: [2],
                    createdCell: function (cell) {
                        var row = table.row(cell)
                        if(row.data()["codcfg"]==3){
                            cell.id = 'campoBanco'+row.data()["idtcfg"]
                        cell.setAttribute('contenteditable', true)
                            }
                        }
            },
            {
                targets: [3],
                    createdCell: function (cell) {
                        var row = table.row(cell)
                        if(row.data()["codcfg"]==3){
                            cell.id = 'campoERP'+row.data()["idtcfg"]
                        cell.setAttribute('contenteditable', true)
                            }
                        }
            },
            {
                targets: [4],
                render: function (data, type, row, meta) {
                    if(row['actpas']=="A"){
                        return '<input id="actpas'+meta.row + '" class="form-control" type="checkbox" checked>'
                    }else{
                        return '<input id="actpas'+meta.row + '" class="form-control" type="checkbox">'
                    }
                }
            }
            
        ],
        


        initComplete: function (settings, json) {
            var inputs = document.getElementsByTagName("input");
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
            $(document).on("change", inputs, function (event) {
                let data={}
                data["fila"] = event.target["id"]
                data["checked"] = document.getElementById(data["fila"]).checked
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
