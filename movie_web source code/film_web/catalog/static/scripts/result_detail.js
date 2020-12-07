$.fn.raty.defaults.path = '../images/img/';

$(function() {
    var score = $('#current_rating').text();

    $('#star').raty({
        half: false,
        hints: [1, 2, 3, 4, 5],
        path: 'https://raw.githubusercontent.com/wbotelhos/raty/master/lib/images/',
        target: '#rate_value',
        targetKeep: false,
        //targetType : 'score',
        targetType: 'hint',
        //precision  : true,
        score: score,
        scoreName: 'score',
        click: function (rating, evt) {
            document.getElementById('bt1').click();
        },
        starType: 'i'
    });

    // on form submit do your test....
    $('#form').on('submit', function(e) {
        if ($('#star').raty('score') == '0') {
        e.preventDefault();
        console.log('error: raty is 0!');
        return;
        }
    });
});
