$(document).ready(function () {
    /* var datas = $.get("/style", function (style) {
        $.ajax({
            type: "GET",
            url: "http://localhost:5000/",
            data: style,
            dataType: "json",
            success:
                $.each(style, function(index,value){
                    console.log(value);
                    $("#style_dropdown").append('<option>'+value+"</option>").selectpicker('refresh')
                })


        })
    }); */

    var datas = $.get("/names", function (style) {
        $.ajax({
            type: "GET",
            url: "http://localhost:5000/",
            data: style,
            dataType: "json",
            success:
                $.each(style, function(index,value){
                    console.log(value);
                    $("#beers_dropdown").append('<option>'+value+"</option>").selectpicker('refresh')
                })


        })
    });
})