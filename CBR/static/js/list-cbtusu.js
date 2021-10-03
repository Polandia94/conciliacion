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
            {"data": "idusu1"},
            {"data": "descusu"},
            {"data": "tipousu"},
            {"data": "actpas"},
            {"data": null}
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3],
                class: 'text-center pt-4',
            },
            {
                targets: [4],
                render: function (data, type, row) {
                    var $elDiv = $('<div></div>');
                    $elDiv.append('<div></div>');

    
                    var classMain = 'btn btn-app';

                    // ##### CONCILIAR #####

                    // ##### ELIMINAR #####
                    $elDiv.children().append($(
                        `<a id="btnResetear${row.idusu1}" data-idusu1="${row.idusu1}" class="${classMain}" "><i  class="fas fa-undo"></i>Resetear</a>`));

                    return $elDiv.clone().html();

                },

            }

        ],
        
        initComplete: function (settings, json) {
            console.log("existe")
            $(document).on("click", "a[id^=btnResetear]", function (event) {
                console.log("se apreto")
                console.log($(this))
                var idusu1 = $(this).data('idusu1');
                var parameters = {'idusu1': idusu1};
                console.log(idusu1)
                ajax_confirm("", 'Confirmación',
                    `¿Resetear el Password de ${$(this).data('idusu1')}?`, parameters,
                    function (response) {
                        location.href = 'res?usuario='+idusu1;
                        return true;
                    })
                })
            }
    })
    
        
})
