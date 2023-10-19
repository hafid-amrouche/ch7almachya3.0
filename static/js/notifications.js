
   
    $('document').ready(function(){
        notifications_page = 1;
        show_older.addEventListener('click', function(){
          notifications_page = notifications_page + 1
          load_notifications_list()
          }
        )
        show_later.addEventListener('click', function(){
          notifications_page = notifications_page - 1
          load_notifications_list()
          }
        )
        function load_notifications_list(){
            $.ajax({
              type: 'GET',
              data : {
                notifications_page : notifications_page,
              },
              url: link_1,
              success: function(data){
                data = JSON.parse(data);
                if (data[2]){
                  document.getElementById('show_older').style.display = "block"
                } else{
                  document.getElementById('show_older').style.display = "none"
                }
                if (data[3]){
                  document.getElementById('show_later').style.display = "block"
                } else{
                  document.getElementById('show_later').style.display = "none"
                }
                count = data[1]
                
                //
                if (data[0].length > 0){
                  let div = document.createElement('div');
                  div.innerHTML = ''
                  for( notification of data[0] ){
                        weight = "normal"
                        point_display = 'none'
                        if (!notification.is_seen){
                            weight = 'bold'
                            point_display = 'block'
                        }
                        div.innerHTML = div.innerHTML + 
                        `       
                        <form action="${notification['url']}" style="background-color:var(--white); margin-bottom:2px; position: relative;" onclick="this.submit()">  
                            <div style='border-radius: 50%; background-color: var(--dark); width:6px; height:6px; position:absolute; right:5px; top:5px; display:${point_display}'></div>
                            ${ text }  
                            <input type="hidden" name="notification_id" value="${notification.id}">
                            <div class="d-flex justify-content-between">
                            <div class="d-flex flex-row align-items-center p-2">
                                <div class="notifications_profile_pic_div">
                                <img style="align-self: baseline;" src="${notification.image_url}" alt="avatar" class="notifications_profile_pic">
                                </div>
                                <div>
                                <p class="small ml-2 mb-0 ms-2" style="word-break: break-all; font-weight: ${ weight };"><span style="color:var(--dark)"> ${notification.text}</span></p>
                                <p class="small ml-2 mb-0 ms-2" style=' font-weight: ${ weight }; color:gray'>${ notification.time }</p>
                                </div>
                            </div>
                            </div>
                        </form>
                        `
                  }
                  notifications_div.innerHTML = div.innerHTML
                }
                else if (count == 0 ) {
                  notifications_div.innerHTML = `<h4 style="text-align: center; padding: 10px 0; margin: 0;">${ trans }</h4>`;
                }
                          
              }
              
            });
  
        };
        
        setInterval(function(){
          if(notifications_page == 1){
            load_notifications_list()
          }
          
        }, 1000)
        load_notifications_list(); 
      })
    