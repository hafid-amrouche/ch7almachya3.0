function load(my_button){
    var product_name = document.getElementById("id_name");
    var dist = document.getElementById('id_distance');
    if ( product_name.value != "" && dist.value != ""){
      my_button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; background: transparent; display: block; shape-rendering: auto; animation-play-state: running; animation-delay: 0s;" height="24px" width="auto" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid"><circle cx="50" cy="50" fill="none" stroke="#fff" stroke-width="10" r="35" stroke-dasharray="164.93361431346415 56.97787143782138" style="animation-play-state: running; animation-delay: 0s;"><animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50;360 50 50" keyTimes="0;1" style="animation-play-state: running; animation-delay: 0s;"></animateTransform></circle><!-- [ldio] generated by https://loading.io/ --></svg>';
    }
  }
let multipleUploader = new MultipleUploader('#multiple-uploader').init({
    maxUpload : 20, // maximum number of uploaded images
    maxSize:20, // in size in mb
    filesInpName:'images', // input name sent to backend
    formSelector: '#my-form', // form selector
});


function check_word(name) {
    return /^[a-zA-Z0-9 -]+$/.test(name) || /^[0-9 ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة-]+$/.test(name);
}

id_name.style.border = "2px var(--red) solid"
id_distance.style.border = "2px var(--red) solid"
document.getElementById('multiple-uploader').style.border = "2px var(--red) solid"

id_distance.value = 0


id_name.addEventListener('input', check_button)
id_distance.addEventListener('input', check_button)

setInterval(function(){
    check_button()
}, 500)

$('#id_name').on('keydown', function(e) {
	if (e.which == 13 && ! e.shiftKey) {
		e.preventDefault();
	}
    return check_word(e.key)
});


flexSwitchCheckChecked.addEventListener('change', function(){
    if (this.checked){
        document.getElementById('options-div').style.display = 'none'
    }else{
        document.getElementById('options-div').style.display = 'block'
    }
})


id_price.value = 0 
id_given_price.value = 0 
let others_list = [
    'other countries|Another brand',
    'france|French brand',
    'germany|German brand',
    'japan|Japanese brand',
    'USA|American brand',
    'england|Brirish brand',
    'Italy|Italian brand',
    'china|Chinese brands'
]
document.getElementById('category-select').addEventListener('change', ()=>{
    if (others_list.includes(document.getElementById('category-select').value)){
    id_new_category_div.style.display = "block"
    }
    else{
    id_new_category_div.style.display = "none"
    }
    check_button()
})

function check_button(){
    cond_1 = check_word(id_name.value)
    cond_2 = Number(id_distance.value) >= 0
    cond_3 = id_images.files.length 
    cond_4 = (others_list.includes(document.getElementById('category-select').value) && check_word(id_new_category.value)) || !others_list.includes(document.getElementById('category-select').value)
    
    if (cond_1){
        id_name.style.border = ""
    }else{        
        id_name.style.border = "2px var(--red) solid"
    }
    if (cond_2){
        id_distance.style.border = ""
    }else{
        id_distance.style.border = "2px var(--red) solid"
    }
    if (cond_3){
        document.getElementById('multiple-uploader').style.border = ""
    }else{
        document.getElementById('multiple-uploader').style.border = "2px var(--red) solid"
    }
    if (cond_4){
        id_new_category.style.border = ""
    }else{
        id_new_category.style.border = "2px var(--red) solid"
    }

   if (cond_1 && cond_2 && cond_3 && cond_4){
    load_button.removeAttribute('disabled') 
   }else{
    load_button.setAttribute('disabled', '') 
   }
}

$('#id_new_category').on('keydown', function(e) {
    return check_word(e.key)
});

$('#id_new_category').on('keyup', function(e) {
    check_button()
});