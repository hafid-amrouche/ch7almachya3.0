
function toggle_div(id){
    div = document.getElementById('collapse_div_' + id);
    if ( div.className == "collapse hide"){
      var collection = document.getElementsByClassName("collapse show");
      for (let i = 0; i < collection.length; i++) {
        collection[i].setAttribute("class", "collapse hide")
      }
      div.setAttribute("class", "collapse show")
    }
    else if ( div.className == "collapse show"){
      div.setAttribute("class", "collapse hide")
    }
  }

  var divs = document.getElementsByClassName( 'check' );
  for ( var index = 0; index < divs.length; index++ ) {
    divs[index].style = "text-align: start; unicode-bidi: plaintext;"
  };


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
  function load_comments(){
    if (index > 0){
      loading_svg.style.display = 'block'
    }
    $.ajax({
      url: link_1,
      data:{
        product_id:product_id,
        index: index
      },
      success:function(data){
        
        data = JSON.parse(data)
        thereIsMore = data[1]
        data = data[0]
        var popUp =""
        comment = {}
        for (comment of data ){
          if ( user_id == comment['comment_owner_id'] || product_owner_id == user_id ){
            popUp = 
          `
            <button style="display: inline-block; width: auto;position: absolute; right: 12px;top:3px" type="button" onclick="toggle_div('${comment['id']}')">
              <img src="https://img.icons8.com/ios-glyphs/26/737373/more.png"/>
            </button>
            <div class="collapse hide" id="collapse_div_${comment["id"]}" style="position: absolute;right: 11px;top: 26px; width:150px; border: 1px solid var(--transparent-dark); border-radius: 5px;">
                  <div class="text-center p-2">
                    <button onclick="delete_this_comment('${comment["id"]}', this)">${ trans_1 }</button>
                  </div>
            </div>
          `
          }
          else{
            popUp = ''
          }
          
          comments_container.innerHTML = comments_container.innerHTML +
          ` 
            <div class="mr-2 card mb-4 col-10 col-sm-7 col-md-5 col-lg-4 col-xl-3" style="flex-shrink: 0;" id="comment_${ comment['id']}">
              <span style="position: absolute; top: -90px;" id="span_${ comment['id']}"></span>
              <div class="py-2">
                  <div class="d-flex justify-content-between mb-2">
                      <div class="d-flex flex-row align-items-center">
                          <a href="/user${comment['comment_owner_id']}" style="color: unset;display: contents;" class="commenter-a">
                            <div class="base_profile_pic_div" style="border-radius: 0;">
                              <img src="${[comment['image']]}" alt="avatar" width="30" height="30" class="base_profile_pic" />
                            </div>
                          </a>
                          <div>
                              <p class="small ml-2 mb-0 ms-2">${comment['comment_owner_name']}</p>
                              <p class="small ml-2 mb-0 ms-2">${comment['created_date']}</p>
                          </div>
                          ${popUp}
                      </div>
                  </div>
                  <p class="check comment-space" onclick="window.location.href='comment-${ comment['id']}'">${comment['text']}</p>
              </div>
            </div>
          `
        }
        if (data.length > 0) {
            index = comment['id']
        }
        
        if (thereIsMore){
          load_more_comments.style.display = 'block'
        }
        else{
          load_more_comments.style.display = 'none'
        }
        loading_svg.style.display = 'none'
        load_suggestions()
    }
    })
  }

  function delete_this_comment(id, element){
    $.ajax({
      type: 'GET',
      url: '/delete-comment/',
      data:{
        comment_id : id
      },
      success: function(data){
        element.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.remove();
      }
    });
  } 
  
  $('document').ready(
   function(){
    $.ajax({
      url: link_2,
      data:{
        product_id : product_id
      },
      success: function(data){
        data = JSON.parse(data)
        product_owner_link.setAttribute('href', '/user' + product_owner_id)
        profile_pic.setAttribute('src', data['pp'])
        full_name.innerHTML = data['full_name']
        creation_date.innerHTML = data['time']
        if( authentication == 'True'){
          if (data['saved']){
            document.getElementById('save-item-icon').setAttribute('src', link_9)
            document.getElementById('save-item-icon').setAttribute('saved', "true")
          }else{
            document.getElementById('save-item-icon').setAttribute('src', link_8)
            document.getElementById('save-item-icon').setAttribute('saved', "false")
          }
        }
        document.getElementById('total-images-number').innerHTML = data['images'].length 
        for (let i = 1 ; i <= data['images'].length ; i++){
          if (i == 1){
            document.getElementById('slideshow-container').innerHTML = document.getElementById('slideshow-container').innerHTML +
            `
            <div class="mySlides fade2" style="display: flex;">
                <img src='${ data['images'][i-1] }' style="max-width:100%; max-height:100%; margin:auto; display:block">
              </div>
            `
        }else{
          document.getElementById('slideshow-container').innerHTML = document.getElementById('slideshow-container').innerHTML +
          `
          <div class="mySlides fade2" style="display: none;">
              <img src='${ data['images'][i-1] }' style="max-width:100%; max-height:100%; margin:auto;"">
            </div>
          `
        }
      }

        like_count.innerHTML = data['likes_count']
        dislike_count.innerHTML = data['dislikes_count']
        if(data['liked']){
          like_image.setAttribute('src', '/static/images/icons/like.png');
        }
        if(data['disliked']){
          dislike_image.setAttribute('src', '/static/images/icons/dislike.png');
        }
        
      
        
        
        brand_box.innerHTML=data['brand']
        model_box.innerHTML=data['model']
        year_box.innerHTML=data['year']
        color_box.innerHTML=data['color']
        document_box.innerHTML = data['document']
        if (data['engine']){
          engine_box.innerHTML = data['engine']
        }
        else{
          engine_box.innerHTML = trans_3
          engine_box.style.color = 'grey'
        }
        if(data['used']){
          condition_box.innerHTML = trans_4
        }
        else{
          condition_box.innerHTML = trans_5
        }
        if(data['price']){
          price_box.innerHTML = data['price'] + " Mi"
          price_box.style.color = '#00b517'
        }
        else{
          price_box.innerHTML = trans_3
          price_box.style.color = 'grey'
        }
        if(data['offered_price']){
          offered_price_box.innerHTML = data['offered_price'] + " Mi"
          offered_price_box.style.color = 'red'
        }
        else{
          offered_price_box.innerHTML = trans_6
          offered_price_box.style.color = 'grey'
        }

        if(data['exchange']){
          exchange_box.innerHTML = trans_7
          exchange_box.style.color = '#00b517'
        }
        else{
          exchange_box.innerHTML = trans_8
          exchange_box.style.color = 'grey'
        }

        distance_box.innerHTML = data['distance'] + " KM"
        fuel_box.innerHTML = data['fuel']
        gear_box_box.innerHTML = data['gear_box']

        if(data['all_option']){
          all_options_box.innerHTML = trans_7
          all_options_box.style.color = '#00b517'
        }
        else{
          all_options_box.innerHTML = trans_8
          all_options_box.style.color = 'grey'
        }

        state_box.innerHTML = data['state']
        city_box.innerHTML = data['city']
        var j = 0
        for ( number of data['phone_number']){
          if (number){
            phone_box.innerHTML = phone_box.innerHTML + `<button class="btn btn-success m-2" onclick='window.location.href="tel:${ number }"'><img src="https://img.icons8.com/fluency-systems-regular/50/ffffff/phone-disconnected.png" style="width:24px"; />  ${ number }</button>`
          }else{
            j = j + 1
          }
        }
        
        if ( j === 3){
          document.getElementById('phone-number_container').style.display = 'none'
        }
        
        if(data['options'].length){
          options_container.innerHTML = 
          `
            <div class="text-center m-2 p-2">
              <strong>${ trans_9 }</strong>
            </div>
            <div id='options_list' style="display: flex; justify-content:center; flex-wrap: wrap"> </div> 
          `
          var button;
          for(option of data['options']){
            button = document.createElement('button')
            button.innerHTML = option
            button.className = "btn btn-success p-1 m-1"
            button.style.borderRadius = '10px'
            document.getElementById('options_list').prepend(button)         
            
          }
        }else{
          options_container.className = ""
        }

        if(data['description']){
          description_container.innerHTML =
          `
          <h4 style="color:#00b517;" class='text-fluid'>${ trans_10 }</h4>
          <div class="p-2">
            <p class="check">
              ${data['description']}
            </p>
          </div>
          `

        }else{
          description_container.innerHTML =
          `
          <div class="text-center"><span>${ trans_11 }</span></div>
          `
        }
          
        
        load_comments()
      }
    })
    //
    
   }
   )
  
  if (authentication == "True"){
    $('#like_image').on('click', function(e){
        $.ajax({
          type: 'POST',
          url: link_3,
          data:{
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
          },
        });
        if ( dislike_image.getAttribute('src') == '/static/images/icons/dislike.png' ) {
            dislike_image.setAttribute('src', '/static/images/icons/empty%20dislike.png'),
            dislike_count.innerHTML =  Number(dislike_count.innerHTML) - 1;
        }
        if ( like_image.getAttribute('src') == '/static/images/icons/empty%20like.png'){
          like_image.setAttribute('src', '/static/images/icons/like.png');
          like_count.innerHTML =  Number(like_count.innerHTML) + 1
        }
        else{
          like_image.setAttribute('src', '/static/images/icons/empty%20like.png');
          like_count.innerHTML =  Number(like_count.innerHTML) - 1
        }
    })
    $('#dislike_image').on('click', function(e){
      e.preventDefault();
      $.ajax({
        type: 'POST',
        url: link_4,
        data:{
          csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
        },
      });
      if ( like_image.getAttribute('src') == '/static/images/icons/like.png' ) {
        like_image.setAttribute('src', '/static/images/icons/empty%20like.png'),
        like_count.innerHTML =  Number(like_count.innerHTML) - 1;
      }
      if ( dislike_image.getAttribute('src') == '/static/images/icons/empty%20dislike.png'){
        dislike_image.setAttribute('src', '/static/images/icons/dislike.png');
        dislike_count.innerHTML =  Number(dislike_count.innerHTML) + 1
      }
      else{
        dislike_image.setAttribute('src', '/static/images/icons/empty%20dislike.png');
        dislike_count.innerHTML =  Number(dislike_count.innerHTML) - 1
      }
    })
    
    $(document).on('submit', "#comment-form", function(e){
      comment_button.setAttribute('disabled', "")
      document.getElementById('comment-input').setAttribute('disabled', "")
      e.preventDefault();
      $.ajax({
        type: 'POST',
        url: "comment/",
        data:{
          csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
          comment : $('#comment-input').val(),
        },
        success: function(comment_id){
          comment_id = JSON.parse(comment_id)
          popUp = 
          `
            <button style="display: inline-block; width: auto;position: absolute; right: 12px;top:3px" type="button" onclick="toggle_div('${comment_id}')">
              <img src="https://img.icons8.com/ios-glyphs/26/737373/more.png"/>
            </button>
            <div class="collapse hide" id="collapse_div_${comment_id}" style="position: absolute;right: 11px;top: 26px; width:150px; border: 1px solid var(--transparent-dark); border-radius: 5px;">
                  <div class="text-center p-2">
                    <button onclick="delete_this_comment('${comment_id}', this)">${ trans_1 }</button>
                  </div>
            </div>
          `
          comments_container.innerHTML = 
          ` 
            <div class="mr-2 card mb-4 col-10 col-sm-7 col-md-5 col-lg-4 col-xl-3" style="flex-shrink: 0;" id="comment_${ comment_id}">
                <span style="position: absolute; top: -90px;" id="span_${ comment_id}"></span>
                <div class="py-2">
                    <div class="d-flex justify-content-between mb-2">
                        <div class="d-flex flex-row align-items-center">
                            <a href="/user${ user_id }" style="color: unset;display: contents;" class="commenter-a">
                              <div class="base_profile_pic_div" style="border-radius: 0;">
                                <img src="${ link_5 }" alt="avatar" width="30" height="30" class="base_profile_pic" />
                              </div>
                            </a>
                            <div>
                                <p class="small ml-2 mb-0 ms-2">${ user_full_name }</p>
                                <p class="small ml-2 mb-0 ms-2">${ trans_12 }</p>
                            </div>
                            ${popUp}
                        </div>
                    </div>
                    <p class="check comment-space"  onclick="window.location.href='comment-${ comment_id }'">${ document.getElementById('comment-input').value }</p>
                </div>
            </div>
          ` + comments_container.innerHTML
          comment_button.removeAttribute('disabled')
          document.getElementById('comment-input').removeAttribute('disabled')
          document.getElementById('comment-input').value = ""
        }
        
      });
      
      
    })
    
    
  }
  

  
  let slideIndex = 1;
  document.getElementById('current-image-number').innerHTML = slideIndex
  showSlides(slideIndex);
  
  function plusSlides(n) {
    showSlides(slideIndex += n);
    document.getElementById('current-image-number').innerHTML = slideIndex
  }
  
  function currentSlide(n) {
    showSlides(slideIndex = n);
  }
  
  function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {slideIndex = 1}    
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
    }
   
    try{ 
      slides[slideIndex-1].style.display = "flex";  
    }

    catch{

    }
  }
  
