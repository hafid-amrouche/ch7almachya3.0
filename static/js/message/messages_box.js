function showTime(text_id){
    texty = document.getElementById(text_id);
    if (texty.className == "small text-right mb-0  collapse hide") {
      var collection = document.getElementsByClassName("small text-right mb-0  collapse show");
          for (let i = 0; i < collection.length; i++) {
            collection[i].setAttribute("class", "small text-right mb-0  collapse hide");
          }
        
      texty.setAttribute('class', 'small text-right mb-0  collapse show');
    }
    else if (texty.className == "small text-right mb-0  collapse show") {
      texty.setAttribute('class', 'small text-right mb-0  collapse hide');
    }
    
  }



let chat_box = document.querySelector(".chat-history");
let message_btn = document.getElementById("submi_button");
let message_input = document.getElementById("text-input");
var page = 1;
var messages_list_IDs = []
var load_next_clicked = false
var load_prev_clicked = false
message_btn.addEventListener('click', send_message);

function load_prev(){
    document.querySelector('#load-prev').innerHTML = 
    `
    <svg xmlns="http://www.w3.org/2000/svg" id="loading_svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="align-self:center; order:1; background: none; shape-rendering: auto; min-width: 50px; height:50px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                        <circle cx="50" cy="50" fill="none" stroke="var(--green)" stroke-width="10" r="40" stroke-dasharray="188.49555921538757 64.83185307179586">
                          <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50;360 50 50" keyTimes="0;1"/>
                        </circle>
                      </svg>
    `
    page = page + 1
    messages_list_IDs = []
    load_prev_clicked = true
    load_messages()
}
function load_next(){
    document.querySelector('#load-next').innerHTML = 
    `
    <svg xmlns="http://www.w3.org/2000/svg" id="loading_svg" xmlns:xlink="http://www.w3.org/1999/xlink" class='mb-4' style="align-self:center; order:1; background: none; shape-rendering: auto; min-width: 50px; height:50px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                        <circle cx="50" cy="50" fill="none" stroke="var(--green)" stroke-width="10" r="40" stroke-dasharray="188.49555921538757 64.83185307179586">
                          <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50;360 50 50" keyTimes="0;1"/>
                        </circle>
                      </svg>
    `
    page = page - 1
    messages_list_IDs = []
    load_next_clicked = true
    load_messages()

}

function send_message(){
    if (message_input.value) {
        $.ajax({
        type: 'POST',
        url: ajax_save_link,
        data:{
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            message : $('#text-input').val(),
        },
        success: function(){
            load_messages_list()
        }
        });
        if (page == 1){
        let ul = document.createElement('ul');
        ul.className = "mb-1 to-be-deleted";
        ul.innerHTML = 
            `            
            <li class="clearfix text-right">
                <div class="message other-message" style='background-color:var(--white)'> <p style="font-weight: 600;letter-spacing: 0.8px;text-align: left; color:var(--green)">${message_input.value}</p> </div>
            </li>                  
            `
        chat_box.prepend(ul);
        document.getElementsByClassName('chat-history')[0].scrollTop = 0;
        }
        message_input.value = "";

    }

}

