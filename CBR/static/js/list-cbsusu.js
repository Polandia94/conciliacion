$(function () {
    $('#data thead tr').clone(true).appendTo( '#data thead' );
    $('#data thead tr:eq(1) th').each( function (i) {

      if(i !== 13) {

        var title = $(this).text();

        var busqueda = window.localStorage.getItem("conectados"  + i)
        $(this).html( function(){
            if (busqueda == null){
                return '<input type="text"/> '
            }else{
            return '<input type="text"value="'+busqueda+ '"/> '
      }});
        $( 'input', this ).on( 'keyup change', function () {
                window.localStorage.setItem("conectados"+i, this.value)
                var busqueda = window.localStorage.getItem("conectados"+i)
                if (busqueda != null){
                table
                    .column(i)
                    .search( busqueda )
                    .draw();
                }
            } );
        $( 'input', this ).ready(function () {
                var busqueda = window.localStorage.getItem("conectados"+i)
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
        //order:[],
        targets: 'no-sort',
        bSort: false,
        orderFixed: [ 2, 'desc' ],
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
            {"data":"idusu1"},
            {"data": "descusu"},
            {"data": "corrusu"},
            {"data": "iniciologin","render":function(data){
                if(moment(data).format('DD/MM/YYYY')=='Invalid date'){return ""}else{
                return moment(data).format('DD/MM/YYYY HH:mm:ss')}}},
            {"data": "finlogin","render":function(data){
                if(moment(data).format('DD/MM/YYYY HH:mm:ss')=='Invalid date'){return ""}else{
                return moment(data).format('DD/MM/YYYY HH:mm:ss')}}},
            {"data": "conectado", "render":function(data){
                if(data){return "Si"}else{return "No"}}}
        ],
        columnDefs: [

            {
                targets: [0, 1, 2, 3, 4,5],
                class: 'text-center pt-4',
                //orderable: false
            },
            
        ],
        
            })
    
        
})
