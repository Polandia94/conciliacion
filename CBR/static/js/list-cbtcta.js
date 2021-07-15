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
            {"data": "idtcta"},
            {"data": "empresa"},
            {"data": "codbco"},
            {"data": "nrocta"},
            {"data": "descta"},
            {"data": "monbasebco"},
            {"data": "monbaseerp"},
            {"data": "ano"},
            {"data": "mes"},
            {"data": "saldoinibco"},
            {"data": "saldoinierp"},
            {"data": null}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4, 5, 6,7,8,9,10],
                class: 'text-center pt-4',
            },
            {
                targets: ['acciones-header'],
                class: 'text-center p-0',
                orderable: false,
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append('<div></div>');
                    var classMain = 'btn btn-app';
                    var classEditar = '';
                    var classEliminar = '';
                    var CodeStatus = 0;
                    if (row['modificable'] == true) CodeStatus = 1;
                    switch (CodeStatus) {
                        case 0: {

                            classEditar = 'disabled'; //OK
                            classEliminar = 'disabled'; 
                            break;
                        }
                        case 1: {
                            break;}
                        }
                    $elDiv.children().addClass('callout m-0 bg-transparent ');
                    $elDiv.children().append($(
                        `<a class="${classMain}" href="edit/?idtcta=${row.idtcta}" ><i class="fas fa-edit"></i>Editar</a>`)
                        .addClass(classEditar));
                    // ##### ELIMINAR #####
                    $elDiv.children().append($(
                        `<a id="btnEliminarC${row.idtcta}" class="${classMain}" data-idtcta="${row.idtcta}""><i  class="fas fa-trash-alt"></i>Eliminar</a>`)
                        .addClass(classEliminar));
                    return $elDiv.clone().html();
                }
            }
            ],
            initComplete: function (settings, json) {
                $(document).on("click", "a[id^=btnEliminarC]", function (event) {
                    var idtcta = $(this).data('idtcta');
                    var parameters = {'idtcta': idtcta, 'index': $(this).data('index')};
                    ajax_confirm("del/", 'Confirmación',
                        `¿Eliminar la cuenta ${$(this).data('modificable')}?`, parameters,
                        function (response) {
                            if (response.hasOwnProperty('info')) {
                                message_info(response['info'], null, null)
                                return false;
                            };
                            location.href = '/cbtcta';
                            return true;
                        }
                    )},
                )},
                    }

               
            

                        
                        
        );
});

        
    
    
    
        

