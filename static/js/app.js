var url = "/api/data";

var globalData;

Plotly.d3.json(url, function(err, response) {
    console.log(response);

    globalData = response;

    var trace = {
        x: response.map(d=>d.title),
        y: response.map(d=>d.year),
        type: 'bar'
    }

    var data = [trace];

    var layout = {
        title: "A Real Dumb Bar Chart"
    }

    Plotly.newPlot("plot", data, layout);

})