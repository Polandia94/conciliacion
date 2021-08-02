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
                                            }
                },

                {
                    targets: [16],
                    createdCell: function (cell) {
                        $(cell).attr("data-look", 'debebco');
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
                    targets: [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,27,28,29,30],
                    className: "dt-nowrap pt-2 pb-2 pr-1 pl-1",
                    // createdCell: function (td,value, data){
                    //     /* CELDA POR CELDA DE LAS COLUMNAS EN targets */
                    // }
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
                
                $(row).children().addClass(classBackground);
                $(row).children().addClass('texto-cbsres');
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

