var globalVariable={
    editado: 0,
    SaldoDiferenciaTotal:0
 };
 var globalVariableSaldo={
    saldo: 0
 };

$(function () { "use strict"
    $(document).ready(function() {
        const searchRegExp = /,/g;
        const csrftoken = getCookie('csrftoken');
        function calcularSaldos(original, row, e, estadooriginal){

            let totaldebe = parseFloat(0);
            let totalhaber = parseFloat(0);
                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                if(row.data()['idrbcodl']==-2 && original != e.target.textContent){
                                    row.data()['estadoerp']=0,
                                    row.data()['estadobco']=0,
                                    row.data()['idrbcodl']=0,
                                    row.data()['idrerpdl']=0
                                };
                                try{
                                    if (table.cell(row,".haberbco").data() != null){
                                    if(parseFloat(table.cell(row,".debeerp").data().replace("$",""))==parseFloat(table.cell(row,".haberbco").data().replace("$","")) &&  parseFloat(table.cell(row,".debebco").data().replace("$",""))==parseFloat(table.cell(row,".habererp").data().replace("$",""))){
                                        row.data()['estadoerp']=1,
                                        row.data()['estadobco']=1,
                                        row.data()['idrbcodl']=-2,
                                        row.data()['idrerpdl']=-2}};
                                    }
                                catch{}
                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {
                                let totalmasdebe = parseFloat(0)
                                let totalmashaber = parseFloat(0)


                                if(table.cell(fila,".debeerp").data() == null || table.cell(fila,".debeerp").data() == 0){
                                    totalmasdebe = parseFloat(0)
                                    totaldebe = totaldebe + totalmasdebe   
                                } else{
                                    totalmasdebe = parseFloat(table.cell(fila,".debeerp").data().replace("$",""))
                                    totaldebe = totaldebe + totalmasdebe
                                }
                                if(table.cell(fila,".habererp").data() == null || table.cell(fila,".habererp").data() == 0){
                                    totalmashaber = parseFloat(0)
                                    totalhaber = totalhaber + totalmashaber   
                                } else{
                                    totalmashaber = parseFloat(table.cell(fila,".habererp").data().replace("$",""))
                                    totalhaber = totalhaber + totalmashaber
                                }
                                let saldomas = parseFloat(0)
                                if (table.cell(fila,".debeerp").data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,".debeerp").data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,".habererp").data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,".habererp").data())}
                                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                table.cell( fila,".saldoacumeserp" ).data(saldoi);

                                var saldodiferencia = parseFloat(table.cell(row,".saldoacumesbco").data().replace("$","")) - parseFloat(table.cell(row,".saldoacumeserp").data())
                                table.cell( row,".saldodiferencia" ).data(saldodiferencia);                                if (table.cell(fila-1,".fechatraerp").data()==table.cell(fila,".fechatraerp").data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,".saldoacumdiaerp" ).data(saldodia);
                                var rows = table.row(fila)
                                try{saldodiferenciahtml.innerHTML = Number(saldodiferencia).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                catch{}
                                try{saldoerphtml.innerHTML = Number(saldoi).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                catch{}
                                try{debeerphtml.innerHTML = Number(totaldebe).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                catch{}
                                try{habererphtml.innerHTML = Number(totalhaber).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                catch{}

                                datasend.push(rows.data());
                                }
                                if(row.data()["idrbcodl"]==-1){row.data()["idrbcodl"]=0}
                                table.rows( function ( idx, data, node ) { 
                                    var rowg = table.row(idx)
                                    if(rowg.data()["idrbcod"]==row.data()["idrbcodl"] && rowg.data()["idrerpdl"]==-1){rowg.data()["idrerpdl"]=0}})
                                var debeerp = 0
                                    var habererp = 0
                                    var aConciliarVarios = 0
                                    /*  
                                      Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                    */
    
                                    /*  
                                      Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                    */
                                    table.rows( function ( idx, data, node ) {
                                        if(data.idrbcodl == row.data()["idrbcodl"]){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == row.data()["idrbcodl"] && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["idrbcodl"] == row.data()["idrbcodl"]){
                                                            rowc.data()["estadoerp"]=1
                                                        }
                                                        if(aConciliarVarios>1){rowb.data()['idrerpdl']=-1}else if(aConciliarVarios==1 && rowb.data()['idrbcodl'] == 0){
                                                            rowb.data()['idrbcodl']=rowc.data()['idrbcod']
                                                        }
                                                    });
                                                    rowb.data()['estadobco']=1
                                                }else if(rowb.data()['idrbcod'] == row.data()["idrbcodl"]){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["idrbcodl"] == row.data()["idrbcodl"]){
                                                                rowc.data()["estadoerp"]=0
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                }
                                    });

                                if(row.data()["estadoerp"]==1){
                                    row.data()["historial"]="4"                                                
                                                table.rows(function ( idx, data, node ) {
                                                    var rowx = table.row(idx)
                                                    if(rowx.data()["idrbcod"] == row.data()["idrbcodl"] && rowx.data()["fechatrabco"] != row.data()["fechatraerp"]){
                                                        row.data()['historial']="2"
                                                    }

                                                })
                                }else{
                                    row.data()["historial"]="1"
                                }
                                if(estadooriginal == "2" || estadooriginal == "3" || estadooriginal == "4"){
                                    if(row.data()["estadoerp"]==0){
                                    row.data()["historial"]="5"}
                                }
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                table.rows().invalidate().draw(false);                         



                            $.ajax({
                                type: "POST",
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace("$", ""),
                                headers: {
                                    'X-CSRFToken': csrfToken
                                  },
                                success: function(response){
                                    $.ajax({
                                        method: 'GET',
                                        beforeSend: function (request) {
                                            request.setRequestHeader("X-CSRFToken", csrftoken);
                                        },
                                        url: '/getTiposDeConciliacionpost',
                                        data: {'idrenc': idrenc},
                                        success: function (respons) {
                                            try{debebcototal.innerHTML = Number(respons.debebcototal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            try{haberbcototal.innerHTML = Number(respons.haberbcototal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            try{saldobcototal.innerHTML = Number(respons.saldobcototal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            try{debeerptotalhtml.innerHTML = Number(respons.debeerptotal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{console.log("error al cargar " + respons.debeerptotal + "como debeerptotal")}
                                            try{habererptotalhtml.innerHTML = Number(respons.habererptotal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            try{saldoerptotalhtml.innerHTML = Number(respons.saldoerptotal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            try{saldodiferenciatotalhtml.innerHTML = Number(respons.saldodiferenciatotal).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})}
                                            catch{}
                                            globalVariable.SaldoDiferenciaTotal = Number(respons.saldodiferenciatotal)
                                            cargando.innerHTML = "Listo"
                                            }})
                                }
                            })
                            cargando.innerHTML = "Cargando"

                        
                            
                           
                        
                         
        }
        function resaltarerp(e){
            var row = table.row(e.target.parentElement)
                                    if(row.data()["idrerpdl"] ==-1){
                                        table.rows( function ( idx, data, node ) {
                                            var rowe = table.row(idx)
                                            if(row.data()["idrbcod"]==rowe.data()["idrbcodl"] && row.data()["idrbcod"] != 0 && row.data()["idrbcod"] != ""){
                                                $(table.cells(rowe, [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]).nodes()).css({ "background-color": "#84cf84"});
                                            }

                                        })
                                    }else{
                                    table.rows( function ( idx, data, node ) {
                                        var rowe = table.row(idx)
                                        if(row.data()["idrerpdl"]==rowe.data()["idrerpd"] && row.data()["idrerpdl"] != 0 && row.data()["idrerpdl"] != ""){
                                            $(table.cells(rowe, [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]).nodes()).css({ "background-color": "#84cf84" });
                                        }

                                    })
                                    }
                                }
        
        function desresaltarerp(e){
            var row = table.row(e.target.parentElement)
                                    if(row.data()["idrerpdl"] ==-1){
                                        table.rows( function ( idx, data, node ) {
                                            var rowe = table.row(idx)
                                            if(row.data()["idrbcod"]==rowe.data()["idrbcodl"] && row.data()["idrbcod"] != 0 && row.data()["idrbcod"] != ""){
                                                $(table.cells(rowe, [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]).nodes()).css({ "background-color": "" });
                                            }

                                        })
                                    }else{
                                    table.rows( function ( idx, data, node ) {
                                        var rowe = table.row(idx)
                                        if(row.data()["idrerpdl"]==rowe.data()["idrerpd"] && row.data()["idrerpdl"] != 0 && row.data()["idrerpdl"] != ""){
                                            $(table.cells(rowe, [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]).nodes()).css({ "background-color": "" });
                                        }
                                    })
                                    }
                                }
        function resaltarbco(e){
            var row = table.row(e.target.parentElement)
            if(row.data()["idrbcodl"] ==-1){
                table.rows( function ( idx, data, node ) {
                    var rowe = table.row(idx)
                    if(row.data()["idrerpd"]==rowe.data()["idrerpdl"] && row.data()["idrerpd"] != 0 && row.data()["idrerpd"] != ""){
                        $(table.cells(rowe,[1,2,3,4,5,6,7,8,9,10,11,12,13,14]).nodes()).css({ "background-color": "#84cf84" });
                    }

                })
            }else{
            table.rows( function ( idx, data, node ) {
                var rowe = table.row(idx)
                if(row.data()["idrbcodl"]==rowe.data()["idrbcod"] && row.data()["idrbcodl"] != 0 && row.data()["idrbcodl"] != ""){
                    $(table.cells(rowe,[1,2,3,4,5,6,7,8,9,10,11,12,13,14]).nodes()).css({ "background-color": "#84cf84" });
                }
            })
            }
        }
        function desresaltarbco(e){
            var row = table.row(e.target.parentElement)
                            if(row.data()["idrbcodl"] ==-1){
                                table.rows( function ( idx, data, node ) {
                                    var rowe = table.row(idx)
                                    if(row.data()["idrerpd"]==rowe.data()["idrerpdl"] && row.data()["idrerpd"] != 0 && row.data()["idrerpd"] != ""){
                                        $(table.cells(rowe,[1,2,3,4,5,6,7,8,9,10,11,12,13,14]).nodes()).css({ "background-color": "" });
                                    } 
                                })
                            }else{
                            table.rows( function ( idx, data, node ) {
                                var rowe = table.row(idx)
                                if(row.data()["idrbcodl"]==rowe.data()["idrbcod"] && row.data()["idrbcodl"] != 0 && row.data()["idrbcodl"] != ""){
                                    $(table.cells(rowe,[1,2,3,4,5,6,7,8,9,10,11,12,13,14]).nodes()).css({ "background-color": "" });
                                }
                            })
                        }
                    }

        globalVariable.editado = 0;
        globalVariableSaldo.saldo = 0;
        try{globalVariable.SaldoDiferenciaTotal = parseFloat(document.getElementById("saldodiferenciatotalhtml").textContent.substring(1))}
        catch{}
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
        let maximosCaracteres = 25;

        let table = $('#data').DataTable({
            
            deferRender: true,
            colReorder: true,
            stateSave: true,
            stateDuration: 60 * 60 * 24 * 30,
            fixedHeader:{            
                header: true,
                footer: true},

            dom: 'lBfrtip',
            language: {
                url: '../static/lib/datatables-es.json'
            },
            buttons: [
                'copy', 'csv', 'excel', 'print',
                {
                    extend: ['colvis'],
                    collectionLayout: 'fixed three-column',
                    columns: ':not(.noVis)',
                }
            ],

            stripeClasses: [],
            autoWidth: false,
            destroy: true,
            hover: true,
            select: true,
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
                {"data": "idsres", className: "dt-comunColor"},
                {"data": "fechatrabco", name: "fechatrabco", className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    if(data!=null){
                    return "<td><nobr>" + data + "</nobr></td>"}else{return""}
                    }},
                {"data": "horatrabco", className: "dt-bancoColor" },
                {"data": "debebco", name: "debebco", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}, className: "dt-bancoColor" },
                {"data": "haberbco", name: "haberbco", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}, className: "dt-bancoColor" },
                {"data": "saldobco", name: "saldobco", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}, className: "dt-bancoColor" },
                {
                    "data": "saldoacumesbco",
                    name: "saldoacumesbco",
                    render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}, 
                    className: "dt-bancoColor" 
                },
                {
                    "data": "saldoacumdiabco",
                    name: "saldoacumdiabco",
                    render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}, 
                    className: "dt-bancoColor" 
                },
                {"data": 'oficina', className: "dt-bancoColor" },
                {"data": 'desctra', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > maximosCaracteres) {
                        zone_html = data.substring(0,maximosCaracteres-7)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'reftra', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > maximosCaracteres) {
                        zone_html = data.substring(0,maximosCaracteres-7)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'codtra', className: "dt-bancoColor" },
                {"data": 'idrbcod', className: "dt-bancoColor" },
                
                {"data": 'estadobco', className: "dt-comunColor" },
                {"data": 'codtcobco', className: "dt-comunColor" },
                {"data": 'idrerpdl', className: "dt-comunColor"},
                
                {"data": 'estadoerp', className: "dt-comunColor"},
                {"data": 'codtcoerp', className: "dt-comunColor"},
                {"data": 'idrbcodl', className: "dt-comunColor"},                
                {"data": 'idrerpd'},
                {"data": "fechatraerp", name: "fechatraerp", "render": function (data, type, full, meta) {
                    if(data!=null){
                    return "<td><nobr>" + data + "</nobr></td>"}else{return""}
                    }},
                {"data": "debeerp", name: "debeerp", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}},
                {"data": "habererp", name: "habererp", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}},
                {"data": "saldoerp", name: "saldoerp", render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}},
                {
                    "data": "saldoacumeserp",
                    name: "saldoacumeserp",
                    render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}
                },
                {
                    "data": "saldoacumdiaerp",
                    name: "saldoacumdiaerp",
                    render: function (data, type, full, meta) {if(data != null){return "$" + data.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}else{return ""}}
                },
                {"data": "saldodiferencia", name: "saldodiferencia", render: $.fn.dataTable.render.number( ',', '.', 2, '$' )},
                
                {"data": 'nrotraerp'},
                {"data": 'nrocomperp', "render": function (data, type, full, meta) {
                    if(data!=null){
                    return "<td><nobr>" + data + "</nobr></td>"}else{return""}
                    }},
                {"data": 'auxerp'},
                {"data": 'referp', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > maximosCaracteres) {
                        zone_html = data.substring(0,maximosCaracteres-7)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'glosaerp', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > maximosCaracteres) {
                        zone_html = data.substring(0,maximosCaracteres-7)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'fechaconerp', "render": function (data, type, full, meta) {
                    if(data!=null){
                    return "<td><nobr>" + data + "</nobr></td>"}else{return""}
                    }},
                
                {"data": 'historial', className: "dt-comunColor", "render": function (data, type, full, meta) {
                    var zone_html = ""; 
                    if (data === "0") {
                        zone_html = 'Original'
                    }
                    if (data === "1") {
                        zone_html = 'Modificado'
                    }
                    if (data === "2") {
                        zone_html = 'Conciliado otra fecha'
                    }
                    if (data === "3") {
                        zone_html = 'Conciliado'
                    }
                    if (data === "4") {
                        zone_html = 'Modificado y Conciliado'
                    }
                    if (data === "5") {
                        zone_html = 'Desconciliado'
                    }
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }
                },

            ],
            columnDefs: [
                {targets: [2,8,10,11,12,13],
                    createdCell: function (cell){
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {  targets: [16,19,20,23,24,25,26,27,28,29,30,31,32],
                    createdCell: function (cell){
                        cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                    }
                },
                {
                    targets: ['fechatrabco'],
                    createdCell: function (cell) {
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})

                        $(cell).attr("data-look", 'fechatraerp');
                    }
                },
                {
                    targets: ["debebco"],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'habererp');
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {
                    targets: ["haberbco"],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'debeerp');
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {
                    targets: ["saldobco"],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoerp');
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {
                    targets: ["saldoacumesbco"],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumeserp');
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {
                    targets: ["saldoacumdiabco"],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumdiaerp');
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {
                    targets: ["desctra"],
                    createdCell: function (cell) {
                        var row = table.row(cell)
                        if(table.column(cell).visible() === true){
                            if(row.data()['desctra']!=null && row.data()['desctra'].length > maximosCaracteres){
                                $(cell).attr("title", row.data()['desctra'])
                            };
                        }
                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                },
                {targets: ["referp"],
                createdCell: function (cell) {
                    var row = table.row(cell)
                    if(table.column(cell).visible() === true){
                    if(row.data()['referp']!=null && row.data()['referp'].length > maximosCaracteres){
                        $(cell).attr("title", row.data()['referp'])
                        };
                        cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                    }
                }
                    
                },
                {targets: ["glosaerp"],
                createdCell: function (cell) {
                    var row = table.row(cell)
                    if(table.column(cell).visible() === true){
                    if(row.data()['glosaerp']!=null && row.data()['glosaerp'].length > maximosCaracteres){
                        $(cell).attr("title", row.data()['glosaerp'])
                        };
                        cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                    }
                }
                },
                {targets: ["codtcobco"],
                    createdCell: function (cell) {

                        cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})

                    }
                    },
                    {
                        targets: ["codtcoerp"],
                    createdCell: function (cell) {
                        
                            
                                            
                        
                        cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                        cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})

                    }
                    },
                {
                    targets: ["idrerpdl"],
                    createdCell: function (cell) {
                        let original
                        var row = table.row(cell)
                        if(table.column(cell).visible() === true){
                            if(row.data()["estadobco"]==1){
                                var $elDiv = $('<div></div>');
                                $elDiv.children().addClass('callout callout-conc m-0 pt-0 h-100 w-100 ')
                            }
                            cell.setAttribute('spellcheck', false)

                            cell.addEventListener('focus', function(e) {
                                var row = table.row(e.target.parentElement)
                                original = row.data()["idrerpdl"]
                                desresaltarerp(e)
                            })
                        }

                        cell.addEventListener('blur', function(e) {
                            e.target.textContent = e.target.textContent.substring(0,10)
                            var row = table.row(e.target.parentElement)
                            if (original !== e.target.textContent) {
                            if(original == -1 || e.target.textContent < 0 || Number.isInteger(parseInt(e.target.textContent)) == false){
                                e.target.textContent = original
                                row.invalidate().draw(false)
                            }else{                                
                                var existe = false
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == e.target.textContent){
                                        if(rowb.data()['idrbcodl'] < 1 || rowb.data()['idrbcodl']== null){
                                        existe = true}} });                                   
                                if(e.target.textContent == 0){existe = true}
                                    /*  
                                  Si el valor es numero pasa a ser rojo, la variable editado se activa
                                */
                            if(existe){ 
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                row.data()['idrerpdl']=e.target.textContent
                                var debebco = 0
                                var haberbco = 0
                                var aConciliarVarios = 0
                                if(original>0){
                                    table.rows( function ( idx, data, node ) {
                                    var rowe = table.row(idx)
                                    if(rowe.data()["idrbcodl"]==row.data()["idrbcod"]){
                                        rowe.data()["idrbcodl"] = 0
                                    }
                                })}
                                /*  
                                  Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                */

                                /*  
                                  Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                */
                                table.rows( function ( idx, data, node ) {
                                    if(data.idrerpdl == e.target.textContent){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debebco = debebco + parseFloat(rowc.data()['debebco'])
                                        haberbco = haberbco + parseFloat(rowc.data()['haberbco'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == e.target.textContent && rowb.data()['debeerp'] == haberbco && rowb.data()['habererp'] == debebco && (debebco != 0 || haberbco != 0)){                                           
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["idrerpdl"] == e.target.textContent){
                                                        rowc.data()["estadobco"]=1
                                                    }});
                                                rowb.data()['estadoerp']=1
                                                rowb.data()['historial']="4"
                                                table.rows(function ( idx, data, node ) {
                                                    var rowx = table.row(idx)
                                                    if(rowx.data()["idrbcod"] == rowb.data()["idrbcodl"] && rowx.data()["fechatrabco"] != rowb.data()["fechatraerp"]){
                                                        rowb.data()['historial']="2"
                                                    }

                                                })
                                                
                                                if(aConciliarVarios>1){rowb.data()['idrbcodl']=-1}else if(aConciliarVarios==1){rowb.data()['idrbcodl']=row.data()['idrbcod']}
                                            }else if(rowb.data()['idrerpd'] == e.target.textContent){
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["idrerpdl"] == e.target.textContent){
                                                            rowc.data()["estadobco"]=0
                                                        }});
                                                    rowb.data()['estadoerp']=0
                                                    if(rowb.data()['historial']=="2" || rowb.data()['historial']=="3" || rowb.data()['historial']=="4"){
                                                        rowb.data()['historial']="5"}
                                                    rowb.data()['idrbcodl']=0
                                            }
                                });
                                row = table.row(e.target.parentElement)
                                debebco = 0
                                haberbco = 0
                                aConciliarVarios = 0
                                /*  
                                  Se realiza lo mismo con el original que se modifico
                                */

                                /*  
                                  Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                */
                                
                                table.rows( function ( idx, data, node ) {
                                    if(data.idrerpdl == original && original != 0){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debebco = debebco + parseFloat(rowc.data()['debebco'])
                                        haberbco = haberbco + parseFloat(rowc.data()['haberbco'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == original && original != 0 && (debebco != 0 || haberbco != 0)){
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["idrerpdl"] == original && original != 0){
                                                        rowc.data()["estadobco"]=1
                                                    }});
                                                rowb.data()['estadoerp']=1
                                                rowb.data()['historial']="4"
                                                table.rows(function ( idx, data, node ) {
                                                    var rowx = table.row(idx)
                                                    if(rowx.data()["idrbcod"] == rowb.data()["idrbcodl"] && rowx.data()["fechatrabco"] != rowb.data()["fechatraerp"]){
                                                        rowb.data()['historial']="2"
                                                    }

                                                })
                                                if(aConciliarVarios>1){rowb.data()['idrbcodl']=-1}else if(aConciliarVarios==1){rowb.data()['idrbcodl']=row.data()['idrbcod']}
                                            }if(rowb.data()['idrerpd'] == original && original != 0){
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["idrerpdl"] == original && original != 0){
                                                            rowc.data()["estadobco"]=0
                                                        }});
                                                    rowb.data()['estadoerp']=0
                                                    if(rowb.data()['historial']=="2" || rowb.data()['historial']=="3" || rowb.data()['historial']=="4"){
                                                        rowb.data()['historial']="5"}
                                                    rowb.data()['idrbcodl']=0
                                            }
                                });

                                table.rows().invalidate().draw(false);
                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {
                                var rows = table.row(fila)
                                datasend.push(rows.data());
                                }

                                
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                            $.ajax({
                                type: "POST",
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/[]/g, ""),
                                headers: {
                                    'X-CSRFToken': csrfToken
                                  }
                            })    
                        }else{e.target.textContent= original}}
                        }
                        row.invalidate().draw(false)
                          })
                          cell.addEventListener('mouseenter', function(e) {resaltarerp(e)})
                          cell.addEventListener('mouseleave', function(e) {desresaltarerp(e)})
                    }
                    
                },
                {
                    targets: ["debeerp"],
                    createdCell: function (cell) {

                        $(cell).attr("data-look", 'haberbco');
                        let original
                        let estadooriginal
                        let saldo = parseFloat(0);
                        var row = table.row(cell)
                        if((table.cell(row,".historial").data() == "1" || table.cell(row,".historial").data() == "4")&& table.cell(row,".debeerp").data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        saldo = parseFloat(table.cell( 0,".saldoacumeserp" ).data())-parseFloat(table.cell( 0,".debeerp" ).data())+parseFloat(table.cell( 0,".habererp" ).data())
                        for (let fila = 1; isNaN(saldo); fila++) {
                            saldo = parseFloat(table.cell( fila,".saldoacumeserp" ).data())-parseFloat(table.cell( fila,".debeerp" ).data())+parseFloat(table.cell( fila,".habererp" ).data())
                        }
                        globalVariableSaldo.saldo = saldo
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent
                            estadooriginal =  row.data()["historial"]
                        })
                        cell.addEventListener('blur', function(e) {
                            var row = table.row(e.target.parentElement)
                            if ( original == null || row.data()['habererp'] != 0 || row.data()['estadoerp'] == "1"){
                                e.target.textContent = original
                            }
                            else if (original !== e.target.textContent) {
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1

                                row.data()['debeerp']=e.target.textContent.replace("$","").replace(searchRegExp,"")
                                calcularSaldos(original, row, e, estadooriginal)   
                        }
                        
                          })
                          cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                          cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                    }
                },
                {
                    targets: ["habererp"],
                    createdCell: function (cell) {

                        $(cell).attr("data-look", 'debebco');
                        let estadooriginal
                        let original
                        var row = table.row(cell)
                        if((table.cell(row,".historial").data() == "1" || table.cell(row,".historial").data() == "4")&& table.cell(row,".debeerp").data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent
                            estadooriginal =  row.data()["historial"]

                        })
                        cell.addEventListener('blur', function(e) {
                            var row = table.row(e.target.parentElement)
                            if ( original == null || row.data()['debeerp'] != 0 || row.data()['estadoerp'] == 1){
                                e.target.textContent = original
                            }else{
                            if (original !== e.target.textContent) {

                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                row.data()['habererp']=e.target.textContent.replace("$","").replace(searchRegExp,"")
                                calcularSaldos(original, row, e, estadooriginal) 
                        }
                          }})
                          cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                          cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                    }
                },
            
                    {
                        targets: ["idrbcodl"],
                        createdCell: function (cell) {
                            let original
                            let estadooriginal

                            cell.setAttribute('spellcheck', false)
    
                            cell.addEventListener('focus', function(e) {
                                var row = table.row(e.target.parentElement)
                                original = row.data()["idrbcodl"]
                                estadooriginal =  row.data()["historial"]
                                desresaltarbco(e)

                            })
    
                            cell.addEventListener('blur', function(e) {

                                e.target.textContent = e.target.textContent.substring(0,10)
                                var row = table.row(e.target.parentElement)
                                if (original !== e.target.textContent) {
                                if(original == -1 || e.target.textContent < 0 || Number.isInteger(parseInt(e.target.textContent)) == false){
                                    e.target.textContent = original
                                    row.invalidate().draw(false);
                                }else{                                
                                var existe = false
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == e.target.textContent){
                                            if(rowb.data()['idrerpdl'] < 1 || rowb.data()['idrerpdl'] == null){
                                            existe = true} }});                                   
                                    if(e.target.textContent == 0){existe = true}
                                        /*  
                                      Si el valor es numero pasa a ser rojo, la variable editado se activa
                                    */
                                if(existe){         
                                    var tr = $(this);
                                    tr.css('color', '#ff0000');
                                    globalVariable.editado = 1                                    
                                    row.data()['idrbcodl']=e.target.textContent
                                    var debeerp = 0
                                    var habererp = 0
                                    var aConciliarVarios = 0
                                    if(original>0){
                                        table.rows( function ( idx, data, node ) {
                                        var rowe = table.row(idx)
                                        if(rowe.data()["idrerpdl"]==row.data()["idrerpd"]){
                                            rowe.data()["idrerpdl"] = 0
                                        }
                                    })}
                                    /*  
                                      Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                    */
    
                                    /*  
                                      Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                    */
                                    table.rows( function ( idx, data, node ) {
                                        if(data.idrbcodl == e.target.textContent){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == e.target.textContent && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["idrbcodl"] == e.target.textContent){
                                                            rowc.data()["estadoerp"]=1
                                                            rowc.data()["historial"]="4"
                                                            table.rows(function ( idx, data, node ) {
                                                    var rowx = table.row(idx)
                                                    if(rowx.data()["idrbcod"] == rowc.data()["idrbcodl"] && rowx.data()["fechatrabco"] != rowc.data()["fechatraerp"]){
                                                        rowc.data()['historial']="2"
                                                    }

                                                })
                                                        }});
                                                    rowb.data()['estadobco']=1
                                                    if(aConciliarVarios>1){rowb.data()['idrerpdl']=-1}else if(aConciliarVarios==1){rowb.data()['idrerpdl']=row.data()['idrerpd']}
                                                }else if(rowb.data()['idrbcod'] == e.target.textContent){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["idrbcodl"] == e.target.textContent){
                                                                rowc.data()["estadoerp"]=0
                                                                if(rowc.data()["historial"]== "2" || rowc.data()["historial"]=="4" || rowc.data()["historial"]=="3"){
                                                                    rowc.data()["historial"]="5"
                                                                        }
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                        rowb.data()['idrerpdl']=0
                                                }
                                    });
                                    row = table.row(e.target.parentElement)
                                    debeerp = 0
                                    habererp = 0
                                    aConciliarVarios = 0
                                    /*  
                                      Se realiza lo mismo con el original que se modifico
                                    */
    
                                    /*  
                                      Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                    */
                                    table.rows( function ( idx, data, node ) {
                                        if(data.idrbcodl == original && original != 0){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == original && original != 0 && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["idrbcodl"] == original && original != 0){
                                                            rowc.data()["estadoerp"]=1
                                                            rowc.data()["historial"]="5"        
                                                table.rows(function ( idx, data, node ) {
                                                    var rowx = table.row(idx)
                                                    if(rowx.data()["idrbcod"] == rowc.data()["idrbcodl"] && rowx.data()["fechatrabco"] != rowc.data()["fechatraerp"]){
                                                        rowc.data()['historial']="5"
                                                    }

                                                })
                                                        }});
                                                    rowb.data()['estadobco']=1
                                                    if(aConciliarVarios>1){rowb.data()['idrerpdl']=-1}else if(aConciliarVarios==1){rowb.data()['idrerpdl']=row.data()['idrerpd']}
                                                }else if(rowb.data()['idrbcod'] == original && original != 0){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["idrbcodl"] == original && original != 0){
                                                                rowc.data()["estadoerp"]=0
                                                                if(rowc.data()["historial"]== "2" || rowc.data()["historial"]=="4" || rowc.data()["historial"]=="3"){
                                                                rowc.data()["historial"]="5"
                                                                    }
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                        rowb.data()['idrerpdl']=0
                                                }
                                    });
                                    if (row.data()['historial']=="0"){
                                        row.data()['historial']="1"
                                    }
                                    table.rows().invalidate().draw(false);
                                    var datasend = []
                                    for (let fila = 0; fila < table.rows().count(); fila++) {
                                    var rows = table.row(fila)
                                    datasend.push(rows.data());
                                    }

                                    if(estadooriginal == "2" ||estadooriginal == "3" || estadooriginal == "4"){
                                        if(row.data()["estadoerp"]==0){
                                        row.data()["historial"]="5"}
                                    }
                                    var token =  $('input[name="csrfToken"]').attr('value')
                                    let cookie = document.cookie
                                    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                $.ajax({
                                    type: "POST",
                                    url: '/updateScript/',
                                    data: JSON.stringify(datasend).replace(/[]/g, ""),
                                    headers: {
                                        'X-CSRFToken': csrfToken
                                      }
                                })    
                            }else{e.target.textContent= original}}
                            }
                            row.invalidate().draw(false)
                              })
                              cell.addEventListener('mouseenter', function(e) {resaltarbco(e)})
                              cell.addEventListener('mouseleave', function(e) {desresaltarbco(e)})
                        }
                    },
                {
                    targets: ["_all"],
                    className: "dt-nowrap pt-1 pb-1 pr-1 pl-1",
                    // createdCell: function (td,value, data){
                    //     /* CELDA POR CELDA DE LAS COLUMNAS EN targets */
                    // }
                },
                {
                    targets: ["idrbcod"],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `</nobr></td> <a class=d-inline href="#!" onclick="javascript:ventanaSecundaria('../cbrbcod/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></nobr></td>`
                    }else{return""}
                    }

                },
                
                
                {
                    targets: ["estadobco"],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                        var $elDiv = $('<div></div>');
                        var classBackground = '';
                        switch (row['estadobco']) {
                            case 0: {
                                            var $Etiqueta = $('<p>No Conciliado</p>');
                                            classBackground = 'callout-warning ';
                                            break;
                                        } 
                                        
                            case 1: {
                                var $Etiqueta = $('<p>Conciliado</p>');
                                classBackground = 'callout-success';
                                break;
                                    } 
                            default: {
                                var $Etiqueta = $('<p></p>');
                                break;
                                    } 
                        }
                        
                        $Etiqueta.attr('style', "width: 50px; height: 6px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-0 h-100 w-100 ' + classBackground);
                        if(row['debebco']!=null){
                        return $elDiv.clone().html();}else{
                            return ""
                        }
                    }
                },
                {
                    targets: ["idrerpdl"],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                            var zone_html = "";
                            if (data == null || data == 0) {
                                zone_html = ""
                            }
                            else if (data == -1){
                                zone_html =  '<i style="color: green;" class="fas fa-check"></i>'
                            }
                            else if(row['estadobco']==1){zone_html =
                                
                                ` <div class="linkconciliadook"><a href="#!" class"linksid" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></div>
                                <script>
                                function ventanaSecundaria (URL){ 
                                        window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                                     } 
                                </script>`
                                    }
                            else{zone_html =
                                
                                ` <div class="linkconciliadofallo"><a href="#!" class"linksid" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></div>
                                <script>
                                function ventanaSecundaria (URL){ 
                                        window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                                     } 
                                </script>`
                                    }

                            
                            return zone_html;
                                
                        
                    }
                },
                {
                    targets: ["idrbcodl"],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                            var zone_html = "";
                            if (data == null || data == 0) {
                                zone_html = ""
                            }
                            else if (data == -1){
                                zone_html =  '<i style="color: green;" class="fas fa-check"></i>'
                            }
                            else if(row['estadoerp']==1){zone_html =
                                
                                ` <div class="linkconciliadook"><a href="#!" class"linksid" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></div>
                                <script>
                                function ventanaSecundaria (URL){ 
                                        window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                                     } 
                                </script>`
                                    }
                            else{zone_html =
                                
                                ` <div class="linkconciliadofallo"><a href="#!" class"linksid" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></div>
                                <script>
                                function ventanaSecundaria (URL){ 
                                        window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                                     } 
                                </script>`
                                    }

                            
                            return zone_html;
                                
                        
                    }
                },
                    
                {
                    targets: ["idrerpd"],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return ` <a href="#!" onclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> ${data}</a>
                    <script>
                    function ventanaSecundaria (URL){ 
                            window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                         } 
                    </script>`
                        }else{return""}
                    }

                },
                {
                    targets: ["estadoerp"],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                        var $elDiv = $('<div></div>');
                        var classBackground = '';
                        switch (parseInt(row['estadoerp'])) {
                            case 0: {
                                            var $Etiqueta = $('<p>No Conciliado</p>');
                                            classBackground = 'callout-warning ';
                                            break;
                                        } 
                                        
                            case 1: {
                                var $Etiqueta = $('<p>Conciliado</p>');
                                classBackground = 'callout-success';
                                break;
                                    } 
                            default: {
                                var $Etiqueta = $('<p>'+row['estadoerp']+'</p>');
                                break;
                                    } 
                        }
                        
                        $Etiqueta.attr('style', "width: 50px; height: 6px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-0 h-100 w-100 ' + classBackground);
                        if(row['debeerp']!=null){
                        return $elDiv.clone().html();
                        }else{return ""}
                    }
                },
                

            ],
            rowCallback: function (row, data, index) {
                var sortInfo = $(this).dataTable().fnSettings().aaSorting;
                if ((sortInfo[0][0] === 0) || (sortInfo[0][0] === 1) || (sortInfo[0][0] === 10)){
                     if (data['pautado'] === 0 ){
                         $(row).addClass('odd');
                     } else {
                         $(row).addClass('even');
                     }
                } else {
                    $(row).removeClass('odd');
                    $(row).removeClass('even');
                }

            },
            drawCallback: function(){
                cargando.innerHTML = " "
            },
            createdRow: function (row, data, dataIndex) {

                var classBackground = '';/*
                switch (data['estado']) {

                    case 0:
                        classBackground += ' bg-conciliado';
                        break;
                    case 1:
                        classBackground += ' bg-enconciliacion-resultados';
                        break;
                    case 2:
                        classBackground += ' bg-conciliado-resultados';
                        break;
                }
                $(row).children().addClass(classBackground);
                $(row).children().addClass('texto-cbsres');*/
            },
            initComplete: function (settings, json) {
            },
        });
        const createdCell = function(cell) {
            let original
          
            cell.setAttribute('spellcheck', false)
          
            cell.addEventListener('focus', function(e) {
              original = e.target.textContent
            })
          
            cell.addEventListener('blur', function(e) {
              if (original !== e.target.textContent) {
                const row = table.row(e.target.parentElement)
                row.invalidate()
                console.log('Row changed: ', row.data())
              }
            })
          }
        table = $('#data').DataTable();


        $('#data tbody')
            .on( 'mouseenter', 'td', function () {
                var colIdx = table.cell(this).index().column;
                var rowIdx = table.cell(this).index().row;
                var datalook= $(this).data('look');
                $( table.cells().nodes() ).removeClass( 'highlight' );
                $( table.cells().nodes() ).removeClass( 'current' );
                if ( datalook ){
                    $( table.column( colIdx ).nodes() ).addClass( 'highlight' );
                    for (let idx = 0; idx < table.columns().header().length ; idx++) {
                        if ( $(table.column( idx ).header()).data('look') === datalook ){
                            $( table.column( idx ).nodes() ).addClass( 'highlight' );
                            $( table.cells(rowIdx, idx).nodes() ) .addClass( 'current' );
                        }
                    }
                    $(table.column(datalook).nodes() ).addClass('highlight');
                }
                $( this  ).addClass( 'current' );
            } );
        $('#data tbody')
            .on( 'mouseenter', 'td', function () {
                var colIdx = table.cell(this).index().column;
                var rowIdx = table.cell(this).index().row;
                var datalook= $(this).data('look');
                $( table.cells().nodes() ).removeClass( 'highlight' );
                $( table.cells().nodes() ).removeClass( 'current' );
                if ( datalook ){
                    $( table.column( colIdx ).nodes() ).addClass( 'highlight' );
                    for (let idx = 0; idx < table.columns().header().length ; idx++) {
                        if ( $(table.column( idx ).header()).data('look') === datalook ){
                            $( table.column( idx ).nodes() ).addClass( 'highlight' );
                            $( table.cells(rowIdx, idx).nodes() ) .addClass( 'current' );
                        }
                    }
                    $(table.column(datalook).nodes() ).addClass('highlight');
                }
                $( this  ).addClass( 'current' );
               

            } );

    } );

    /*
    $("#data").append(
        $('<tfoot/>').append( $('#data thead tr').clone()),
        $('<tfoot/>').append( '<th colspan="3" style="text-align:right">Total:</th> <th colspan="4" style="text-align:right">debebco</th> '        )

        );
    */

} );

