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
        document.getElementById('bt1').click();
    } 
}

