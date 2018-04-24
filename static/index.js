$(document).ready(function () {
    var datas = $.get("/style", function (style) {
        $.ajax({
            type: "GET",
            url: "http://localhost:5000/",
            data: style,
            dataType: "json",
            success: $.each(style, function (index, value) {
                console.log(value);

                function URLify(value) {
                    return value.trim().replace(/\s/g, '%20');
                }
                $("#styleDropdown").append('<option value=' + URLify(value) + ">" + value + "</option>").selectpicker('refresh')
            })


        })
    });
    $('#beerDropdown').attr('disabled', true);
    $("#styleDropdown").change(function () {
        // $('#suggestion').remove(5);
        $('#beerDropdown').empty();
        $('#beerDropdown').attr('disabled', false);
        var query = $(this).val();
        console.log(query);
        var datas = $.get(`/beers/${query}`, function (style) {
            $.ajax({
                type: "GET",
                url: "http://localhost:5000/",
                data: style,
                dataType: "json",
                success: $.each(style, function (index, value) {
                    console.log(value);

                    function URLify(value) {
                        return value.trim().replace(/\s/g, '%20');
                    }
                    $("#beerDropdown").append('<option value=' + URLify(value) + ">" + value + "</option>").selectpicker('refresh')
                })


            })
        });

    });
    $("#beerDropdown").change(function () {
        var query = $(this).val();
        console.log(query);
        var datas = $.get(`/recommendations/${query}`, function (beer) {
            $.ajax({
                type: "GET",
                url: "http://localhost:5000/",
                data: beer,
                dataType: "json",
                success: $.each(beer, function (index, value) {
                    function URLify(value) {
                        return value.trim().replace(/\s/g, '%20');
                    }
                    console.log(beer[index][0]);
                    $('#suggestions_list').append('<p id="suggestion"><b>Name:</b> ' + beer[index][0] + " <b>Style:</b> " + beer[index][1] + " <b>ABV:</b> " + beer[index][2] + " <b>IBU:</b> " + beer[index][3] + " <b>Color:</b> " + beer[index][4] + "</p>")

                    /*$("#beerDropdown").append('<option value=' + value + ">" + value + "</option>").selectpicker('refresh') */

                })


            });
        });

    })

    

});