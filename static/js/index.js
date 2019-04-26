$(document).ready(function(){
    $('#latitude').keyup(function(){
        var api = "https://www.google.com/maps/embed/v1/place?q=" + $(this).val() +",+" + $('#longitude').val() +"&key=" + $('#map').attr('data');
        $('#map').attr('src', api);
        
    });

    $('#longitude').keyup(function(){
        var api = "https://www.google.com/maps/embed/v1/place?q=" + $('#latitude').val() +",+" + $(this).val() +"&key=" + $('#map').attr('data');
        $('#map').attr('src', api);
        
    });

    $('#back').click(function(){
        $("#input").css('display', 'inline');
        $("#footer").css('display', 'block');
        $("#result").css('display', 'none');

    });

    $('#submit').click(function(){

        $("#input").css('display', 'none');
        $("#footer").css('display', 'none');
        $("#loader").css('display', 'block');
         
         data = {

            "latitude": $('#latitude').val(),
            "longitude": $('#longitude').val(),
            "radius": $('#radius').val(),
            "population": $('#population').val(),
            "generation": $('#generation').val(),
            "hof": $('#hof').val()

        };

        $.post('/get_pharmacies', data, function(response, status){

            var r = $.parseJSON(response);

            console.log(r['pop_lats']);
            console.log(r['pop_longs']);

            if(r['status'] == 'ok'){

                var locs = {
                    lat: r['lats'],
                    lon: r['longs'],
                    mode: 'markers',
                    name: 'pharmacies nearby',
                    type: 'scattermapbox',
                    text: r['names']
                };

                var pop = {
                    lat: r['pop_lats'],
                    lon: r['pop_longs'],
                    mode: 'markers',
                    name: 'initial population',
                    type: 'scattermapbox',
                };

                var center = {
                    lat: [r['center_spot'][0]],
                    lon: [r['center_spot'][1]],
                    mode: 'markers',
                    name: 'input location',
                    type: 'scattermapbox'
                };

                var data = [ pop, locs, center ];

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500,
                    hovermode:'closest',
                    mapbox: {
                    bearing:0,
                    center: {
                        lat: r['center_spot'][0],
                        lon: r['center_spot'][1]
                    },
                    yaxis: {
                        automargin: true
                    },
                    pitch:0,
                    zoom:12
                    },
                }

                Plotly.setPlotConfig({
                    mapboxAccessToken: 'pk.eyJ1IjoicGF1bG9icmFuY28iLCJhIjoiY2p1d21xd3YyMGUwNTRkc2tkNmxoMWZyNiJ9.SlJK610dPRl8h52h5TVTZg'
                })

                Plotly.newPlot('init-map-plot', data, layout);

                // ############################################################################# \\

                var locs = {
                    lat: r['lats'],
                    lon: r['longs'],
                    mode: 'markers',
                    name: 'pharmacies nearby',
                    type: 'scattermapbox',
                    text: r['names']
                };

                var best = {
                    lat: r['best_spot_lats'],
                    lon: r['best_spot_longs'],
                    mode: 'markers',
                    name: 'ec location result',
                    type: 'scattermapbox'
                };

                var center = {
                    lat: [r['center_spot'][0]],
                    lon: [r['center_spot'][1]],
                    mode: 'markers',
                    name: 'input location',
                    type: 'scattermapbox'
                };

                var data = [ locs, center, best ];

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500,
                    hovermode:'closest',
                    mapbox: {
                    bearing:0,
                    center: {
                        lat: r['center_spot'][0],
                        lon: r['center_spot'][1]
                    },
                    yaxis: {
                        automargin: true
                    },
                    pitch:0,
                    zoom:12
                    },
                }

                Plotly.setPlotConfig({
                    mapboxAccessToken: 'pk.eyJ1IjoicGF1bG9icmFuY28iLCJhIjoiY2p1d21xd3YyMGUwNTRkc2tkNmxoMWZyNiJ9.SlJK610dPRl8h52h5TVTZg'
                })

                Plotly.newPlot('map-plot', data, layout);

                // ############################################################################# \\


                var gens = {
                    x: r['gens'],
                    y: r['nevals'],
                    mode: 'markers',
                    type: 'lines+markers',
                };

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500
                };

                var data = [ gens ];

                Plotly.newPlot('eval-plot', data, layout);

                // ############################################################################# \\


                var gens = {
                    x: r['gens'],
                    y: r['avg'],
                    mode: 'lines',
                    type: 'lines',
                };

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500
                };

                var data = [ gens ];

                Plotly.newPlot('avg-plot', data, layout);

                $("#loader").css('display', 'none');
                $("#result").css('display', 'block');
                $("#footer").css('display', 'block');

            } else {
                alert(r['status'])
                $("#input").css('display', 'block');
                $("#footer").css('display', 'block');
                $("#loader").css('display', 'none');

            }


        });

    });

});
