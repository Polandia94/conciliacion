$(function () {
    
        // Setup - add a text input to each footer cell
    $('#data thead tr').clone(true).appendTo( '#data thead' );
    $('#data thead tr:eq(1) th').each( function (i) {

      if(i !== 13) {

        var title = $(this).text();

        var busqueda = window.localStorage.getItem(i)
        $(this).html( function(){
            if (busqueda == null){
                return '<input type="text"/> '
            }else{
            return '<input type="text"value="'+busqueda+ '"/> '
      }});
        $( 'input', this ).on( 'keyup change', function () {
                window.localStorage.setItem(i, this.value)
                var busqueda = window.localStorage.getItem(i)
                if (busqueda != null){
                table
                    .column(i)
                    .search( busqueda )
                    .draw();
                }
            } );
        $( 'input', this ).ready(function () {
                var busqueda = window.localStorage.getItem(i)
                if (busqueda != null){
                    table
                        .column(i)
                        .search( busqueda )
                        .draw();
                    }
            } );
        }
        else {var title = $(this).text();

            $(this).html("")}
        

    } );
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
            {"data": "idrenc"},
            {"data": "empresa"},
            {"data": "codbco"},
            {"data": "nrocta"},
            {"data": "ano"},
            {"data": "mes"},
            {
                'data': 'estado', 'sClass': 'text-center pt-4', "render": function (data, type, full, meta) {
                    var zone_html = "";
                    if (data === "0") {
                        zone_html = 'Cargado'
                    }
                    if (data === "1") {
                        zone_html = 'Editado'
                    }
                    if (data === "2") {
                        zone_html = 'Conciliado'
                    }
                    if (data === "3") {
                        zone_html = 'Eliminado'
                    }
                    return zone_html;
                }
            },
            {"data": "recordbco"},
            {"data": "recorderp"},
            {"data": "saldobco"},
            {"data": "saldoerp"},
            {"data": "difbcoerp"},
            {"data": "usuario"},
            {"data": null}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6,12],
                class: 'text-center pt-4',
            },
            {
                targets: [9,10,11],
                class: 'text-center pt-4',
                render: function (data, type, row) {
                    return row['moneda'] + parseFloat(data).toLocaleString('en-US', {minimumFractionDigits:2})
                }
            },
            {
                targets: [7],
                width: "2%",
                class: 'text-center',
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append(
                        `<a  style="padding: 2px 7px !important; 
                                    margin-bottom: 2px !important; 
                                    height: 100% !important; 
                                    font-size: large !important; 
                                    color: #727272 !important; 
                                    width: 80%; " 
                                    class="btn btn-block btn-outline-info btn-sm" 
                                    href="cbrbcod/?idrbcoe=${row.idrenc}">
                                <i style="color: #4f4f4f!important;"  
                                          class="far fa-file-alt mr-2"></i> ${row['recordbco']} </a>`);
                    return $elDiv.clone().html();
                },
                "createdCell": function (td, cellData, rowData, row, col) {
                    $(td).css('padding-bottom', '0px');
                }
            },
            {
                targets: [8],
                width: "2%",
                class: 'text-center',
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append(
                        `<a  style="padding: 2px 7px !important; 
                                    margin-bottom: 2px !important; 
                                    height: 100% !important; 
                                    font-size: large !important; 
                                    color: #727272 !important; 
                                    width: 80%; " 
                                    class="btn btn-block btn-outline-info btn-sm" 
                                    href="cbrerpd/?idrerpe=${row.idrenc}">
                                <i style="color: #4f4f4f!important;"  
                                          class="far fa-file-alt mr-2"></i> ${row['recorderp']} </a>`);
                    return $elDiv.clone().html();
                },

                "createdCell": function (td, cellData, rowData, row, col) {
                    $(td).css('padding-bottom', '0px');
                }
            },
            {targets: [9],
                createdCell: function (cell) {
                    var row = table.row(cell)
                    if(row.data()['saldobcoori'] != null){
                        var monto = parseFloat(row.data()['saldobcoori']);
                        $(cell).attr("title", "Saldo Original: "+ row.data()['moneda'] + monto.toLocaleString('en-US', {minimumFractionDigits:2}))
                    }
                }
            },
            {targets: [10],
                createdCell: function (cell) {
                    var row = table.row(cell)
                    if(row.data()['saldobcoori'] != null){
                        var monto = parseFloat(row.data()['saldoerpori']);
                        $(cell).attr("title", "Saldo Original: "+row.data()['moneda'] + monto.toLocaleString('en-US', {minimumFractionDigits:2}))
                    }
                }
            },
            {
                targets: ['acciones-header'],
                class: 'text-center p-0',
                orderable: false,
                render: function (data, type, row) {
                    var classBackground = '';
                    var $elDiv = $('<div></div>');
                    $elDiv.append('<div></div>');

                    var CodeStatus = 0;
                    if (row['recorderp'] === 0 || row['recordbco'] === 0) {
                        CodeStatus = 0;
                    }
                    if (row['recorderp'] > 0 && row['recordbco'] > 0) {
                        if (row['recorderp'] !== row['recordbco']) {
                            CodeStatus = 1;
                        } else {
                            CodeStatus = 2;
                        }
                    }
                    if (row['estado'] == '3') CodeStatus = 4;
                    if (row['estado'] == '2') CodeStatus = 5; //nuevo codestatus 5 para conciliados
                    if (row["enuso"]) CodeStatus = 3;
                    var classMain = 'btn btn-app';
                    var classDetalles = '';
                    var classLog = '';
                    var classConciliar = '';
                    var classResultados = 'disabled';
                    var classEliminar = '';
                    var classIndicador = '';
                    var classVerConciliacion = '';
                    var classDesconciliar = '';

                    switch (CodeStatus) {
                        // Error no cargado
                        case 0: {
                            var classBackground = '';
                            classIndicador = 'callout-danger';
                            classDetalles = 'disabled'; //OK
                            classDesconciliar = 'disabled';
                            break;
                        }
                        // Cargado con misma cantidad de registros de ambos lados
                        case 1: {
                            classIndicador = 'callout-danger'; //OK
                            classDesconciliar = 'disabled';
                            break;
                        }
                        // Cargado con distinta cantidad de registros en cada lado
                        case 2: {
                            classIndicador = 'callout-danger';
                            classDesconciliar = 'disabled';
                            break;
                        }
                        // Conciliacion que se encuentra en uso
                        case 3: {
                            // classConciliar = 'disabled'; //OK
                            classResultados = ''; //OK
                            classEliminar = 'disabled'; //OK
                            classIndicador = 'callout-danger';
                            classConciliar = 'disabled';
                            classDesconciliar = 'disabled';
                            break;
                        }
                        // conciliacion eliminada
                        case 4: {
                            // classConciliar = 'disabled'; //OK
                            classResultados = ''; //OK
                            classEliminar = 'disabled'; //OK
                            classIndicador = 'callout-danger';
                            classConciliar = 'disabled';
                            classDesconciliar = 'disabled';

                            break;
                        }
                        case 5: {
                            // classConciliar = 'disabled'; //OK
                            classResultados = ''; //OK
                            classIndicador = 'callout-success';
                            classConciliar = 'disabled'
                            if(row.noDesconciliable){
                                classDesconciliar = 'disabled';
                            }

                            break;
                        }
                    }
                    $elDiv.children().addClass('callout m-0 bg-transparent ' + classIndicador);
                    // ##### CONCILIAR #####
                    $elDiv.children().append($(
                        `<a id="btnConciliar${row.idrenc}" class="${classMain}"data-estado="${row.estado}" data-idrenc="${row.idrenc}" ><i class="fas fa-clone"></i>Conciliar</a>`)
                        .addClass(classConciliar));
                    // ##### ELIMINAR #####
                    $elDiv.children().append($(
                        `<a id="btnEliminar${row.idrenc}" class="${classMain}" data-estado="${row.estado}" data-difbcoerp="${row.difbcoerp}" data-idrenc="${row.idrenc}""><i  class="fas fa-trash-alt"></i>Eliminar</a>`)
                        .addClass(classEliminar));
                    // ##### LOG #####
                    $elDiv.children().append($(
                        `<a class="${classMain}" href="log/?idrenc=${row.idrenc}" ><i class="fas fa-bars"></i>Log</a>`)
                        .addClass(classLog));

                    // ##### VER CONCILIAR #####
                    $elDiv.children().append($(
                        `<a class="${classMain}"data-estado="${row.estado}" data-idrenc="${row.idrenc}" href="cbsresview/?idrenc=${row.idrenc}" ><i class="fas fa-eye"></i>Ver</a>`)
                        .addClass(classVerConciliacion));
                    // ##### tiempos #####
                    $elDiv.children().append($(
                        `<a class="${classMain}" href="tiempo/?idrenc=${row.idrenc}" ><i class="fas fa-clock"></i>Tiempo</a>`)
                        .addClass(classLog));
                    // ##### desconciliar ######
                    if(globalVariable.classDesconciliador != 'False'){
                        $elDiv.children().append($(
                        `<a class="${classMain}" id="btnDesconciliar${row.idrenc}" data-idrenc="${row.idrenc}" ><i class="fas fa-unlock-alt"></i>Desconciliar</a>`)
                        .addClass(classDesconciliar)); 
                    }                   

                    return $elDiv.clone().html();

                },
            },

        ],
        createdRow: function (row, data, dataIndex) {
            var classBackground = '';
            switch (data['estado']) {
                case 0:
                    classBackground = 'bg-default';
                    break;
                case 1:
                    classBackground = 'bg-paraconciliar';
                    break;
                case 2:
                    classBackground = 'bg-enconciliacion';
                    break;
                case 3:
                    classBackground = 'bg-conciliado';
                    break;
                case 4:
                    classBackground = 'bg-conciliado';
                    break;
            }
            $(row).children().addClass(classBackground);
        },
        initComplete: function (settings, json) {
            $(document).on("click", "a[id^=btnConciliar]", function (event) {
                var idrenc = $(this).data('idrenc');
                $.ajax({
                    method: 'POST',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    url: '/posibilidaddeconciliar/',
                    data: {'idrenc': idrenc},
                    success: function (respons) { 
                        if(respons["posible"]== "si"){               
                            location.href = '/cbsres/?idrenc='+idrenc;
                        }else{
                            message_info("El folio se encuentra en uso", null, null)
                        }
                }
                })
            })
            $(document).on("click", "a[id^=btnEliminar]", function (event) {
                var idrenc = $(this).data('idrenc');
                var estado= $(this).data('estado');
                var difbcoerp = $(this).data('difbcoerp');
                var parameters = {'idrenc': idrenc, 'index': $(this).data('index')};
                ajax_confirm("cbrenc/del/", 'Confirmación',
                    `¿Eliminar la conciliación ${$(this).data('idrenc')}?`, parameters,
                    function (response) {
                        if (response.hasOwnProperty('info')) {
                            message_info(response['info'], null, null)
                            return false;
                        }
                        if (estado === "1"){
                        ajax_confirm("cbrenc/del/", 'Confirmación',
                        `¿Eliminar la conciliación? Se van a perder las modificaciones realizadas sobre el movimiento`, parameters,
                        function (response) {
                            if (response.hasOwnProperty('info')) {
                                message_info(response['info'], null, null)
                                return false;
                            }
                            location.href = 'cbrenc/del?idrenc='+idrenc;
                            return true;
                        })}
                        else{
                            if (difbcoerp == 0.00){
                                ajax_confirm("cbrenc/del/", 'Confirmación',
                                `¿Eliminar la conciliación? los saldos del movimiento estan conciliados`, parameters,
                                function (response) {
                                    if (response.hasOwnProperty('info')) {
                                        message_info(response['info'], null, null)
                                        return false;
                                    }
                                    location.href = 'cbrenc/del?idrenc='+idrenc;
                                    return true;
                                })}
                                else{
                                    location.href = 'cbrenc/del/?idrenc='+idrenc;
                                    return true;
                                };;
                        };
                    });
                        });
                        }
            });
            $(document).on("click", "a[id^=btnDesconciliar]", function (event) {
                var idrenc = $(this).data('idrenc');
                var parameters = {'idrenc': idrenc};
                ajax_confirm("cbrenc/desc/", 'Confirmación',
                    `¿Desconciliar la conciliación ${$(this).data('idrenc')}?`, parameters,
                    function (response) {
                        if (response.hasOwnProperty('info')) {
                            message_info(response['info'], null, null)
                            return false;
                        }else{
                            location.reload()
                        }
                    }
                )
                    
                    
            });
    $.fn.dataTable.ext.search.push(
        function (settings, searchData, index, rowData, counter) {
            

            if ($('#cbox_conciliados').is(":checked")) {
                return (rowData['estado'] <= 3)
            } else {
                return (rowData['estado'] != 2);

            }
        }
    );
    ;
        
});
