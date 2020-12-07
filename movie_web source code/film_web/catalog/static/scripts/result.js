'use strict';

var searchBox = document.querySelectorAll('.search-box input[type="text"] + span');

searchBox.forEach(function (elm) {
	elm.addEventListener('click', function () {
		elm.previousElementSibling.value = '';
	});
});

function EnterPress(){ //传入 event 
    var ieKey = event.which;
    if( ieKey == 13){
        var options = $("#search_type option:selected");
        var myselect = document.getElementById("search_type");
        var index = myselect.selectedIndex;
        $('#input2').val(options.val());
        $('#input3').val(index);
        $('#search_type').val(options.val());
        
        document.getElementById('bt1').click();
    } 
}

function change_type() {
    var type = $('#option_id').text();
    var all_options = document.getElementById("search_type").options;
    all_options[type].selected = true;
}


