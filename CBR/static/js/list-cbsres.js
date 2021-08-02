var globalVariable={
    editado: 0
 };
 var globalVariableSaldo={
    saldo: 0
 };
 var globalVariableUltimoModificadoBco={
    idsres: 0
 };
 var globalVariableUltimoModificadoErp={
    idsres: 0
 };

$(function () { "use strict"
    $(document).ready(function() {
        console.log("empieza")     
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
                {"data": "idsres", className: "dt-comunColor"},
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
                {"data": 'oficina', className: "dt-bancoColor" },
                {"data": 'desctra', className: "dt-bancoColor" },
                {"data": 'reftra', className: "dt-bancoColor" },
                {"data": 'codtra', className: "dt-bancoColor" },
                {"data": 'idrbcod', className: "dt-bancoColor" },
                {"data": 'estadobco', className: "dt-bancoColor" },
                {"data": 'codtcobco', className: "dt-bancoColor" },
                {"data": 'linkconciliadobco', className: "dt-bancoColor", "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data < 0) {
                        zone_html = ""
                    }
                    else{zone_html = data} 
                    return zone_html;
                    }},
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
                {"data": 'estadoerp'},
                {"data": 'codtcoerp'},
                {"data": 'linkconciliadoerp', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data < 0) {
                        zone_html = ""
                    }
                    else{zone_html = data} 
                    return zone_html;
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

                {targets: [14],
                    createdCell: function (cell) {
                        cell.addEventListener('mouseleave', function(e) {
                            var row = table.row(e.target.parentElement)
                            var valor = document.getElementById('optionbco-'+row.data()['idsres']);
                            try{var value = valor.value}
                            finally{}
                            setTimeout(() => {                              if(globalVariableUltimoModificadoBco.idsres == table.cell(row,0).data() && row.data()['codtcobco'] != "" && row.data()['codtcobco'] != "" && valor != null){
                                globalVariableUltimoModificadoBco.idsres = 0
                                console.log(globalVariableUltimoModificadoBco.idsres)
                                }; }, 2000); 
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
                {
                    targets: [15],
                    createdCell: function (cell) {
                        let original

                        cell.setAttribute('contenteditable', true)
                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {
                            original = e.target.textContent
                        })

                        cell.addEventListener('blur', function(e) {
                            if (original !== e.target.textContent) {
                                if(globalVariableUltimoModificadoBco.idsres != 0 || globalVariableUltimoModificadoErp.idsres != 0){
                                    e.target.textContent = original
                                    alert("Llene el código de modificación")
                                }else{
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)
                                row.data()['linkconciliadobco']=e.target.textContent
                                row.data()['estadobco']=1
                                if (original == -2){
                                    row.data()['linkconciliadoerp']=0
                                };
                    
                                /*  
                                  Cambia los valores del resto de las celdas
                                */
                              
                                table.rows( function ( idx, data, node ) { 
                                    if (data.idrerpd == e.target.textContent){ 
                                        var rowb = table.row(idx)
                                        rowb.data()['estadoerp']=0+0
                                        rowb.data()['linkconciliadoerp']=0+0
                                        }                   
                                });
                                table.rows( function ( idx, data, node ) { 
                                    if (data.idrerpd == e.target.textContent){ 
                                        var rowb = table.row(idx)
                                        rowb.data()['estadoerp']=1+0
                                        rowb.data()['linkconciliadoerp']=-1+0
                                        }                   
                                });
                                globalVariableUltimoModificadoBco.idsres = table.cell(row,0).data()
                                table.rows().invalidate().draw(false);
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
                        }
                          })
                    }
                },
                {
                    targets: [17],
                    createdCell: function (cell) {

                        $(cell).attr("data-look", 'haberbco');
                        let original
                        let saldo = parseFloat(0);
                        var row = table.row(cell)
                        if((table.cell(row,28).data() == "1" || table.cell(row,28).data() == "4")&& table.cell(row,15).data()>0){
                        var tr = $(cell);
                        tr.css('color', '#ff0000');
                        }
                        
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
                            if ( original == 0 || original == null || row.data()['habererp'] != 0){
                                e.target.textContent = original
                            }
                            else if (original !== e.target.textContent) {
                                if(globalVariableUltimoModificadoErp.idsres != 0){
                                    e.target.textContent = original
                                    alert("Llene el código de modificación")
                                }else{
                                console.log("debe")
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                console.log(row.data()['codtcoerp'])
                                if (row.data()['codtcoerp'] == "" || row.data()['codtcoerp'] == " " || row.data()['codtcoerp'] == null|| row.data()['codtcoerp'] == undefined){
                                globalVariableUltimoModificadoErp.idsres = table.cell(row,0).data()
                                console.log(globalVariableUltimoModificadoErp.idsres)
                                }
                                row.data()['habererp']=e.target.textContent.replace("$","")
                                let total = parseFloat(0);
                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                if(row.data()['linkconciliadoerp']==-2 && original != e.target.textContent){
                                    row.data()['estadoerp']=0,
                                    row.data()['estadobco']=0,
                                    row.data()['linkconciliadoerp']=0,
                                    row.data()['linkconciliadobco']=0
                                };
                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,17).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,18).data().replace("$",""))){
                                        console.log("iguales")
                                        row.data()['estadoerp']=1,
                                        row.data()['estadobco']=1,
                                        row.data()['linkconciliadoerp']=-2,
                                        row.data()['linkconciliadobco']=-2}};
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
                                debeerp.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})
                                datasend.push(rows.data());
                                }
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                console.log(row.data()['estadoerp'])
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
                        }
                          })
                    }
                },
                {
                    targets: [18],
                    createdCell: function (cell) {

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
                            if ( original == 0 || original == null || row.data()['debeerp'] != 0){
                                e.target.textContent = original
                            }
                            else if (original !== e.target.textContent) {
                                if(globalVariableUltimoModificadoErp.idsres != 0){
                                    e.target.textContent = original
                                    alert("Llene el código de modificación")
                                }else{
                                console.log("haber")
                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                console.log(row.data()['codtcoerp'])
                                if (row.data()['codtcoerp'] == "" || row.data()['codtcoerp'] == " " || row.data()['codtcoerp'] == null|| row.data()['codtcoerp'] == undefined){
                                globalVariableUltimoModificadoErp.idsres = table.cell(row,0).data()
                                console.log(globalVariableUltimoModificadoErp.idsres)
                                }
                                row.data()['habererp']=e.target.textContent.replace("$","")
                                let total = parseFloat(0);
                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)
                                if(row.data()['linkconciliadoerp']==-2 && original != e.target.textContent){
                                    row.data()['estadoerp']=0,
                                    row.data()['estadobco']=0,
                                    row.data()['linkconciliadoerp']=0,
                                    row.data()['linkconciliadobco']=0
                                };
                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,17).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,18).data().replace("$",""))){
                                        console.log("iguales")
                                        row.data()['estadoerp']=1,
                                        row.data()['estadobco']=1,
                                        row.data()['linkconciliadoerp']=-2,
                                        row.data()['linkconciliadobco']=-2}};
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
                                habererp.innerHTML = Number(total).toLocaleString("en-US", {style: "currency", currency: "USD", minimumFractionDigits: 2})
                                datasend.push(rows.data());
                                }
                                var token =  $('input[name="csrfToken"]').attr('value')
                                let cookie = document.cookie
                                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                                console.log(row.data()['estadoerp'])
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
                        }
                          })
                    }
                },
                {targets: [31],
                    createdCell: function (cell) {
                        cell.addEventListener('mouseleave', function(e) {
                            var row = table.row(e.target.parentElement)
                            var valor = document.getElementById('optionerp-'+row.data()['idsres']);
                            try{var value = valor.value}
                            finally{}
                            setTimeout(() => {                              if(globalVariableUltimoModificadoErp.idsres == table.cell(row,0).data() && row.data()['codtcoerp'] != "" && row.data()['codtcoerp'] != "" && valor != null){
                                globalVariableUltimoModificadoErp.idsres = 0
                                console.log(globalVariableUltimoModificadoErp.idsres)
                                }; }, 2000); 
                            if(value != row.data()['codtcorep']){
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
                        targets: [32],
                        createdCell: function (cell) {
                            let original
    
                            cell.setAttribute('contenteditable', true)
                            cell.setAttribute('spellcheck', false)
    
                            cell.addEventListener('focus', function(e) {
                                original = e.target.textContent
                            })
    
                            cell.addEventListener('blur', function(e) {
                                if (original !== e.target.textContent) {
                                    if(globalVariableUltimoModificadoBco.idsres != 0 || globalVariableUltimoModificadoErp.idsres != 0){
                                        e.target.textContent = original
                                        alert("Llene el código de modificación")
                                    }else{
                                    var tr = $(this);
                                    tr.css('color', '#ff0000');
                                    globalVariable.editado = 1
                                    var row = table.row(e.target.parentElement)
                                    row.data()['linkconciliadoerp']=e.target.textContent
                                    row.data()['estadoerp']=1
                                    if (original == -2){
                                        row.data()['linkconciliadobco']=0
                                    };
                                    /*  
                                      Cambia los valores del resto de las celdas
                                    */
                                      table.rows( function ( idx, data, node ) { 
                                        if (data.idrbcod == original){ 
                                            var rowb = table.row(idx)
                                            rowb.data()['estadobco']=0
                                            rowb.data()['linkconciliadobco']=0
                                            }                   
                                    });
      
                                    table.rows( function ( idx, data, node ) { 
                                        if (data.idrbcod == e.target.textContent){ 
                                            var rowb = table.row(idx)
                                            rowb.data()['estadobco']=1
                                            rowb.data()['linkconciliadobco']=-1
                                            }                   
                                    });
                                    globalVariableUltimoModificadoErp.idsres = table.cell(row,0).data()
                                    table.rows().invalidate().draw(false);
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
                            }
                              })
                        }
                    },
                {
                    targets: [2, 3, 4, 5, 6, 7, 8,9, 10, 11,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,27,28,29,30,31,32,33],
                    className: "dt-nowrap pt-2 pb-2 pr-1 pl-1",
                    // createdCell: function (td,value, data){
                    //     /* CELDA POR CELDA DE LAS COLUMNAS EN targets */
                    // }
                },
                {
                    targets: [12],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `${data} <a href="#" onclick="javascript:ventanaSecundaria('../cbrbcod/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> <i class="fas fa-search-plus"></i></a>`
                    }else{return""}
                    }

                },
                
                {
                    targets: [13],
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
                        
                        $Etiqueta.attr('style', "width: 100px; height: 16px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-2 h-100 w-100 ' + classBackground);
                        
                        return $elDiv.clone().html();
                    }
                },
                
                {
                    targets: [14],
                    render: function (data, type, row,meta) {
                        if (row['linkconciliadobco']!= 0 && row['linkconciliadobco']!= null){
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
                    targets: [23],
                    render: function (data, type, row) {
                        if(((data != "0") && (data != null) && (data != undefined) && (data != '')) ){
                        return `${data} <a href="#" onclick="javascript:ventanaSecundaria('../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list')"> <i class="fas fa-search-plus"></i></a>
                    <script>
                    function ventanaSecundaria (URL){ 
                            window.open(URL,"Lupa","centerscreen=yes, top=10, left=50, width=520,height=650,toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no") 
                         } 
                    </script>`
                        }else{return""}
                    }

                },
                {
                    targets: [30],
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
                        
                        $Etiqueta.attr('style', "width: 100px; height: 16px");
                        $elDiv.append($('<div style="font-size: x-small;" class="dt-nowrap p-0">  </div>').append($Etiqueta));
                        $elDiv.children().removeClass();
                        $elDiv.children().addClass('callout callout-conc m-0 pt-2 h-100 w-100 ' + classBackground);
                        
                        return $elDiv.clone().html();
                    }
                },
                {
                    targets: [31],
                    render: function (data, type, row,meta) {
                        if (row['linkconciliadoerp']!= 0 && row['linkconciliadoerp']!= null){
                            let agregar = ""
                            for(let opcion = 0; opcion < globalVariableIndtco.indtco_bco.length; opcion++){
                                agregar = agregar + '<option value="'+globalVariableIndtco.indtco_bco[opcion]+'">'+globalVariableIndtco.indtco_bco[opcion]+'</option>'
                            }
                            let texto= `
                        <td><nobr>
                        <select name="tipo" id="optionerp-${row['idsres']}">
                        <option value="${table.row(meta.row).data()['codtcoerp']}">${table.row(meta.row).data()['codtcoerp']}</option>
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

