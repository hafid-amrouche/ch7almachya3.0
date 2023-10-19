
   
    $('document').ready(function(){
        let plist_3 = document.getElementById('plist_3')
        messages_page = 1;
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
              url: link_1,
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
  
                    you = ""
                    color = 'grey'
                    weight = "normal"
                    point_display = 'none'
                    if (message.is_user_sender){
                      you = trans_1
                    }
                    if (!message.is_seen){
                      color =  '#00b517'
                      weight = 'bold'
                      point_display = 'block'
                    }
                    let div = document.createElement('div');
                    div.style = `position: relative;  margin-bottom: 2px`
                    div.innerHTML = 
                    `            
                    <div style='border-radius: 50%; background-color: var(--dark); width:6px; height:6px; position:absolute; right:5px; top:5px; display:${point_display}'></div>
                      <ul class="list-unstyled chat-list mt-0 mb-0">
                        <a style="color:unset; background-color:var(--white);" href="/messages/${message.reciever_id}/">
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
                }else{
                  plist_3.innerHTML = `<h4 style="text-align: center; padding: 10px 0; margin: 0;">${ trans_2 }</h4>`;
                }
                          
              }
              
            });
  
        };
        
        setInterval(
        function(){
          if (messages_page == 1){
            load_messages_list()
          }
        }  
        , 3000)
        load_messages_list(); 
      })
    