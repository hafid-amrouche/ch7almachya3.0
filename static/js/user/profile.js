var button = document.getElementById('copy-link')
  button.innerHTML = window.location.href;
  function copylink(image) {
    try{
      navigator.clipboard.writeText(window.location.href);
    }catch{

    }

    if ( button.style.visibility == "hidden"){
      button.style.visibility = 'visible';
      image.style.background = "var(--green)";
    } else {
      button.style.visibility = 'hidden';
      image.style.background = "var(--white)";
    }
    
  }

  var index = 0;
  var show_more_var;
  function load_products(){
    $.ajax({
      url: link_1,
      data: {
        index : index
      },
      success: function(data){
        data = JSON.parse(data)
        show_more_var = data[1]
        data = data[0]
        document.getElementById('loading-animations').style.display = 'none'
        if (data.length > 0){
          var price_span
          for (product of data){
                if ( product['price'] ){
                  price_span = `<span style="color: #00b517;">${ product['price'] } Mi</span>`
                }
                    
                else if ( product['given_price'] ){
                  price_span = `<span style="color: red;">${ product['given_price'] } Mi</span>`
                }
                    
                else{
                  price_span = `<span style="color: red;">${ trans_1 }</span>`
                }
                    
      
                products_container.innerHTML = products_container.innerHTML +
                `
                  <div class="col-12 col-lg-6 p-3">
                    <a href="/product/${ owner_id }/${ product['slug'] }-${ product['id'] }/" style="color: unset;">
                        <div class="card p-2">
                            <div class="d-flex align-items-center p-2">
                            <div style='width:70px; margin-right: 10px; background-color: var(--white); text-align:center'> <img src="${ product['main_image'] }" style="max-height: 70px; max-width: 70px"/> </div>
                                <div class="d-flex flex-column" style="flex-grow: 1; padding-right:8px"> 
                                  <span class="text-muted" style="font-size:0.8rem;">${ product['created_date'] }</span>
                                    <strong>${ product['name'] }</strong>
                                    ${ price_span }
                                    <div>${ product['views'] }  <img src="${ link_2 }" width="18" alt=""> &nbsp;&nbsp; <span >${ product['likes_count'] }</span> <img style="padding-bottom: 2px;" src="${ link_3 }" width="18" alt=""></div>
                                </div>
                                
                            </div>
                        </div>
                    </a>
                  </div>
                `
              
          }
        }
        else{
            products_container.innerHTML= 
            `
            <h4 class='my-4 text-center'> ${ trans_2 } </h4>
            ` + products_container.innerHTML
        }
        try{
          index = product['id']
                if (show_more_var){
                  document.getElementById('show_more').style.display = 'block'
                }else{
                  document.getElementById('show_more').style.display = 'none'
                }
                loading_svg.style.display = 'none'
        }catch{}
                
      }
    })
  }
  function followAnimation(form){
    var followers_count = document.getElementById('followers_count')
    $.ajax({
      type: 'POST',
      url: "follow_unfollow/",
      data:{
        csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
      },
    });

    if (form.getAttribute('state') == "2"){
      form.setAttribute('state', '1')
      form.innerHTML=
      `
        <button type="submit" class="btn btn-success btn-md follow">
          <img   src="https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/E0kRRLkJ46S.png?_nc_eui2=AeETistanzcx95psW4bgN8drLW6Wl0-A-i4tbpaXT4D6Lk2-AD5k6SH2jUtQjQ1ktEGVO0ySBXXm9oHb0_e06f11" alt="" height="20" width="20">    
          &nbsp; ${ trans_3 }
        </button>
      `
      followers_count.innerHTML = Number(followers_count.innerHTML) - 1
    }
    else{
      form.setAttribute('state', '2')
      form.innerHTML=
        `
        <button type="submit" class="btn btn-success btn-md follow">
          <img class="x1b0d499 xep6ejk" src="https://static.xx.fbcdn.net/rsrc.php/v3/yF/r/pkvyTf8WAzw.png?_nc_eui2=AeHI9dpTxnmrKVKrlzIABdBAYl0KlTPLtyJiXQqVM8u3IiGVScoYsuYYw3BX2gZo9pTVp9topLoSUvcAwMrFJ4QM" alt="" height="16" width="16">
          &nbsp; ${ trans_4 }
        </button>
        `
        followers_count.innerHTML = Number(followers_count.innerHTML) + 1
    }
  }
  show_more.addEventListener('click', function(){
    loading_svg.style.display = 'block'
    show_more.style.display = 'none'
    load_products()
    
  })
  $('document').ready(function(){
    
    $.ajax({
      url: link_4,
      success: function(data){
        data = JSON.parse(data)
        console.log(data)
        owner_picture.setAttribute('src', data['pp'])
        owner_name.innerHTML = data['owner_name']
        bio.innerHTML = data['bio']
  
        if ( authentication =='True' && owner_id != user_id ) {
          if (data['is_follower']){
            follow_message_report.innerHTML = 
            `
              <form id="follow-form" state="2" method="POST" onclick='followAnimation(this)'> 
                  <button type="button" class="btn btn-success btn-md follow">
                      <img class="x1b0d499 xep6ejk" src="https://static.xx.fbcdn.net/rsrc.php/v3/yF/r/pkvyTf8WAzw.png?_nc_eui2=AeHI9dpTxnmrKVKrlzIABdBAYl0KlTPLtyJiXQqVM8u3IiGVScoYsuYYw3BX2gZo9pTVp9topLoSUvcAwMrFJ4QM" alt="" height="16" width="16">
                      &nbsp; ${ trans_4 }
                  </button>
              </form>
          `
          }
          else{
            follow_message_report.innerHTML = 
            `
              <form id="follow-form" state="1" method="POST" onclick='followAnimation(this)'>     
                <button type="button" class="btn btn-success btn-md follow">
                    <img class="x1b0d499 xep6ejk" src="https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/E0kRRLkJ46S.png?_nc_eui2=AeETistanzcx95psW4bgN8drLW6Wl0-A-i4tbpaXT4D6Lk2-AD5k6SH2jUtQjQ1ktEGVO0ySBXXm9oHb0_e06f11" alt="" height="20" width="20">    
                    &nbsp; ${ trans_3 }
                </button>
              </form>
            `
          }
          
          follow_message_report.innerHTML = follow_message_report.innerHTML +
          `
            <button type="button" class="btn btn-light ml-2" style="border-color: #9e9090;display: flex; align-items: center;" onclick="window.location.href= '/messages/${ data["owner_id"] }'" >
              <img src="https://img.icons8.com/ios-filled/50/40C057/facebook-messenger.png" width="24"/>
            </button>
            <form action="" method="POST">
                ${ token }
                <button type="button" class="btn btn-light ml-2" style="border-color: #9e9090;" onclick="window.location.href = 'report/';" >
                    ${ trans_5 }
                </button>
            </form>
          `
          
        }

      
        followers_count.innerHTML = data['followers_count']
        products_count.innerHTML = data['products_count']
        if ( data['feedback'] != "False"){
          feedback.innerHTML = data['feedback']
        }
        else{
          feedback.innerHTML = trans_6
        }
        scoore.innerHTML = data['scoore']
        rank.innerHTML = data['rank']

        load_products()
      }
    })
  })
