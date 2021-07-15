var globalVariable={
    editado: 0
 };
 var globalVariableSaldo={
    saldo: 0
 };


$(function () { "use strict"
    $(document).ready(function() {

        

        globalVariable.editado = 0;
        globalVariableSaldo.saldo = 0;
        const urlParams = new URLSearchParams(window.location.search);
        const idrenc = urlParams.get('idrenc');
        let table = $('#data').DataTable({
            scrollX: true,
            order: [[0, 'asc']],
            deferRender: true,
            colReorder: true,
            stateSave: true,
            fixedHeader: true,
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
            responsive: true,
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
                {"data": "fechatrabco", name: "fechatrabco"},
                {"data": "horatrabco"},
                {"data": "debebco", name: "debebco", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {"data": "haberbco", name: "haberbco", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {"data": "saldobco", name: "saldobco", render: $.fn.dataTable.render.number(',', '.', 2, '$')},
                {
                    "data": "saldoacumesbco",
                    name: "saldoacumesbco",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$')
                },
                {
                    "data": "saldoacumdiabco",
                    name: "saldoacumdiabco",
                    render: $.fn.dataTable.render.number(',', '.', 2, '$')
                },
                {"data": 'idrbcod'},
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
                {"data": 'oficinabco'},
                {"data": 'desctrabco'},
                {"data": 'reftrabco'},
                {"data": 'codtrabco'},
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
                        $(cell).attr("data-look", 'debeerp');
                    }
                },
                {
                    targets: [4],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'habererp');
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
                    targets: [10],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'fechatrabco');
                    }
                },
                {
                    targets: [11],
                    createdCell: function (cell) {

                        $(cell).attr("data-look", 'debebco');
                        let original
                        let saldo = parseFloat(0);

                        saldo = parseFloat(table.cell( 0,14 ).data())-parseFloat(table.cell( 0,11 ).data())+parseFloat(table.cell( 0,12 ).data())
                        globalVariableSaldo.saldo = saldo

                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

                        })

                        cell.addEventListener('blur', function(e) {
                            if ( original == 0 || original == null || original == "$0.00"){
                                e.target.textContent = original
                            }
                            else if (original !== e.target.textContent) {

                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)

                                row.data()['debeerp']=e.target.textContent


                                /*  
                                  Cambia los valores del resto de las celdas
                                */



                                
                                let total = parseFloat(0);




                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)

                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,11).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,12).data().replace("$",""))){
                                        row.data()['isconciliado']=2}else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){ 
                                        row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                                }else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){
                                    row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                    
                                    
                                var historial = table.cell( row,28 );


                                if (row.data()['isconciliado'] == 1){
                                    historial.data( "1").draw();
                                }else{
                                    historial.data( "4").draw();
                                }


                                for (let fila = 0; fila < table.rows().count()+1; fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,11).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,11).data().replace("$",""))
                                    total = total + totalmas
                                }



                                let saldomas = parseFloat(0)
                                if (table.cell(fila,11).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,11).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,12).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,12).data())}


                                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,14 ).data(saldoi).draw();




                                table.cell( row,16 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,14).data())).draw();

                                if (table.cell(fila-1,10).data()==table.cell(fila,10).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,15 ).data(saldodia).draw();
                                var rows = table.row(fila)
                                


                                debeerp.innerHTML = total;
 
                                table.rows().invalidate().draw();


                                

                                
                                
                                  
                              }
 
                            }
                          })
                    }
                },
                {
                    targets: [12],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'haberbco');
                        let original
                        let saldo = parseFloat(0);

                        saldo = parseFloat(table.cell( 0,14 ).data())-parseFloat(table.cell( 0,11 ).data())+parseFloat(table.cell( 0,12 ).data())
                        globalVariableSaldo.saldo = saldo


                        cell.setAttribute('spellcheck', false)

                        cell.addEventListener('focus', function(e) {

                            original = e.target.textContent

                        })

                        cell.addEventListener('blur', function(e) {
                            if ( original == 0 || original == null || original == "$0.00"){
                                e.target.textContent = original
                            }
                            else if (original !== e.target.textContent) {

                                var tr = $(this);
                                tr.css('color', '#ff0000');
                                globalVariable.editado = 1
                                var row = table.row(e.target.parentElement)

                                row.data()['habererp']=e.target.textContent


                                /*  
                                  Cambia los valores del resto de las celdas
                                */



                                
                                let total = parseFloat(0);




                                let saldodia = parseFloat(0)
                                let saldoi = parseFloat(0)
                                saldoi = parseFloat(globalVariableSaldo.saldo)


                                if (table.cell(row,4).data() != null){
                                    if(parseFloat(table.cell(row,11).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,12).data().replace("$",""))){
                                        row.data()['isconciliado']=2}else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){ 
                                        row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}
                                }else if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']==""){
                                    row.data()['isconciliado']=1}else{row.data()['isconciliado']=2}

                                var historial = table.cell( row,28 );


                                if (row.data()['isconciliado'] == 1){
                                    historial.data( "1").draw();
                                }else{
                                    historial.data( "4").draw();
                                }


                                for (let fila = 0; fila < table.rows().count()+1; fila++) {

                                let totalmas = parseFloat(0)


                                if(table.cell(fila,11).data() == null){
                                    totalmas = parseFloat(0)
                                    total = total + totalmas   
                                } else{
                                    totalmas = parseFloat(table.cell(fila,11).data().replace("$",""))
                                    total = total + totalmas
                                }



                                let saldomas = parseFloat(0)
                                if (table.cell(fila,11).data()==null){
                                    saldomas = parseFloat(0)
                                }else{saldomas = parseFloat(table.cell(fila,11).data())}

                                let saldomenos = parseFloat(0)

                                if (table.cell(fila,12).data()==null){
                                    saldomenos = parseFloat(0)
                                }else{saldomenos = parseFloat(table.cell(fila,12).data())}


                                
                                saldoi =  saldoi + parseFloat(saldomas) - parseFloat(saldomenos);
                                
                                table.cell( fila,14 ).data(saldoi).draw();




                                table.cell( row,16 ).data(parseFloat(table.cell(row,6).data().replace("$","")) - parseFloat(table.cell(row,14).data())).draw();

                                if (table.cell(fila-1,10).data()==table.cell(fila,10).data()){
                                    saldodia = saldodia + saldomas - saldomenos
                                }else{
                                    saldodia = saldomas - saldomenos
                                }
                                table.cell( fila,15 ).data(saldodia).draw();
                                var rows = table.row(fila)
                                

                                habererp.innerHTML = total;
                                table.rows().invalidate().draw();                                

                                

                                
                                  
                                }
                            }
                          })
                    }
                },

                {
                    targets: [13],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldobco');
                    }
                },

                {
                    targets: [14],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumesbco');
                    }
                },
                {
                    targets: [15],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'saldoacumdiabco');
                    }
                },

                {
                    targets: [30],
                    createdCell: function (cell) {
                        let original

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
                                    historial.data( "1").draw();
                                }else{
                                    historial.data( "4").draw();
                                }                                
  
                                if(table.cell(row,4).data() == null || table.cell(row,11).data() == null || table.cell(row,12).data() == null || table.cell(row,3).data() == null){
                                    if(row.data()['linkconciliado']==undefined || row.data()['linkconciliado']==null || row.data()['linkconciliado']=="") {
                                        row.data()['isconciliado']=1
                                        }else{row.data()['isconciliado']=2}
                                }else{
                                    if(parseFloat(table.cell(row,11).data().replace("$",""))==parseFloat(table.cell(row,4).data().replace("$","")) &&  parseFloat(table.cell(row,3).data().replace("$",""))==parseFloat(table.cell(row,12).data().replace("$",""))){
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

                                table.rows().invalidate().draw();
                                

                                  
                                
  
                                
                                
  
                                
                                
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
                    targets: [8],
                    render: function (data, type, row) {
                        return `${data} <a href="../cbrbcod/${data}/${idrenc}/?return_url=CBR:cbsres-list" > <i class="fas fa-search-plus"></i></a>`
                    }

                },
                {
                    targets: [17],
                    render: function (data, type, row) {

                        return `${data} <a href="../cbrerpd/${data}/${idrenc}/?return_url=CBR:cbsres-list" > <i class="fas fa-search-plus"></i></a>`
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
                        $elDiv.children().addClass('callout callout-conc m-0 pt-2 h-100 w-100' + classBackground);
                        return $elDiv.clone().html();
                    }
                },
                
                {
                    targets: [16],
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

