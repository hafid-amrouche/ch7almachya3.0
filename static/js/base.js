
function onlyNumberKey(evt) {
		
	// Only ASCII character in that range allowed
	var ASCIICode = (evt.which) ? evt.which : evt.keyCode
	if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)){
		return false;
	}
		
	return true;
}

$(document).mouseup(function(e){
	var SB_1 = $("#search-input-1");
	var SB_2 = $("#search-input-2");

	// If the target of the click isn't the container
	if(!SB_1.is(e.target) && !SB_2.is(e.target)){
		document.getElementById('search-input-2-suggestions').style.display = 'none'
		document.getElementById('search-input-1-suggestions').style.display = 'none'
	}else{
		document.getElementById('search-input-2-suggestions').style.display = 'block'
		document.getElementById('search-input-1-suggestions').style.display = 'block'
	}
});




/* sidebar */
function openNav() {
	if (document.getElementById("mySidebar").style.transform != "translate(0%)"){
		document.getElementById("mySidebar").style.transition ="0.5s";
		document.getElementById("mySidebar").style.transform= "translate(0%)";
	}else{
		closeNav()
	}
		

	}

function closeNav() {
	document.getElementById("mySidebar").style.transform = "translate(-100%)";
	}

function show_hide(id){
	div = document.getElementById(id);
	if (div.style.display == "none"){
		var collection = document.getElementsByClassName("show_hide");
		for (let i = 0; i < collection.length; i++) {
			collection[i].style.display = "none";
			}
		
		var collection = document.getElementsByClassName("notification");
		for (let i = 0; i < collection.length; i++) {
			collection[i].style.background = "transparent";
			}

		div.style.display = "block";
	}
	else if (div.style.display == "block"){
		div.style.display = "none";
	}
}

document.getElementById('search-input-1').addEventListener('input', get_suggestions_1)
document.getElementById('search-input-2').addEventListener('input', get_suggestions_2)

function get_suggestions_1(){
	$.ajax({
		url: "/auto-complete-suggestions/",
		data : {
			words : document.getElementById('search-input-1').value
		},
		success : function(data){
			data = JSON.parse(data)
			var block;
			for (var i = 0; i < 5; i++){
				block = document.getElementById('suggestion_' + i)
				if (data[i]){
					block.style.display= 'block'
					block.innerHTML = data[i]
				}
				else{
					block.style.display= 'none'
				}

			}
		}
	})
}
function get_suggestions_2(){
	$.ajax({
		url: "/auto-complete-suggestions/",
		data : {
			words : document.getElementById('search-input-2').value
		},
		success : function(data){
			data = JSON.parse(data)
			var block;
			for (var i = 0; i < 5; i++){
				block = document.getElementById('suggestion_2_' + i)
				if (data[i]){
					block.style.display= 'block'
					block.innerHTML = data[i]
				}
				else{
					block.style.display= 'none'
				}

			}
		}
	})
}

function change_search_1(suggestion){
	document.getElementById('search-input-1').value = suggestion.innerHTML
	document.getElementById('search-input-1-suggestions').style.display = 'none'
	store_search(document.getElementById('search-input-1').value)
	document.getElementById('search-form-1').submit()
}
function change_search_2(suggestion){
	document.getElementById('search-input-2').value = suggestion.innerHTML
	document.getElementById('search-input-2-suggestions').style.display = 'none'
	store_search(document.getElementById('search-input-2').value)
	document.getElementById('search-form-2').submit()
}

function activate_dark_mode(){
	document.body.classList.add('dark-theme')
	document.getElementById('main-navbar').classList.add('navbar-dark')
	document.getElementById('main-navbar').classList.remove('navbar-light')
	document.getElementById('main-navbar-1').classList.add('navbar-dark')
	document.getElementById('main-navbar-1').classList.remove('navbar-light')
	
}

function deactivate_dark_mode(){
	document.body.classList.remove('dark-theme')
	document.getElementById('main-navbar').classList.add('navbar-light')
	document.getElementById('main-navbar').classList.remove('navbar-dark')
	document.getElementById('main-navbar-1').classList.add('navbar-light')
	document.getElementById('main-navbar-1').classList.remove('navbar-dark')

	
}

document.getElementById('change-mode').addEventListener('change', function() {
	if (this.checked) {
		activate_dark_mode()
		$.ajax({
		url : '/activate-dark-mode/'
		})
	} 
	else {
		deactivate_dark_mode()
		$.ajax({
			 url : '/deactivate-dark-mode/'
		  })
		
	}
  });


$('#search-input-1').on('keydown', function(e) {
	if (e.which == 13 && ! e.shiftKey) {
		e.preventDefault();
	}
	return /[a-zA-Z0-9 ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة-]/i.test(e.key)
});

$('#search-input-2').on('keydown', function(e) {
	if (e.which == 13 && ! e.shiftKey) {
		e.preventDefault();
	}
	return /[a-zA-Z0-9 ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة-]/i.test(e.key)
});


function store_search(text){
	$.ajax({
		url: '/store-search/',
		data: {
			text : text
		}
	})
}

document.getElementById('search-form-2').addEventListener('submit', (e)=>{
	store_search(document.getElementById('search-input-2').value)
})
document.getElementById('search-form-1').addEventListener('submit', (e)=>{
	store_search(document.getElementById('search-input-1').value)
})