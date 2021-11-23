$(function () {
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
            {"data": "idtbco"},
            {"data": "pais"},
            {"data": "codbco"},
            {"data": "desbco"},
            {"data": "actpas", "render": function (data, type, full, meta) {
                if (data == "A"){
                    return "Activo"
                }else{
                    if (data=="P"){
                        return "Pasivo"
                    }else{
                        return data
                    }
                }
                }},
            {"data": null},
        ],
        columnDefs: [
            {
                targets:[0],
                visible: false
            },
            {
                targets: [1, 2,3,4],
                class: 'text-center pt-4',
            },
            {
                targets : [5],
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append('<div></div>');

    
                    var classMain = 'btn btn-app';

                    // ##### EDITAR #####
                    $elDiv.children().append($(
                        `<a class="${classMain}" href="edit/?idtbco=${row.idtbco}" ><i class="fas fa-edit"></i>Editar</a>`)
                        );
                    // ##### ELIMINAR #####
                    $elDiv.children().append($(
                        `<a id="btnEliminarE${row.codbco}" data-codbco="${row.codbco}" data-idtbco="${row.idtbco}" class="${classMain}" "><i  class="fas fa-trash-alt"></i>Eliminar</a>`));

                    return $elDiv.clone().html();

                },
            }
            

        ],
        
        initComplete: function (settings, json) {
            $(document).on("click", "a[id^=btnEliminarE]", function (event) {
                var idtbco = $(this).data('idtbco');
                var codbco = $(this).data('codbco');
                var parameters = {'idtbco': idtbco, 'index': $(this).data('index')};
                ajax_confirm("del/", 'Confirmación',
                    `¿Eliminar el banco ${$(this).data('codbco')}?`, parameters,
                    function (response) {
                        if (response.hasOwnProperty('info')) {
                            message_info(response['info'], null, null)
                            return false;
                        };
                        location.href = '/cbtbco';
                        return true;
                    }
                )},
            )},
                
    })
    
        
})
