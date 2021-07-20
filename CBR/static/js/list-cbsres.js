var globalVariable={
    editado: 0
 };
 var globalVariableSaldo={
    saldo: 0
 };
 var globalVariableUltimoModificado={
    idsres: 0
 };

$(function () { "use strict"
    $(document).ready(function() {

        

        globalVariable.editado = 0;
        globalVariableSaldo.saldo = 0;
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
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
                {"data": "idsres"},
                {"data": "fechatrabco", name: "fechatrabco", className: "dt-bancoColor" },
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
                {"data": 'idrbcod', className: "dt-bancoColor" },
                {"data": 'oficinabco', className: "dt-bancoColor" },
                {"data": 'desctrabco', className: "dt-bancoColor" },
                {"data": 'reftrabco', className: "dt-bancoColor" },
                {"data": 'codtrabco', className: "dt-bancoColor" },
                {"data": 'isconciliado'},
                {"data": "fechatraerp", name: "fechatraerp"},
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
                {"data": 'idrerpd'},
                {"data": 'nrotraerp'},
                {"data": 'nrocomperp'},
                {"data": 'auxerp'},
                {"data": 'referp'},
                {"data": 'glosaerp'},
                {"data": 'fechaconerp'},
                {"data": 'historial', 'sClass': 'text-center pt-4', "render": function (data, type, full, meta) {
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
                {"data": 'tipoconciliado'},
                {"data": 'linkconciliado'},

            ],
            columnDefs: [
                {
                    targets: [1],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'fechatraerp');
                    }
                },
                {
                    targets: [3],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'habererp');
                    }
                },
                {
                    targets: [4],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'debeerp');
                    }
                },
                {
                    targets: [5],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoerp');
                    }
                },
                {
                    targets: [6],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumeserp');
                    }
                },
                {
                    targets: [7],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumdiaerp');
                    }
                },

                {
                    targets: [14],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'fechatrabco');
                    }
                },
                {
                    targets: [15],
                    createdCell: function (cell) {

                        $(cell).attr("data-look", 'haberbco');
                        let original
                        let saldo = parseFloat(0);
                        var row = table.row(cell)

                        if((table.cell(row,28).data() == "1" || table.cell(row,28).data() == "4")&& table.cell(row,15).data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        
                        saldo = parseFloat(table.cell( 0,18 ).data())-parseFloat(table.cell( 0,15 ).data())+parseFloat(table.cell( 0,16 ).data())
                        for (let fila = 1; isNaN(saldo); fila++) {
                            saldo = parseFloat(table.cell( fila,18 ).data())-parseFloat(table.cell( fila,15 ).data())+parseFloat(table.cell( fila,16 ).data())
                        }
                        globalVariableSaldo.saldo = saldo

                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

                        })

                        cell.addEventListener('blur', function(e) {
                            if ( original == 0 || original == null || original == "$0.00" || globalVariableUltimoModificado.idsres != 0){
                                e.target.textContent = original
                                if(globalVariableUltimoModificado.idsres != 0){
                                    alert("Llene el código de modificación")
                                }
                            }
                            else if (original !== e.target.textContent) {
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)
                                if (row.data()['tipoconciliado'] == " " || row.data()['tipoconciliado'] == null|| row.data()['tipoconciliado'] == undefined){
                                globalVariableUltimoModificado.idsres = table.cell(row,0).data()
                                }
                                row.data()['debeerp']=e.target.textContent.replace("$","")


                                /*  
                                  Cambia los valores del resto de las celdas
                                */



                                
                                let total = parseFloat(0);




                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,15).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,16).data().replace("$",""))){
                                        row.data()['isconciliado']=2}else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){ 
                                        row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                                }else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){
                                    row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                    
                                    
                                var historial = table.cell( row,28 );


                                if (row.data()['isconciliado'] == 1){
                                    historial.data( "1");
                                }else{
                                    historial.data( "4");
                                }

                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,15).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,15).data().replace("$",""))
                                    total = total + totalmas
                                }



                                let saldomas = parseFloat(0)
                                if (table.cell(fila,15).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,15).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,16).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,16).data())}


                                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,18 ).data(saldoi);


                                table.cell( row,20 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,18).data()));

                                if (table.cell(fila-1,14).data()==table.cell(fila,14).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,19 ).data(saldodia);
                                var rows = table.row(fila)

                              
                                debeerp.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})
 
                                
                                datasend.push(rows.data());
                                }
                            table.rows().invalidate().draw(false);
                            $.ajax({
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/["']/g, ""),
                                contentType: 'application/json'
                            })
                        
                            }
                          })
                    }
                },
                {targets: [29],
                    createdCell: function (cell) {
                        cell.addEventListener('mouseleave', function(e) {
                            var row = table.row(e.target.parentElement)
                            var valor = document.getElementById('option-'+row.data()['idsres']);
                            var value = valor.value
                            if(globalVariableUltimoModificado.idsres == table.cell(row,0).data() && value != " "){
                            globalVariableUltimoModificado.idsres = 0
                            }
                            if(value != " "){
                                globalVariable.editado = 1
                            }
                            
                            var datasend = []
                            row.data()['tipoconciliado']= value                           
                            datasend.push(row.data());
                            $.ajax({
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/["']/g, ""),
                                contentType: 'application/json'
                            })
                        })}
                    },
                {
                    targets: [16],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'debebco');
                        let original
                        let saldo = parseFloat(0);

                        var row = table.row(cell)

                        if((table.cell(row,28).data() == "1" || table.cell(row,28).data() == "4")&& table.cell(row,16).data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

                        })

                        cell.addEventListener('blur', function(e) {
                            if ( original == 0 || original == null || original == "$0.00" || globalVariableUltimoModificado.idsres != 0){
                                e.target.textContent = original
                                if(globalVariableUltimoModificado.idsres != 0){
                                    alert("Llene el código de modificación")
                                }
                            }
                            else if (original !== e.target.textContent) {

                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)
                                if (row.data()['tipoconciliado'] == " " || row.data()['tipoconciliado'] == null || row.data()['tipoconciliado'] == undefined){
                                    globalVariableUltimoModificado.idsres = table.cell(row,0).data()
                                    }

                                row.data()['habererp']=e.target.textContent.replace("$","")


                                /*  
                                  Cambia los valores del resto de las celdas
                                */



                                
                                let total = parseFloat(0);




                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)


                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,15).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,16).data().replace("$",""))){
                                        row.data()['isconciliado']=2}else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){ 
                                        row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                                }else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){
                                    row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}

                                var historial = table.cell( row,28 );


                                if (row.data()['isconciliado'] == 1){
                                    historial.data( "1");
                                }else{
                                    historial.data( "4");
                                }

                                var datasend = []
                                for (let fila = 0; fila < table.rows().count(); fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,16).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,16).data().replace("$",""))
                                    total = total + totalmas
                                }



                                let saldomas = parseFloat(0)
                                if (table.cell(fila,15).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,15).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,16).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,16).data())}


                                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,18 ).data(saldoi);




                                table.cell( row,20 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,18).data()));

                                if (table.cell(fila-1,14).data()==table.cell(fila,14).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,19 ).data(saldodia);
                                var rows = table.row(fila)
                                

                                habererp.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2});                                                           
                                datasend.push(rows.data());
                                }
                            table.rows().invalidate().draw(false);    
                            $.ajax({
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/["']/g, ""),
                                contentType: 'application/json'
                            })
                            }
                          })
                    }
                },

                {
                    targets: [17],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldobco');
                    }
                },

                {
                    targets: [18],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumesbco');
                    }
                },
                {
                    targets: [19],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumdiabco');
                    }
                },

                {
                    targets: [30],
                    createdCell: function (cell) {
                        let original

                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {
                            original = e.target.textContent
                        })

                        cell.addEventListener('blur', function(e) {
                            if (original !== e.target.textContent) {
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)
                                row.data()['linkconciliado']=e.target.textContent
                                /*  
                                  Cambia los valores del resto de las celdas
                                */
                                var historial = table.cell( row,28 );
                                if (row.data['isconciliado'] == 1){
                                    historial.data( "1");
                                }else{
                                    historial.data( "4");
                                }                                
  
                                if(table.cell(row,4).data() == null || table.cell(row,15).data() == null || table.cell(row,16).data() == null || table.cell(row,3).data() == null){
                                    if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']=="") {
                                        row.data()['isconciliado']=1
                                        }else{row.data()['isconciliado']=2}
                                }else{
                                    if(parseFloat(table.cell(row,15).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,16).data().replace("$",""))){
                                    row.data()['isconciliado']=2
                                    }else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']=="") {
                                        row.data()['isconciliado']=1
                                        }else{row.data()['isconciliado']=2}
                                }
                                table.rows( function ( idx, data, node ) { 
                                    if (data.idrerpd == e.target.textContent){ 
                                        var rowb = table.row(idx)
                                        rowb.data()['isconciliado']=2
                                        }                   
                                });

                                table.rows().invalidate().draw(false);
                                var datasend = []
                                datasend.push(row.data());
                                
                            $.ajax({
                                url: '/updateScript/',
                                data: JSON.stringify(datasend).replace(/["']/g, ""),
                                contentType: 'application/json'
                            })    
                            }
                          })
                    }
                },

                {
                    targets: [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,27,28,29,30],
                    className: "dt-nowrap pt-2 pb-2 pr-1 pl-1",
                    // createdCell: function (td,value, data){
                    //     /* CELDA POR CELDA DE LAS COLUMNAS EN targets */
                    // }
                },
                {
                    targets: [29],
                    render: function (data, type, row,meta) {
                        if (row['historial']== 1 ||row['historial']== 4){
                        if (row['haberbco'] == null || row['haberbco'] == undefined){
                        return `
                        <td><nobr>
                        <select name="tipo" id="option-${row['idsres']}">
                        <option value="${table.row(meta.row).data()['tipoconciliado']}">${table.row(meta.row).data()['tipoconciliado']}</option>
                        <option value=" "></option>
                        <option value="CHTR">CHTR</option>
                        <option value="DPTR">DPTR</option>
                        <option value="NCTR">NCTR</option>
                        <option value="NDTR">NDTR</option>
                      </select>
                      <a onclick="alertaa()" id="masInfo"  data-toggle="tooltip" data-toggle="tooltip" data-placement="right" title="Más info">
                      <i class="fas fa-question fa-xs"></i></a>
                      <script>
                    function alertaa() {
                    alert("CHTR Cheques en Tránsito \\nDPTR Depósitos en Tránsito \\nNotas de Crédito en Tránsito \\nNotas de Débito en Tránsito");
                    }
                    </script>
                      </nobr></td>`
                        }else if (row['fechatraerp'] == null || row['fechatraerp'] == undefined){
                            return`
                            <td><nobr>
                            <select name="tipo" id="option-${row['idsres']}">
                            <option value="${table.row(meta.row).data()['tipoconciliado']}">${table.row(meta.row).data()['tipoconciliado']}</option>
                            <option value=" "></option>
                            <option value="DNC">DNC</option>
                            <option value="NCNC">NCNC</option>
                            <option value="NDNC">NDNC</option>
                            <option value="CHNC">CHNC</option>
                            <option value="CERR">CERR</option>
                            <option value="AERR">AERR</option>
                          </select>
                          <a onclick="alertab()" id="masInfo"  data-toggle="tooltip" data-toggle="tooltip" data-placement="right" title="Más info">
                          <i class="fas fa-question fa-xs"></i></a>
                          <script>
                        function alertab() {
                        alert("DNC:Débito no Contabilizado \\nNCNC Notas de Créditos no contabilizadas\\nNDNC Notas de Débito no Contabilizadas \\nCHNC Cheques No Contabilizados \\nCERR Cargos Erróneos \\nAERR Abonos Erróneos");
                        }
                        </script>
                          </nobr></td>`
                                
                        }else{return `
                        <td><nobr>
                        <select name="tipo" id="option-${row['idsres']}">
                        <option value="${table.row(meta.row).data()['tipoconciliado']}">${table.row(meta.row).data()['tipoconciliado']}</option>
                        <option value=" "></option>
                        <option value="CHTR">CHTR</option>
                        <option value="DPTR">DPTR</option>
                        <option value="NCTR">NCTR</option>
                        <option value="NDTR">NDTR</option>
                        <option value="DNC">DNC</option>
                        <option value="NCNC">NCNC</option>
                        <option value="NDNC">NDNC</option>
                        <option value="CHNC">CHNC</option>
                        <option value="CERR">CERR</option>
                        <option value="AERR">AERR</option>
                      </select>
                      <a onclick="alertac()" id="masInfo"  data-toggle="tooltip" data-toggle="tooltip" data-placement="right" title="Más info">
                      <i class="fas fa-question fa-xs"></i></a>
                      <script>
                    function alertac() {
                    alert("CHTR Cheques en Tránsito \\nDPTR Depósitos en Tránsito \\nNotas de Crédito en Tránsito \\nNotas de Débito en Tránsito\\nDNC:Débito no Contabilizado \\nNCNC Notas de Créditos no contabilizadas\\nNDNC Notas de Débito no Contabilizadas \\nCHNC Cheques No Contabilizados \\nCERR Cargos Erróneos \\nAERR Abonos Erróneos");
                    }
                    </script>
                      </nobr></td>`}
                    }else{return ""}
                }
                },
                
                {
                    targets: [8],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `${data} <a href="#" onclick="javascript:ventanaSecundaria('../cbrbcod/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> <i class="fas fa-search-plus"></i></a>`
                    }else{return""}
                    }

                },
                {
                    targets: [21],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `${data} <a href="#" onclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> <i class="fas fa-search-plus"></i></a>
                    <script>
                    function ventanaSecundaria (URL){ 
                            window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=420,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                         } 
                    </script>`
                        }else{return""}
                    }

                },
                
                {
                    targets: ['estado'],
                    className: "p-0 pb-0 ",
                    orderable: true,
                    render: function (data, type, row) {
                        var $elDiv = $('<div></div>');
                        var classBackground = '';
                        switch (row['isconciliado']) {
                            case 1: {

                                switch (row['numrec']) {
                                    case 1: {
                                        if ((row['codtra_bco'] == null) || (row['codtra_bco'] === undefined) || (row['codtra_bco'] === '')) {
                                            var $Etiqueta = $('<p>Sobrante en ERP</p>');
                                            classBackground = 'callout-warning ';
                                        } else {
                                            var $Etiqueta = $('<p>Faltante en ERP</p>');
                                            classBackground = 'callout-danger';
                                        }
                                        break;
                                    }
                                    default : {
                                        if ((row['codtrabco'] == null) || (row['codtrabco'] === undefined) || (row['codtrabco'] === '')) {
                                            var $Etiqueta = $('<p>Sobrante en ERP </p>');
                                            classBackground = 'callout-warning ';
                                        } else {
                                            if ((row['fechatraerp'] == null) || (row['fechatraerp'] === undefined) || (row['fechatra_rp'] === '')) {
                                                var $Etiqueta = $('<p>Faltante en ERP</p>');
                                                classBackground = 'callout-danger ';
                                            } else {
                                                var $Etiqueta = $('<p>No Conciliado</p> ');
                                                classBackground = 'callout-info ';
                                            }
                                        }
                                        break;
                                    }
                                }
                                break;
                            }
                            case 2: {
                                switch (row['numrec']) {
                                    case 1: {
                                        var $Etiqueta = $('<p>Conciliado</p>');
                                        classBackground = 'callout-success';
                                        break;
                                    }
                                    default : {
                                        var $Etiqueta = $('<p>Conciliado <strong>');
                                        classBackground = 'callout-info ';
                                        break;
                                    }
                                }
                                break;
                            }
                        }
                        $Etiqueta.attr('style', "width: 100px; height: 16px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-2 h-100 w-100 ' + classBackground);
                        return $elDiv.clone().html();
                    }
                },
                
                {
                    targets: [20],
                    createdCell: function (td, cellData, rowData, row, col) {

                        if (rowData['saldodiferencia'] != '0.00') {
                            $(td).css('color', 'red')
                        }
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

                var classBackground = '';
                switch (data['isconciliado']) {

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
                $(row).children().addClass('texto-cbsres');
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


    } );

    /*
    $("#data").append(
        $('<tfoot/>').append( $('#data thead tr').clone()),
        $('<tfoot/>').append( '<th colspan="3" style="text-align:right">Total:</th> <th colspan="4" style="text-align:right">debebco</th> '        )

        );
    */

} );

