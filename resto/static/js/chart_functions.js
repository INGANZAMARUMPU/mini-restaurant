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
function resizeChart(element, length){
    $element = $("#"+element);
    $div = $element.parent('div');
    if(screen.width < 650){
        if(length<4){
            size = length*100;
        }else{
            size = length*50;
        }
    }else{
        if(length<4){
            size = length*200;
        }else{
            size = length*100;
        }
    }
    $element.attr('width', size);
    $div.css('width', size);
}

function plotBar(element, url, label){
    var ctx = document.getElementById(element).getContext('2d');
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
    })
    .done(function(data) {
        labels = []
        datas = []
        for(var item of data){
            labels.push(item["labels"].slice(0,15));
            datas.push(item["datas"]);
        }
        resizeChart(element, labels.length);
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                colors : randomColor(labels.length), // personnalization
                datasets: [{
                    label: label,
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