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
            {"data":"idtusu"},
            {"data": "idusu1"},
            {"data": "descusu"},
            {"data": "tipousu", "render": function (data, type, full, meta) {
                if (data == "S"){
                    return "Sí"
                }else{
                    return data
                }
                }
            },
            {"data": "indconc", "render": function (data, type, full, meta) {
                if (data == "S"){
                    return "Sí"
                }else{
                    return data
                }
                }},
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
            {"data": null}
        ],
        columnDefs: [
            {
                targets: [0],
                visible: false
            },
            {
                targets: [1, 2, 3, 4,5],
                class: 'text-center pt-4',
            },
            {
                targets: [6],
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append('<div></div>');
                    var classEliminar = '';
                    if (row['modificable'] != true || row['eliminable'] != true){
                    classEliminar = 'disabled'; 
                    }
    
                    var classMain = 'btn btn-app';


                    $elDiv.children().append($(
                        `<a id="btnResetear${row.idusu1}" data-idusu1="${row.idusu1}" class="${classMain}" "><i  class="fas fa-undo"></i>Resetear</a>`));
                    
                    $elDiv.children().append($(
                            `<a id="btnEditar${row.idusu1}" data-idusu1="${row.idusu1}" data-idtsu="${row.idusu}" href="edit/?idusu1=${row.idusu1}&idtusu=${row.idtusu}" class="${classMain}" "><i  class="fas fa-edit"></i>editar</a>`));
                        
                    $elDiv.children().append($(
                        `<a id="btnEliminarU${row.idusu1}" class="${classMain}" data-idusu1="${row.idusu1}""><i  class="fas fa-trash-alt"></i>Eliminar</a>`)
                        .addClass(classEliminar));
                    
                    return $elDiv.clone().html();



                },

            }

        ],
        
        initComplete: function (settings, json) {
            $(document).on("click", "a[id^=btnResetear]", function (event) {
                var idusu1 = $(this).data('idusu1');
                var parameters = {'idusu1': idusu1};
                ajax_confirm("", 'Confirmación',
                    `¿Resetear el Password de ${$(this).data('idusu1')}?`, parameters,
                    function (response) {
                        location.href = 'res?usuario='+idusu1;
                        return true;
                    })
                })
                $(document).on("click", "a[id^=btnEliminarU]", function (event) {
                    var idusu1 = $(this).data('idusu1');
                    var parameters = {'idusu1': idusu1, 'index': $(this).data('index')};
                    ajax_confirm("del/", 'Confirmación',
                        `¿Eliminar el usuario ${$(this).data('idusu1')}?`, parameters,
                        function (response) {
                            if (response.hasOwnProperty('info')) {
                                message_info(response['info'], null, null)
                                return false;
                            };
                            location.href = '/cbtusu';
                            return true;
                        }
                    )})
            }
    })
    
        
})
