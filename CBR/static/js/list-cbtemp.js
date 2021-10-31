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
            {"data": "idtemp"},
            {"data": "pais"},
            {"data": "empresa"},
            {"data": "desemp"},
            {"data": "actpas"},
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
                        `<a class="${classMain}" href="edit/?idtemp=${row.idtemp}" ><i class="fas fa-edit"></i>Editar</a>`)
                        );
                    // ##### ELIMINAR #####
                    $elDiv.children().append($(
                        `<a id="btnEliminarE${row.empresa}" data-empresa="${row.empresa}" data-idtemp="${row.idtemp}" class="${classMain}" "><i  class="fas fa-trash-alt"></i>Eliminar</a>`));

                    return $elDiv.clone().html();

                },
            }
            

        ],
        
        initComplete: function (settings, json) {
            $(document).on("click", "a[id^=btnEliminarE]", function (event) {
                var idtemp = $(this).data('idtemp');
                var empresa = $(this).data('empresa');
                var parameters = {'idtemp': idtemp, 'index': $(this).data('index')};
                ajax_confirm("del/", 'Confirmación',
                    `¿Eliminar la empresa ${$(this).data('empresa')}?`, parameters,
                    function (response) {
                        if (response.hasOwnProperty('info')) {
                            message_info(response['info'], null, null)
                            return false;
                        };
                        location.href = '/cbtemp';
                        return true;
                    }
                )},
            )},
                
    })
    
        
})