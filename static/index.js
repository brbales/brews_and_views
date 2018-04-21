$(document).ready(function () {
     var datas = $.get("/style", function (style) {
        $.ajax({
            type: "GET",
            url: "http://localhost:5000/",
            data: style,
            dataType: "json",
            success:
                $.each(style, function(index,value){
                    console.log(value);
                    $("#styles_dropdown").append('<option>'+value+"</option>").selectpicker('refresh')
                })


        })
    }); 

   /*  var datas = $.get("/names", function (style) {
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
    }); */
})

/* $('select[name="country"]').on('change', function() {
    var countryId = $(this).val();

    $.ajax({
        type: "POST",
        url: "get-province.php",
        data: {country : countryId },
        success: function (data) {
                    //remove disabled from province and change the options
                    $('select[name="province"]').prop("disabled", false);
                    $('select[name="province"]').html(data.response);
        }
    });
}); */