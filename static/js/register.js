id_first_name.addEventListener('input', check_button)
id_first_name.style.border = 'var(--red) 2px solid'

id_last_name.addEventListener('input', check_button)
id_username.addEventListener('input', check_username)
id_password.addEventListener('input', check_button)
id_confirm_password.addEventListener('input', check_button)

function check_word(name) {
        return /^[a-zA-Z]+$/.test(name) || /^[ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة]+$/.test(name);
}
var cond_1
var cond_2
function check_button(){
    try{
        username_value.innerHTML = id_username.value
    }
    catch{

    }
    submit_registration_button.setAttribute('disabled', '')
    if ( id_first_name.value && check_word(id_first_name.value)){
        id_first_name.style.border = 'var(--green) 2px solid'
        if ( id_last_name.value && check_word(id_last_name.value)){
            id_last_name.style.border = 'var(--green) 2px solid'
            if( username_checked && id_username.value ){
                id_username.style.border = 'var(--green) 2px solid'
                username_x.style.display = 'none'
                username_wrong.innerHTML = ""
                username_tick.style.display = 'inline'
                if(id_password.value.length >= 8 && id_password.value == id_confirm_password.value){
                    id_confirm_password.style.border = 'var(--green) 2px solid'
                    id_password.style.border = 'var(--green) 2px solid'
                    submit_registration_button.removeAttribute('disabled')
                }else{
                    id_confirm_password.style.border = 'var(--red) 2px solid'
                    id_password.style.border = 'var(--red) 2px solid'
                    submit_registration_button.setAttribute('disabled', '')
                    
                }
            }
            else{
                    id_username.style.border = 'var(--red) 2px solid'
                    username_x.style.display = 'inline'
                    username_tick.style.display = 'none'
                    id_confirm_password.style.border = ''
                    id_password.style.border = ''
                }

            
                
        }
        else{
        id_last_name.style.border = 'var(--red) 2px solid'
        id_username.style.border = ''
    }
            
    }
    else{
        id_first_name.style.border = 'var(--red) 2px solid'
        id_last_name.style.border = ''
    }
    
        
}

var username_checked = false
function check_username(){
    id_username.style.border = ''
    if (/^[a-zA-Z0-9_]+$/.test(id_username.value) ){
        loading_animation.style.display = 'block'
        username_tick.style.display = "none"
        username_x.style.display = "none"
        submit_registration_button.setAttribute('disabled', '')
        $.ajax({
            url : '/check-username/',
            data : {
                text : id_username.value
            },
            success: function(data){
                if (data == 'T'){
                    username_checked = true
                }
                else{
                    username_checked = false
                    if (id_username.value){
                        username_wrong.innerHTML = '"' + id_username.value + '" ' + trans_1
                    }else{
                        username_wrong.innerHTML = trans_2
                    }
                    
                }
                check_button()
                loading_animation.style.display = 'none'

            }
        })  
    }
    else{
        username_checked = false
        loading_animation.style.display = 'none'
        check_button()
        
        username_wrong.innerHTML = trans_2
    }
    

    
}

$('#id_first_name').on('keydown', function(e) {
	if (e.which == 32 && ! e.shiftKey) {
		e.preventDefault();
	}
});
$('#id_last_name').on('keydown', function(e) {
	if (e.which == 32 && ! e.shiftKey) {
		e.preventDefault();
	}
});

$('#id_username').on('keydown', function(e) {
	if (e.which == 32 && ! e.shiftKey) {
		e.preventDefault();
	}
});