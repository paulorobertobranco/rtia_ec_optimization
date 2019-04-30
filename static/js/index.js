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
            "cxprob": $('#cxprob').val(),
            "mtprob": $('#mtprob').val()

        };

        $.post('/get_pharmacies', data, function(response, status){

            var r = $.parseJSON(response);

            if(r['status'] == 'ok'){

                var pharm = {
                    lat: r['pharm_lats'],
                    lon: r['pharm_longs'],
                    mode: 'markers',
                    name: 'pharmacies nearby',
                    type: 'scattermapbox',
                    text: r['pharm_names']
                };

                var hosp = {
                    lat: r['hosp_lats'],
                    lon: r['hosp_longs'],
                    mode: 'markers',
                    name: 'hospitals nearby',
                    type: 'scattermapbox',
                    text: r['hosp_names']
                };

                var pop = {
                    lat: r['init_pop_lats'],
                    lon: r['init_pop_longs'],
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

                var data = [ pop, pharm, hosp, center ];

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


                var best = {
                    lat: r['best_spot_lats'],
                    lon: r['best_spot_longs'],
                    mode: 'markers',
                    name: 'ec location result',
                    type: 'scattermapbox'
                };

                var data = [ pharm, hosp, center, best ];

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


                var pharm_std = {
                    x: r['gens'],
                    y: r['std_pharm'],
                    mode: 'lines',
                    type: 'lines',
                    name: 'pharm_dist'
                };

                var hosp_std = {
                    x: r['gens'],
                    y: r['std_hosp'],
                    mode: 'lines',
                    type: 'lines',
                    name: 'hosp_dist'
                };

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500
                };

                var data = [ pharm_std, hosp_std ];

                Plotly.newPlot('std-plot', data, layout);

                // ############################################################################# \\


                var pharm_avg = {
                    x: r['gens'],
                    y: r['avg_pharm'],
                    mode: 'lines',
                    type: 'lines',
                    name: 'pharm_dist'
                };

                var hosp_avg = {
                    x: r['gens'],
                    y: r['avg_hosp'],
                    mode: 'lines',
                    type: 'lines',
                    name: 'hosp_dist'
                };

                var layout = {
                    autosize: false,
                    width: 500,
                    height: 500
                };

                var data = [ pharm_avg, hosp_avg ];

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