if( authentication == 'True'){
  document.getElementById('save-item').addEventListener('click', ()=>{
    var icon = document.getElementById('save-item-icon')
    if (icon.getAttribute('saved') === "true"){
      icon.setAttribute('saved', 'false')
      icon.setAttribute('src', link_8)
      $.ajax({
        url : link_6,
      })
    }else{
      icon.setAttribute('saved', 'true')
      icon.setAttribute('src', link_9)
      $.ajax({
        url : link_7,
      })
    }
  })
  
}
function load_suggestions(){
  $.ajax({
    url : '/simular-products/',
    data : {
      keyword : text_1,
      product_id : product_id,
    },
    success: (data)=>{
      document.getElementById('loading-suggestions').style.display = 'none'
      createProducts(data)
    }
  })
}

function createProducts(data){
  data = JSON.parse(data)  
  data = data[0]
  var searchContainer = document.getElementById('suggesions-continer')
  var products_count = data.length
  if ( products_count ) {
      if (LC != 'ar'){                        
              var div  = document.createElement('div')
              for(product of data){
                      try {
                          product = product[0]
                          var exchangeHTML = ""
                          if (product['exchange']){
                              exchangeHTML = 
                              `
                                  <span style="font-size:0.8rem; color:#fff; padding: 5px; border-radius: 0.45rem 0 5px 0; background-color: var(--green); position: absolute; z-index: 1;">
                                      <img src="${ s_link_3 }" alt="" width="30px">
                                  </span>
                              `
                          }
                          
                          if (product['price'] ){
                              var product_price = `${ s_trans_1 } <span style="color:var(--green)">${ product['price'] } Mi </span>`
                          }
                          else if (product['given_price'] ){
                              var product_price =`${ s_trans_2 } <span style="color:var(--red)">${product['given_price']} Mi </span>`
                          }
                          else{
                              var product_price = `<span style="color:var(--red)">${ s_trans_3 }</span>`
                          }
      
                          var all_options_display = 'none'
                          if (product['is_all_options']){
                              all_options_display = "block"
                          }
      
                          var store_display = 'none'
                          if (!product['used']){
                              store_display = 'block'
                          }
      
                          var engine_display = 'none'
                          if (product['engine']){
                              engine_display = 'block'
                          }
                          let category = product['other_category'] || product['category_en']
      
                          div.innerHTML = div.innerHTML + 
                          `
                              <div class="col-6 col-md-4 col-lg-3 col-xl-2 p-1 post" style="flex-shrink: 0; position: relative">
                                  ${ exchangeHTML }
                                  <a href="/product/${ product['user'] }/${ product['slug'] }-${product['id']}/" class='product-link'>
                                      <center style="background: url('${ product['image'] }'); position: relative;" class="mb-2 class_image">
                                          <span class='product-year'>
                                          ${ product['year'] }
                                          </span>
                                      </center>
                                      <h6 class="mb-1 mx-1 cut-text">
                                          ${ category.toUpperCase() } - ${ product['name'] }
                                      </h6>
                                      <div class="product-price ml-1 mr-1 cut-text">
                                          ${ product_price }
                                      
                                      </div>
                                      <div style="display: flex; flex-wrap: wrap; font-size: small; height: 67px;" class="cut-text">
                                          <button class="btn btn-danger style-3" style="display:${ all_options_display };">${ s_trans_4 }</button>
                                          <button class="btn btn-success style-3" >${ product['destance'] } Km</button>
                                          <button class="btn btn-success style-3" >${ product['fuel_name'] }</button>
                                          <button class="btn btn-success style-3">${ product['gear_box_name'] }</button>
                                          <button class="btn btn-danger style-3" style="display:${ store_display };">${ s_trans_5 }</button>                
                                          <button class="btn btn-success style-3" style="display:${ engine_display };">${ product['engine'] }</button>                
                                      </div>
                                      <div class="pl-1 cut-text" style="font-size: 0.8rem;">
                                      <img src="https://img.icons8.com/material-rounded/30/28a745/marker.png" width="15" />
                                      <span>${ product['state_name'].toUpperCase() }, ${ product['city'] }</span>
                                      </div>
      
                                      <p class="mx-2" style="font-size: 0.9rem; ">
                                      <img src="https://img.icons8.com/material-outlined/24/28a745/time-machine.png" width="15" />
                                          ${ product['created_date'] }
                                      </p>
                                      <div class="product-price text-right mr-2" style="margin-top: -7px;"> <span style="">${ product['views'] }</span> <img src="${ s_link_4 }" width="15" alt=""> &nbsp; <span style="">${ product['likes_count'] }</span> <img style="padding-bottom: 2px;" src="${ s_link_5 }" width="15" alt=""> </div>
                                  </a>
                              </div>
                          `
                      }
                      catch{

                      }
              }
      }
      else{               
          var div  = document.createElement('div')
          for(product of data){
              try {
                  product = product[0]
                  var exchangeHTML = ""
                  if (product['exchange']){
                      exchangeHTML = 
                      `
                          <span style="font-size:0.8rem; color:#fff; padding: 5px; border-radius: 0.45rem 0 5px 0; background-color: var(--green); position: absolute; z-index: 1;">
                              <img src="${ s_link_3 }" alt="" width="30px">
                          </span>
                      `
                  }
                  
                  if (product['price'] ){
                      var product_price = `<span style="color:var(--green)">مليون ${ product['price'] }</span>`
                      
                  }
                  else if (product.given_price ){
                      var product_price =`عطاولو : <span style="color:var(--red)">مليون ${product['given_price']} </span>`
                  }
                  else{
                      var product_price = `<span style="color:var(--red)">${ s_trans_3 }</span>`
                  }

                  var all_options_display = 'none'
                  if (product['is_all_options']){
                      all_options_display = "block"
                  }

                  var store_display = 'none'
                  if (!product['used']){
                      store_display = 'block'
                  }

                  var engine_display = 'none'
                  if (product['engine']){
                      engine_display = 'block'
                  }
                  let category = product['other_category'] || product['category_ar']
                  div.innerHTML = div.innerHTML + 
                  `
                      <div class="col-6 col-md-4 col-lg-3 p-1 post" style="flex-shrink: 0; position: relative">
                          ${ exchangeHTML }
                          <a href="/product/${ product['user'] }/${ product['slug'] }-${product['id']}/" class='product-link'>
                              <center style="background: url('${ product['image'] }'); position: relative;" class="mb-2 class_image">
                                  <span style=" padding: 3px 5px 3px 20px; position: absolute; bottom: 0; right:0; border-radius: 30px 0 0 0; color: var(--white); background-color: var(--green); font-size: 0.9rem; z-index: 1;" >
                                  ${ product['year'] }
                                  </span>
                              </center>
                              <h6 class="mb-0 mx-1 cut-text text-right" style="height: 20px;">
                                  ${ category.toUpperCase() } - ${ product['name'] }
                              </h6>
                              <div class="product-price ml-1 mr-1 cut-text text-right">
                                  ${ product_price }
                              
                              </div>
                              <div style="display: flex; flex-wrap: wrap; font-size: small; height: 67px;" class="cut-text">
                                  <button class="btn btn-danger style-3" style="display:${ all_options_display }">${ s_trans_4 }</button>
                                  <button class="btn btn-success style-3">${ product['destance'] } كم </button>
                                  <button class="btn btn-success style-3" >${ product['fuel_name'] }</button>
                                  <button class="btn btn-success style-3">${ product['gear_box_name'] }</button>
                                  <button class="btn btn-danger style-3" style="display:${ store_display }">${ s_trans_5 }</button>                
                                  <button class="btn btn-success style-3" style="display:${ engine_display }">${ product['engine'] }</button>                
                              </div>
                              <div class="pl-1 cut-text" style="font-size: 0.8rem;">
                              <img src="https://img.icons8.com/material-rounded/30/28a745/marker.png" width="15" />
                              <span>${ product['state_name'].toUpperCase() }, ${ product['city'] }</span>
                              </div>

                              <p class="mx-2" style="font-size: 0.9rem; ">
                              <img src="https://img.icons8.com/material-outlined/24/28a745/time-machine.png" width="15" />
                                  ${ product['created_date'] }
                              </p>
                              <div class="product-price text-right mr-2" style="margin-top: -7px;"> <span style="">${ product['views'] }</span> <img src="${ s_link_4 }" width="15" alt=""> &nbsp; <span style="">${ product['likes_count'] }</span> <img style="padding-bottom: 2px;" src="${ s_link_5 }" width="15" alt=""> </div>
                          </a>
                      </div>
                  `
              
              }
                  catch{
                      console.log('error')
                  }
          }
  
          
      }
      searchContainer.innerHTML = ''
      searchContainer.innerHTML = div.innerHTML
      
  }
  else {
      searchContainer.innerHTML =
      `
      <div class="p-4 col-12" style="min-height: calc(100vh - 329px) !important; display: flex; justify-content: center; align-items: center;">
          <h4 class="text-center">
                  ${ s_trans_6 }
                  :(
          </h4>
      </div>
      `
  }
  
}

