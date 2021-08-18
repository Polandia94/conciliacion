var globalVariable={
    editado: 0
 };
 var globalVariableSaldo={
    saldo: 0
 };



$(function () { "use strict"
    $(document).ready(function() {
        console.log("empieza")     
        globalVariable.editado = 0;
        globalVariableSaldo.saldo = 0;
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
        let maximosCaracteres = 25;

        let table = $('#data').DataTable({
            
            deferRender: true,
            colReorder: true,
            stateSave: true,
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
                {"data": "debebco", name: "debebco", render: $.fn.dataTable.render.number(',', '.', 2, '$'), className: "dt-bancoColor" },
                {"data": "haberbco", name: "haberbco", render: $.fn.dataTable.render.number(',', '.', 2, '$'), className: "dt-bancoColor" },
                {"data": "saldobco", name: "saldobco", render: $.fn.dataTable.render.number(',', '.', 2, '$'), className: "dt-bancoColor" },
                {
                    "data": "saldoacumesbco",
                    name: "saldoacumesbco",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$'), 
                    className: "dt-bancoColor" 
                },
                {
                    "data": "saldoacumdiabco",
                    name: "saldoacumdiabco",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$'), 
                    className: "dt-bancoColor" 
                },
                {"data": 'oficina', className: "dt-bancoColor" },
                {"data": 'desctra', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > 25) {
                        zone_html = data.substring(0,15)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'reftra', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > 25) {
                        zone_html = data.substring(0,15)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'codtra', className: "dt-bancoColor" },
                {"data": 'idrbcod', className: "dt-bancoColor" },
                
                {"data": 'estadobco', className: "dt-bancoColor" },
                {"data": 'codtcobco', className: "dt-bancoColor" },
                {"data": 'linkconciliadoerp', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data == null || data == 0) {
                        zone_html = ""
                    }
                    else if (data == -1){
                        zone_html =  '<i class="fas fa-check"></i>'
                    }
                    else{zone_html =
                        
                        ` <a href="#" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a>
                        <script>
                        function ventanaSecundaria (URL){ 
                                window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                             } 
                        </script>`
                            }
                    return zone_html;
                    }},
                
                {"data": 'idrerpd'},
                {"data": 'estadoerp'},
                {"data": 'codtcoerp'},
                {"data": 'linkconciliadobco', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data == null || data == 0) {
                        zone_html = ""
                    }
                    else if (data == -1){
                        zone_html =  '<i class="fas fa-check"></i>'
                    }
                    else{zone_html =
                        
                        ` <a href="#" ondblclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a>
                        <script>
                        function ventanaSecundaria (URL){ 
                                window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                             } 
                        </script>`
                            }
                    return zone_html;
                    }},              
                
                    
                {"data": "fechatraerp", name: "fechatraerp", "render": function (data, type, full, meta) {
                    if(data!=null){
                    return "<td><nobr>" + data + "</nobr></td>"}else{return""}
                    }},
                {"data": "debeerp", name: "debeerp", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {"data": "habererp", name: "habererp", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {"data": "saldoerp", name: "saldoerp", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {
                    "data": "saldoacumeserp",
                    name: "saldoacumeserp",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$')
                },
                {
                    "data": "saldoacumdiaerp",
                    name: "saldoacumdiaerp",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$')
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
                    if (data != null && data.length > 25) {
                        zone_html = data.substring(0,15)+"..."+data.substring(data.length -5)
                    }
                    else if (data != null){zone_html = data} 
                    return "<td><nobr>" +zone_html+ "</nobr></td>";
                    }},
                {"data": 'glosaerp', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data != null && data.length > 25) {
                        zone_html = data.substring(0,15)+"..."+data.substring(data.length -5)
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
                    if (data === "3") {
                        zone_html = 'Conciliado'
                    }
                    if (data === "4") {
                        zone_html = 'Modificado y Conciliado'
                    }
                    return zone_html;
                    }
                },

            ],
            columnDefs: [
                {
                    targets: ['fechatrabco'],
                    createdCell: function (cell) {
                        console.log("1")
                        $(cell).attr("data-look", 'fechatraerp');
                    }
                },
                {
                    targets: ["debebco"],
                    createdCell: function (cell) {
                        console.log("2")
                        $(cell).attr("data-look", 'habererp');
                    }
                },
                {
                    targets: ["haberbco"],
                    createdCell: function (cell) {
                        console.log("3")
                        $(cell).attr("data-look", 'debeerp');
                    }
                },
                {
                    targets: ["saldobco"],
                    createdCell: function (cell) {
                        console.log("4")
                        $(cell).attr("data-look", 'saldoerp');
                    }
                },
                {
                    targets: ["saldoacumesbco"],
                    createdCell: function (cell) {
                        console.log("5")
                        $(cell).attr("data-look", 'saldoacumeserp');
                    }
                },
                {
                    targets: ["saldoacumdiabco"],
                    createdCell: function (cell) {
                        console.log("6")
                        $(cell).attr("data-look", 'saldoacumdiaerp');
                    }
                },
                {
                    targets: ["desctra"],
                    createdCell: function (cell) {
                        console.log("7")
                        var row = table.row(cell)
                        if(row.data()['desctra']!=null && row.data()['desctra'].length > maximosCaracteres){
                            $(cell).attr("title", row.data()['desctra'])
                        };
                    }
                },
                {targets: ["referp"],
                createdCell: function (cell) {
                    console.log("8")
                    var row = table.row(cell)
                    if(row.data()['referp']!=null && row.data()['referp'].length > maximosCaracteres){
                        $(cell).attr("title", row.data()['referp'])
                        };
                    }
                },
                {targets: ["glosaerp"],
                createdCell: function (cell) {
                    console.log("9")
                    var row = table.row(cell)
                    if(row.data()['glosaerp']!=null && row.data()['glosaerp'].length > maximosCaracteres){
                        $(cell).attr("title", row.data()['glosaerp'])
                        };
                    }
                },
                {targets: ["codtcobco"],
                    createdCell: function (cell) {
                        console.log("10")
                        cell.addEventListener('mouseleave', function(e) {
                            var row = table.row(e.target.parentElement)
                            var valor = document.getElementById('optionbco-'+row.data()['idsres']);
                            try{var value = valor.value}
                            finally{}
                            if(value != row.data()['codtcobco']){
                                globalVariable.editado = 1
                                row.data()['codtcobco']= value
                                var datasend = []
                                datasend.push(row.data());
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
                            }
                            
                            
                        })}
                    },
                    {targets: ["codtcoerp"],
                    createdCell: function (cell) {
                        console.log("11")
                        cell.addEventListener('mouseleave', function(e) {
                            var row = table.row(e.target.parentElement)
                            var valor = document.getElementById('optionerp-'+row.data()['idsres']);
                            try{var value = valor.value}
                            finally{}
                            if(value != row.data()['codtcoerp']){
                                globalVariable.editado = 1
                                row.data()['codtcoerp']= value
                                var datasend = []
                                datasend.push(row.data());
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
                            }
                            
                            
                        })}
                    },
                {
                    targets: ["linkconciliadoerp"],
                    createdCell: function (cell) {
                        console.log("12")
                        let original

                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {
                            var row = table.row(e.target.parentElement)
                            original = row.data()["linkconciliadoerp"]
                        })

                        cell.addEventListener('blur', function(e) {
                            e.target.textContent = e.target.textContent.substring(0,10)
                            console.log(e.target.textContent)
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
                                        if(rowb.data()['linkconciliadobco'] < 1 || rowb.data()['linkconciliadobco']== null){
                                        existe = true}} });                                   
                                if(e.target.textContent == 0){existe = true}
                                    /*  
                                  Si el valor es numero pasa a ser rojo, la variable editado se activa
                                */
                            if(existe){         
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                row.data()['linkconciliadoerp']=e.target.textContent
                                var debebco = 0
                                var haberbco = 0
                                var aConciliarVarios = 0
                                if(original>0){
                                    table.rows( function ( idx, data, node ) {
                                    var rowe = table.row(idx)
                                    if(rowe.data()["linkconciliadobco"]==row.data()["idrbcod"]){
                                        rowe.data()["linkconciliadobco"] = 0
                                    }
                                })}
                                /*  
                                  Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                */

                                /*  
                                  Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                */
                                table.rows( function ( idx, data, node ) {
                                    if(data.linkconciliadoerp == e.target.textContent){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debebco = debebco + parseFloat(rowc.data()['debebco'])
                                        haberbco = haberbco + parseFloat(rowc.data()['haberbco'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == e.target.textContent && rowb.data()['debeerp'] == haberbco && rowb.data()['habererp'] == debebco && (debebco != 0 || haberbco != 0)){                                           
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["linkconciliadoerp"] == e.target.textContent){
                                                        rowc.data()["estadobco"]=1
                                                    }});
                                                rowb.data()['estadoerp']=1
                                                if(aConciliarVarios>1){rowb.data()['linkconciliadobco']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadobco']=row.data()['idrbcod']}
                                            }else if(rowb.data()['idrerpd'] == e.target.textContent){
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadoerp"] == e.target.textContent){
                                                            rowc.data()["estadobco"]=0
                                                        }});
                                                    rowb.data()['estadoerp']=0
                                                    rowb.data()['linkconciliadobco']=0
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
                                    if(data.linkconciliadoerp == original && original != 0){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debebco = debebco + parseFloat(rowc.data()['debebco'])
                                        haberbco = haberbco + parseFloat(rowc.data()['haberbco'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == original && original != 0 && rowb.data()['debeerp'] == haberbco && rowb.data()['habererp'] == debebco && (debebco != 0 || haberbco != 0)){                                           
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["linkconciliadoerp"] == original && original != 0){
                                                        rowc.data()["estadobco"]=1
                                                    }});
                                                rowb.data()['estadoerp']=1
                                                if(aConciliarVarios>1){rowb.data()['linkconciliadobco']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadobco']=row.data()['idrbcod']}
                                            }else if(rowb.data()['idrerpd'] == original && original != 0){
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadoerp"] == original && original != 0){
                                                            rowc.data()["estadobco"]=0
                                                        }});
                                                    rowb.data()['estadoerp']=0
                                                    rowb.data()['linkconciliadobco']=0
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
                    }
                },
                {
                    targets: ["debeerp"],
                    createdCell: function (cell) {
                        console.log("13")

                        $(cell).attr("data-look", 'haberbco');
                        let original
                        let saldo = parseFloat(0);
                        var row = table.row(cell)
                        if((table.cell(row,28).data() == "1" || table.cell(row,28).data() == "4")&& table.cell(row,15).data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        console.log("sigue")
                        saldo = parseFloat(table.cell( 0,20 ).data())-parseFloat(table.cell( 0,17 ).data())+parseFloat(table.cell( 0,18 ).data())
                        for (let fila = 1; isNaN(saldo); fila++) {
                            saldo = parseFloat(table.cell( fila,20 ).data())-parseFloat(table.cell( fila,17 ).data())+parseFloat(table.cell( fila,18 ).data())
                        }
                        globalVariableSaldo.saldo = saldo
                        
                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

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

                                row.data()['habererp']=e.target.textContent.replace("$","")
                                let total = parseFloat(0);
                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                if(row.data()['linkconciliadobco']==-2 && original != e.target.textContent){
                                    row.data()['estadoerp']=0,
                                    row.data()['estadobco']=0,
                                    row.data()['linkconciliadobco']=0,
                                    row.data()['linkconciliadoerp']=0
                                };
                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,17).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,18).data().replace("$",""))){
                                        row.data()['estadoerp']=1,
                                        row.data()['estadobco']=1,
                                        row.data()['linkconciliadobco']=-2,
                                        row.data()['linkconciliadoerp']=-2}};
                                var historial = table.cell( row,33 );

                                if (row.data()['estadoerp'] == 1){
                                    historial.data( "1");
                                }else{
                                    historial.data( "4");
                                }

                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,17).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,17).data().replace("$",""))
                                    total = total + totalmas
                                }

                                let saldomas = parseFloat(0)
                                if (table.cell(fila,17).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,17).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,18).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,18).data())}
                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,20 ).data(saldoi);

                                table.cell( row,22 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,20).data()));

                                if (table.cell(fila-1,14).data()==table.cell(fila,14).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,21 ).data(saldodia);
                                var rows = table.row(fila)
                                debeerphtml.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})
                                datasend.push(rows.data());
                                }
                                if(row.data()["linkconciliadobco"]==-1){row.data()["linkconciliadobco"]=0}
                                table.rows( function ( idx, data, node ) { 
                                    var rowg = table.row(idx)
                                    if(rowg.data()["idrbcod"]==row.data()["linkconciliadobco"] && rowg.data()["linkconciliadoerp"]==-1){rowg.data()["linkconciliadoerp"]=0}})
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
                                        if(data.linkconciliadobco == row.data()["linkconciliadobco"]){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == row.data()["linkconciliadobco"] && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadobco"] == row.data()["linkconciliadobco"]){
                                                            rowc.data()["estadoerp"]=1
                                                        }});
                                                    rowb.data()['estadobco']=1
                                                    if(aConciliarVarios>1){rowb.data()['linkconciliadoerp']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadoerp']=row.data()['idrerpd']}
                                                }else if(rowb.data()['idrbcod'] == row.data()["linkconciliadobco"]){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["linkconciliadobco"] == row.data()["linkconciliadobco"]){
                                                                rowc.data()["estadoerp"]=0
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                }
                                    });

                                
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                table.rows().invalidate().draw(false);                         



                            $.ajax({
                                type: "POST",
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/[]/g, ""),
                                headers: {
                                    'X-CSRFToken': csrfToken
                                  }
                            })   
                        
                            
                        }
                        
                          })
                          console.log("termina")
                    }
                },
                {
                    targets: ["habererp"],
                    createdCell: function (cell) {
                        console.log("14")

                        $(cell).attr("data-look", 'debebco');
                        let original
                        var row = table.row(cell)
                        if((table.cell(row,28).data() == "1" || table.cell(row,28).data() == "4")&& table.cell(row,15).data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        
                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

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
                                row.data()['habererp']=e.target.textContent.replace("$","")
                                let total = parseFloat(0);
                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                var historial = table.cell( row,33 );
                                if (row.data()['estadoerp'] == 1){
                                    historial.data( "1");
                                }else{
                                    historial.data( "4");
                                }

                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,18).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,18).data().replace("$",""))
                                    total = total + totalmas
                                }

                                let saldomas = parseFloat(0)
                                if (table.cell(fila,17).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,17).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,18).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,18).data())}
                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,20 ).data(saldoi);

                                table.cell( row,22 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,20).data()));

                                if (table.cell(fila-1,14).data()==table.cell(fila,14).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,21 ).data(saldodia);
                                var rows = table.row(fila)
                                habererphtml.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})
                                datasend.push(rows.data());
                                }
                                if(row.data()["linkconciliadobco"]==-1){row.data()["linkconciliadobco"]=0}
                                table.rows( function ( idx, data, node ) { 
                                    var rowg = table.row(idx)
                                    if(row.data()["idrerpd"]==rowg.data()["linkconciliadoerp"]){
                                        rowg.data()["estadobco"]=0
                                        if(rowg.data()["linkconciliadoerp"]==-1){rowg.data()["linkconciliadoerp"]=0}

                                        }})
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
                                    if(data.linkconciliadobco == row.data()["linkconciliadobco"]){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                        habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrbcod'] == row.data()["linkconciliadobco"] && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["linkconciliadobco"] == row.data()["linkconciliadobco"]){
                                                        rowc.data()["estadoerp"]=1
                                                    }});
                                                rowb.data()['estadobco']=1
                                                if(aConciliarVarios>1){rowb.data()['linkconciliadoerp']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadoerp']=row.data()['idrerpd']}
                                            }else if(rowb.data()['idrbcod'] == row.data()["linkconciliadobco"]){
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadobco"] == row.data()["linkconciliadobco"]){
                                                            rowc.data()["estadoerp"]=0
                                                        }});
                                                    rowb.data()['estadobco']=0
                                                    if(rowb.data()["linkconciliadoerp"]==-1){rowb.data()["linkconciliadoerp"]=0}
                                            }
                                });

                                var debebco = 0
                                var haberbco = 0
                                var aConciliarVarios = 0
                                /*  
                                  Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                */

                                /*  
                                  Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                */
                                table.rows( function ( idx, data, node ) {
                                    if(data.linkconciliadoerp == row.data()["idrerpd"]){
                                        var rowc = table.row(idx)
                                        aConciliarVarios = aConciliarVarios + 1
                                        debebco = debebco + parseFloat(rowc.data()['debebco'])
                                        haberbco = haberbco + parseFloat(rowc.data()['haberbco'])}});
                                table.rows( function ( idx, data, node ) { 
                                    var rowb = table.row(idx)
                                    if(rowb.data()['idrerpd'] == row.data()["idrerpd"] && rowb.data()['debeerp'] == haberbco && rowb.data()['habererp'] == debebco && (debebco != 0 || haberbco != 0)){                                           
                                            table.rows( function ( idx, data, node ) {
                                                var rowc = table.row(idx)
                                                if(rowc.data()["linkconciliadoerp"] == row.data()["idrerpd"]){
                                                        rowc.data()["estadobco"]=1
                                                    }});
                                                rowb.data()['estadoerp']=1
                                                if(aConciliarVarios>1){rowb.data()['linkconciliadobco']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadobco']=row.data()['idrbcod']}
                                            }
                                });
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                table.rows().invalidate().draw(false);
                            $.ajax({
                                type: "POST",
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/[]/g, ""),
                                headers: {
                                    'X-CSRFToken': csrfToken
                                  }
                            })   
                        }
                          }})
                    }
                },
                {targets: ["codtcoerp"],
                    createdCell: function (cell) {
                        console.log("15")
                        cell.addEventListener('mouseleave', function(e) {
                            cell.addEventListener('mouseleave', function(e) {
                                var row = table.row(e.target.parentElement)
                                var valor = document.getElementById('optionerp-'+row.data()['idsres']);
                                try{var value = valor.value}
                                finally{}
                                if(value != row.data()['codtcoerp']){
                                    globalVariable.editado = 1
                                    row.data()['codtcoerp']= value
                                    var datasend = []
                                    datasend.push(row.data());
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
                                }
                                
                                
                            })})}
                    },
                    {
                        targets: ["linkconciliadobco"],
                        createdCell: function (cell) {
                            console.log("16")
                            let original

                            cell.setAttribute('contenteditable', true)
                            cell.setAttribute('spellcheck', false)
    
                            cell.addEventListener('focus', function(e) {
                                var row = table.row(e.target.parentElement)
                                original = row.data()["linkconciliadobco"]
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
                                            if(rowb.data()['linkconciliadoerp'] < 1 || rowb.data()['linkconciliadoerp'] == null){
                                            existe = true} }});                                   
                                    if(e.target.textContent == 0){existe = true}
                                        /*  
                                      Si el valor es numero pasa a ser rojo, la variable editado se activa
                                    */
                                if(existe){         
                                    var tr = $(this);
                                    tr.css('color', '#ff0000');
                                    globalVariable.editado = 1                                    
                                    row.data()['linkconciliadobco']=e.target.textContent
                                    var debeerp = 0
                                    var habererp = 0
                                    var aConciliarVarios = 0
                                    if(original>0){
                                        table.rows( function ( idx, data, node ) {
                                        var rowe = table.row(idx)
                                        if(rowe.data()["linkconciliadoerp"]==row.data()["idrerpd"]){
                                            rowe.data()["linkconciliadoerp"] = 0
                                        }
                                    })}
                                    /*  
                                      Si el debe y el haber del banco y del erp linkeados coinciden se coloca coinciliado ambos y ambos links
                                    */
    
                                    /*  
                                      Caso contrario suma todos los que tengan el mismo link conciliado y se verifica si suman igual y se cambian los correspondientes
                                    */
                                    table.rows( function ( idx, data, node ) {
                                        if(data.linkconciliadobco == e.target.textContent){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == e.target.textContent && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadobco"] == e.target.textContent){
                                                            rowc.data()["estadoerp"]=1
                                                        }});
                                                    rowb.data()['estadobco']=1
                                                    if(aConciliarVarios>1){rowb.data()['linkconciliadoerp']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadoerp']=row.data()['idrerpd']}
                                                }else if(rowb.data()['idrbcod'] == e.target.textContent){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["linkconciliadobco"] == e.target.textContent){
                                                                rowc.data()["estadoerp"]=0
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                        rowb.data()['linkconciliadoerp']=0
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
                                        if(data.linkconciliadobco == original && original != 0){
                                            var rowc = table.row(idx)
                                            aConciliarVarios = aConciliarVarios + 1
                                            debeerp = debeerp + parseFloat(rowc.data()['debeerp'])
                                            habererp = habererp + parseFloat(rowc.data()['habererp'])}});
                                    table.rows( function ( idx, data, node ) { 
                                        var rowb = table.row(idx)
                                        if(rowb.data()['idrbcod'] == original && original != 0 && rowb.data()['debebco'] == habererp && rowb.data()['haberbco'] == debeerp && (debeerp != 0 || habererp != 0)){                                           
                                                table.rows( function ( idx, data, node ) {
                                                    var rowc = table.row(idx)
                                                    if(rowc.data()["linkconciliadobco"] == original && original != 0){
                                                            rowc.data()["estadoerp"]=1
                                                        }});
                                                    rowb.data()['estadobco']=1
                                                    if(aConciliarVarios>1){rowb.data()['linkconciliadoerp']=-1}else if(aConciliarVarios==1){rowb.data()['linkconciliadoerp']=row.data()['idrerpd']}
                                                }else if(rowb.data()['idrbcod'] == original && original != 0){
                                                    table.rows( function ( idx, data, node ) {
                                                        var rowc = table.row(idx)
                                                        if(rowc.data()["linkconciliadobco"] == original && original != 0){
                                                                rowc.data()["estadoerp"]=0
                                                            }});
                                                        rowb.data()['estadobco']=0
                                                        rowb.data()['linkconciliadoerp']=0
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
                        console.log("17")
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `</nobr></td> <a class=d-inline href="#" onclick="javascript:ventanaSecundaria('../cbrbcod/${data}/${idrenc}/?return_url=CBR:cbsres-list')">${data}</a></nobr></td>`
                    }else{return""}
                    }

                },
                
                
                {
                    targets: ["estadobco"],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                        console.log("18")
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
                        
                        $Etiqueta.attr('style', "width: 100px; height: 8px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-1 h-100 w-100 ' + classBackground);
                        if(row['debebco']!=null){
                        return $elDiv.clone().html();}else{
                            return ""
                        }
                    }
                },
                
                {
                    targets: ["codtcobco"],
                    render: function (data, type, row,meta) {
                        console.log("19")
                        if (row['debebco']!=null){
                            let agregar = ""
                            for(let opcion = 0; opcion < globalVariableIndtco.indtco_bco.length; opcion++){
                                agregar = agregar + '<option value="'+globalVariableIndtco.indtco_bco[opcion]+'">'+globalVariableIndtco.indtco_bco[opcion]+'</option>'
                            }
                            let texto= `
                        <td><nobr>
                        <select name="tipo" id="optionbco-${row['idsres']}">
                        <option value="${table.row(meta.row).data()['codtcobco']}">${table.row(meta.row).data()['codtcobco']}</option>
                        `
                            +agregar+
                            `</select>
                      <a onclick="alertab()" id="masInfo"  data-toggle="tooltip" data-toggle="tooltip" data-placement="right" title="Más info">
                      <i class="fas fa-question fa-xs"></i></a>
                      </nobr></td>`
                      return texto
                        }else {return ""}
                    }
                },
                {
                    targets: ["idrerpd"],
                    render: function (data, type, row) {
                        console.log("20")
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return ` <a href="#" onclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> ${data}</a>
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
                        console.log("21")
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
                        
                        $Etiqueta.attr('style', "width: 100px; height: 8px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-1 h-100 w-100 ' + classBackground);
                        if(row['debeerp']!=null){
                        return $elDiv.clone().html();
                        }else{return ""}
                    }
                },
                {
                    targets: ["codtcoerp"],
                    render: function (data, type, row,meta) {
                        console.log("22")
                        if (row['debeerp']!=null ){
                            let agregar = ""
                            for(let opcion = 0; opcion < globalVariableIndtco.indtco_erp.length; opcion++){
                                agregar = agregar + '<option value="'+globalVariableIndtco.indtco_erp[opcion]+'">'+globalVariableIndtco.indtco_erp[opcion]+'</option>'
                            }
                            let texto= `
                        <td><nobr>
                        <select name="tipo" id="optionerp-${row['idsres']}">
                        <option value="${table.row(meta.row).data()['codtcoerp']}">${table.row(meta.row).data()['codtcoerp']}</option>
                        `
                            +agregar+
                            `</select>
                      <a onclick="alertaa()" id="masInfo"  data-toggle="tooltip" data-toggle="tooltip" data-placement="right" title="Más info">
                      <i class="fas fa-question fa-xs"></i></a>
                      </nobr></td>`
                      return texto
                        }else {return ""}
                    }
                },

            ],
            rowCallback: function (row, data, index) {
                var sortInfo = $(this).dataTable().fnSettings().aaSorting;
                if ((sortInfo[0][0] === 0) || (sortInfo[0][0] === 1) || (sortInfo[0][0] === 10)){
                     if (data['blockcolor'] === 0 ){
                         $(row).addClass('odd');
                     } else {
                         $(row).addClass('even');
                     }
                } else {
                    $(row).removeClass('odd');
                    $(row).removeClass('even');
                }

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
          
            cell.setAttribute('contenteditable', true)
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

            console.log("Termina")         
    } );

    /*
    $("#data").append(
        $('<tfoot/>').append( $('#data thead tr').clone()),
        $('<tfoot/>').append( '<th colspan="3" style="text-align:right">Total:</th> <th colspan="4" style="text-align:right">debebco</th> '        )

        );
    */

} );

