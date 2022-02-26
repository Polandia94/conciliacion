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
            url: '/getconfigsemi',
            // url: window.location.pathname,
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
            // {"data": "codcfg", "render": function (data, type, full, meta) {
            //     if (data == 1){
            //         return "Busqueda de importe del Erp en fechas posteriores del Banco"
            //     }else{
            //         if (data==2){
            //             return "Busqueda de importe del Banco en fechas posteriores del ERP"
            //         }else{
            //             if(data==3){
            //                 return "Compara campos del lado del Banco y ERP"
            //             }else{
            //             return data
            //             }
            //         }
            //     }
            //     }},
            {"data": "campobco"},
            {"data": "campoerp"},
            {"data": "campoper"},
            {"data": "indestado"},
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
                        if(row.data()["codcfg"]==3){
                        cell.setAttribute('contenteditable', true)
                        }
                        cell.addEventListener('blur', function (e) {
                            const csrftoken = getCookie('csrftoken');
                            let data={}
                            data["fila"] = "ordencfg-" + row.data()["idtcfg"]
                            data["value"] = e.target.textContent
                            $.ajax({
                                type: "POST",
                                url: '/updatecbtcfg/',
                                data: data,
                                headers: {
                                    'X-CSRFToken': csrftoken
                                }
                            })
                        })
                            }
            },
            {
                targets: [2],
                render: function (data, type, row, meta) {
                    if(table.row(meta.row).data()["codcfg"]==3){
                        let nombre = ""
                        switch(data){
                            case "desctra":
                                nombre = "Desc Trans"
                                break;
                            case "reftra":
                                nombre = "Ref Trans"
                                break;
                            case "codtra":
                                nombre = "Cod Trans"
                                break;
                            
                        }
                        let formulario = `
                        <td><nobr>
                        <select class="form-control" name="tipo" id="optionbco-${row['idtcfg']}">
                        <option selected hidden value="`+data+`">`+nombre+`</option>
                        <option value="desctra">Desc Trans</option>
                        <option value="reftra">Ref Trans</option>
                        <option value="codtra">Cod Trans</option>
                        </td></nobr>
                        `
                        return formulario
                    }
                    else{
                        return ""
                    }
                }
                    
            },
            {
                targets: [3],
                render: function (data, type, row, meta) {
                    if(table.row(meta.row).data()["codcfg"]==3){
                        let nombre = ""
                        switch(data){
                            case "nrocomperp":
                                nombre = "Num Compro Erp"
                                break;
                            case "auxerp":
                                nombre = "Auxiliar ERP"
                                break;
                            case "referp":
                                nombre = "Referencia ERP"
                                break;
                            case "glosaerp":
                                nombre = "Glosa"
                                break;
                            case "nrotraerp":
                                nombre = "Nro Trans Erp"
                                break;
                            
                        }
                        return `
                        <td><nobr>
                        <select class="form-control" name="tipo" id="optionerp-${row['idtcfg']}">
                        <option selected hidden value="`+data+`">`+nombre+`</option>
                        <option value="nrotraerp">Nro Trans Erp</option>
                        <option value="nrocomperp">Num Compro Erp</option>
                        <option value="auxerp">Auxiliar ERP</option>
                        <option value="referp">Referencia ERP</option>
                        <option value="glosaerp">Glosa</option>
                        </td></nobr>
                        `
                    }
                    else{
                        return ""
                    }
                }
            },
            {
                targets: [4],
                render: function (data, type, row, meta) {
                    if(row['actpas']=="A"){
                        return `<input id="actpas-${row['idtcfg']}" class="form-control" type="checkbox" checked>`
                    }else{
                        return `<input id="actpas-${row['idtcfg']}" class="form-control" type="checkbox">`
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
                data["value"] = document.getElementById(data["fila"]).value
                $.ajax({
                    type: "POST",
                    url: '/updatecbtcfg/',
                    data: data,
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                })
            })
            
        }
            })
    
            
            
            
})