function load_messages(){
    $.ajax({
        type: 'GET',
        url: ajax_load_link,
        data:{
        page: page
        },
        success: function(data){
            $('.to-be-deleted').remove();
            data = JSON.parse(data);
            page = Number(data[1])
            
            messages = data[0]
            if (load_next_clicked || load_prev_clicked){
                document.getElementsByClassName('chat-history')[0].innerHTML = ''
            }

            for( message of messages[0] ){
                if( messages_list_IDs.includes(message['id'])){
                    continue
                }
                else{
                    messages_list_IDs.push(message['id'])
                    class_name = 'left'
                    backgound = 'var(--green)'
                    color = 'var(--white)'
                    if (message.is_user_sender) {
                        class_name = 'right';
                        backgound = 'var(--white)'
                        color = 'var(--green)' 
                    }
                    let ul = document.createElement('ul');
                    ul.className = "mb-1";
                    ul.id = 'message_' + message['id']
                    ul.innerHTML = 
                    `            
                        <li class="clearfix text-${class_name}">
                            <div class="message other-message" style='background-color: ${ backgound }' onclick="showTime('text_time_${message.id}')"> <p style="font-weight: 600;letter-spacing: 0.8px;text-align: left; color: ${ color }">${message.text}</p></div>
                            <div style="width: 100%;" class="text-${class_name}"> 
                            <span style="font-size: 0.8rem;" id="text_time_${message.id}" class="small text-right mb-0  collapse hide">${message.time}</span>       
                            </div>
                        </li>                  
                    `
                    chat_box.prepend(ul);
                    message_index = message.id;
                }
            }
            if(data[2]  && !document.getElementById('load-prev')){
                chat_box.innerHTML = 
                chat_box.innerHTML +
            
                `
                <div id="load-prev" style="text-align: center; cursor:pointer; margin-top: 30px"><span class='btn btn-outline-success btn-sm' onclick='load_prev()'>Load prev</span></div>
                `
                document.getElementById('chat-history').scrollTo(0, 0)
            }

            if(data[3]  && !document.getElementById('load-next')){
                chat_box.innerHTML = 
                `
                        <div id="load-next" style="text-align: center; cursor:pointer; margin-bottom: 10px;">
                            <span class='btn btn-outline-success btn-sm' onclick='load_next()' >Load next</span>
                        </div>
                ` + chat_box.innerHTML
                if ( !data[2] ){
                    document.getElementById('chat-history').scrollTo(0, 0)
                }
            }  
            if (load_next_clicked ){
                window.location.href = "#load-prev" ;
            }
            load_next_clicked = false
            load_prev_clicked = false
        }
        
    });
};


let plist_3 = document.getElementById('plist_3')
var messages_page = 1;
show_older.addEventListener('click', function(){
    messages_page = messages_page + 1
    load_messages_list()
}
)
show_later.addEventListener('click', function(){
    messages_page = messages_page - 1
    load_messages_list()
}
)

function load_messages_list(){
    $.ajax({
    type: 'GET',
    data : {
        messages_page : messages_page,
    },
    url: ajax_messages_list_link,
    success: function(data){
        data = JSON.parse(data);
        if (data[1]){
        document.getElementById('show_older').style.display = "block"
        } else{
        document.getElementById('show_older').style.display = "none"
        }
        if (data[2]){
        document.getElementById('show_later').style.display = "block"
        } else{
        document.getElementById('show_later').style.display = "none"
        }

        if (data[0].length > 0){
        list_div = document.createElement('div')
        for( message of data[0] ){

            var you = ""
            var color = 'grey'
            var weight = "normal"
            var point_display = 'none'
            if (message.is_user_sender){
            you = trans_1
            }
            if (!message.is_seen){
            color =  'var(--green)'
            weight = 'bold'
            point_display = 'block'
            }

            
            let div = document.createElement('div');
            div.style = `border-bottom: var(--transparent-dark) 1px solid;position: relative`
            div.innerHTML = 
            `            
            <div style='border-radius: 50%; background-color: var(--green); width:6px; height:6px; position:absolute; right:5px; top:5px; display:${point_display}'></div>

            <ul class="list-unstyled chat-list mt-0 mb-0">
                <a style="color:unset; background-color: var(--white);" href="/messages/${message.reciever_id}/">
                <li class="clearfix" style="background-color:inherit">
                    <div class="messages_profile_pic_div" style="display: inline;">
                    <img src="${message.image_url}" alt="avatar" class="messages_profile_pic">
                    </div>
                    <div class="about" style="max-width:calc(100% - 45px);">
                    <div class="name" style="font-weight:${weight};">${message.name}</div>
                    <div class="status" style="line-break: anywhere; color:${color}; font-weight:${weight};text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">${you} ${message.text} </div>
                    </div>
                </li>
                </a>
            </ul>
            `
            list_div.append(div)
        }
        plist_3.innerHTML = ''
        plist_3.innerHTML = list_div.innerHTML
        }
        
        else{
        plist_3.innerHTML = `<h4 style="text-align: center; padding: 10px 0; margin: 0;">${ trans_2 }</h4>`;
        }
                
    }
    
    });

};




$('document').ready(function(){
    load_messages();
    setInterval(function(){
        if (page == 1) {
            load_messages()
        }
        }, 2000)
        

    if(window.innerWidth >= 768){
        load_messages_list(); 
    }
    setInterval( function(){
        if(window.innerWidth >= 768){
            if (messages_page == 1){
                load_messages_list(); 
            }
            }
        }, 5000)
    
  })