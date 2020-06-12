let randomColor = function (numbers) { 
    colors = {borders:[], backgrounds:[]}
    for (var i = 0; i < numbers; i++) {
        var num = Math.round(0xffffff * Math.random());
        var r = num >> 16;
        var g = num >> 8 & 255;
        var b = num & 255;
        back = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + 0.2 + ')';
        bord = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + 1 + ')';
        colors.borders.push(bord);
        colors.backgrounds.push(back);
    };
    return colors;
};

var ctx = document.getElementById('chartPersonnel').getContext('2d');

function plot(){
    $.ajax({
        url: '/api/chart_perso/service/',
        type: 'GET',
        dataType: 'json',
    })
    .done(function(data) {
        labels = []
        datas = []
        for(var item of data){
            labels.push(item["serveur__username"]);
            datas.push(item["commandes"]);
        }
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                colors : randomColor(labels.length), // personnalization
                datasets: [{
                    label: '# of Votes',
                    data: datas,
                    backgroundColor: colors.backgrounds,
                    borderColor: colors.borders,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });
}
plot();