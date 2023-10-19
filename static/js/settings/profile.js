
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
my_button = save
var width = my_button.offsetWidth + 2
my_button.style.width = "" + width +"px";
function check_email(my_button){
    if ( id_email.value != user_email ){
        var retVal = confirm('You changed your email. If you continue you will have to confirm the new email');
        if ( retVal == true ){
            return true;
        }
        else {
            id_email.value = user_email;
            my_button.innerHTML = trans_1;
            return false;
        }
    }

}

