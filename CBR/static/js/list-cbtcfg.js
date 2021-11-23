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
            {"data": "codcfg", "render": function (data, type, full, meta) {
                if (data == 1){
                    return "Busqueda de importe en fechas posteriores del Banco"
                }else{
                    if (data==2){
                        return "Busqueda de importe en fechas posteriores del ERP"
                    }else{
                        if(data==3){
                            return "Compara campos del lado del Banco y ERP"
                        }else{
                        return data
                        }
                    }
                }
                }},
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
                            case "oficina":
                                nombre = "oficina"
                                break;
                            case "desctra":
                                nombre = "Descripcion de Transaccion"
                                break;
                            case "reftra":
                                nombre = "Referencia de Transaccion"
                                break;
                            case "codtra":
                                nombre = "Codigo de transaccion"
                                break;
                            
                        }
                        let formulario = `
                        <td><nobr>
                        <select class="form-control" name="tipo" id="optionbco-${row['idtcfg']}">
                        <option selected hidden value="`+data+`">`+nombre+`</option>
                        <option value="oficina">oficina</option>
                        <option value="desctra">Descripcion de Transaccion </option>
                        <option value="reftra">Referencia de Transaccion</option>
                        <option value="codtra">Codigo de transaccion</option>
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
                                nombre = "Numero de Comprobante"
                                break;
                            case "auxerp":
                                nombre = "Auxiliar"
                                break;
                            case "referp":
                                nombre = "Referencia de Transaccion"
                                break;
                            case "glosaerp":
                                nombre = "Glosa"
                                break;
                            
                        }
                        return `
                        <td><nobr>
                        <select class="form-control" name="tipo" id="optionerp-${row['idtcfg']}">
                        <option selected hidden value="`+data+`">`+nombre+`</option>
                        <option value="nrocomperp">Numero de Comprobante</option>
                        <option value="auxerp">Auxiliar </option>
                        <option value="referp">Referencia de Transaccion</option>
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
                console.log(data)
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
