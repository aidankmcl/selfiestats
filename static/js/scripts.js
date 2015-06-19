// overide default submit action to specifiy what to do with res
$('#form_holder > input').click(function() {
    /* 
    jQuery's 'post' method takes an endpoint, data,
    and optionally a success funtion that says what
    to do with returned data.
    */
    $.post('/crunch', $(this).serialize() , function(res) {

        res = JSON.parse(res)
        var ctx = document.getElementById("result").getContext("2d");

        var data = {
            labels: res['labels'],
            datasets: [
                {
                    label: "Emotions",
                    fillColor: "white",
                    data: res['scores']
                }
            ]
        };
        var myLineChart = new Chart(ctx).Bar(data, {
            showScale: false
        });

    });

    return false; // so that form doesn't try to complete post
});