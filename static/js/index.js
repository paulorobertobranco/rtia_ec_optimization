$(document).ready(function(){
    $('#latitude').keyup(function(){
        var api = "https://www.google.com/maps/embed/v1/place?q=" + $(this).val() +",+" + $('#longitude').val() +"&key=" + $('#map').attr('data');
        $('#map').attr('src', api);
        
    });

    $('#longitude').keyup(function(){
        var api = "https://www.google.com/maps/embed/v1/place?q=" + $('#latitude').val() +",+" + $(this).val() +"&key=" + $('#map').attr('data');
        $('#map').attr('src', api);
        
    });

    $('#submit').click(function(){
         
         data = {

            "latitude": $('#latitude').val(),
            "longitude": $('#longitude').val(),
            "radius": $('#radius').val()
        };

        $.post('/get_pharmacies', data, function(response, status){

            var r = $.parseJSON(response);
            console.log(response);

            $("#result").css('display', 'initial');

            var locs = {
                x: r['lats'],
                y: r['longs'],
                mode: 'markers',
                name: 'pharmacies',
                type: 'scatter'
            };

            var best = {
                x: [r['hof'][0]],
                y: [r['hof'][1]],
                mode: 'markers',
                name: 'best_spot',
                type: 'scatter'
            };

            var center = {
                x: [40.677810],
                y: [-73.943432],
                mode: 'markers',
                name: 'center',
                type: 'scatter'
            };

            var data = [ locs, best, center ];

            var layout = {};

            Plotly.newPlot('myDiv', data, layout, {showSendToCloud: true});

        });

    });

});
