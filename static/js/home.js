
var container = document.getElementById('products-container')
var i = 0
$('document').ready(function(){
  $.ajax({
    type: 'GET',
    url: home_ajax_link,
    success: function(data){
      document.getElementById('loading-animations').style.display = 'none'
      data = JSON.parse(data);
      if (LC != 'ar'){
        function loop(){
          row = data[i]
          let div = document.createElement('div');
          div.className = 'pt-3 ml-auto mr-auto'
          div.innerHTML =
          `
            <div class="row">
              <div class="col-12">
                <div class="d-flex align-items-center mb-1">
                      <span>
                        <img src="${row[3]}" alt="" width="30">
                      </span>
                    <h6 class="mx-2 mb-0" onclick="window.location.href='${row[1]}'">${row[0]}</h6>
                </div>
              </div>
            </div>  
            <div>
              <div id="${row[0]}_products" >
              </div>
            </div>
                ` ;
          container.appendChild(div)
          var products_div = document.getElementById( row[0] + '_products')
          
          for(product of row[2]){
            try{
              
            var exchange_display = 'none'
            if (product['exchange'] ){
              exchange_display = 'block'
            }
            if (product['price'] ){
              var product_price = `${ trans_1 } <span style="color:var(--green)">${ product['price'] } Mi </span>`
            }
            else if (product.given_price ){
              var product_price =`${trans_2} <span style="color:var(--red)">${product['given_price']} Mi </span>`
            }
            else{
              var product_price = `<span style="color:var(--red)">${ trans_3 }</span>`
            }
            
          
            let category = product['other_category'] || product['category_name']
            

            products_div.innerHTML = products_div.innerHTML + 
            `
              <div class="mr-2 product-cart">
               
                  <span style="display:${ exchange_display };" class='exchange-icon'>
                    <img src="${ src_1 }" alt="" width="30px">
                  </span>
                <a href="/product/${ product['user'] }/${ product['slug'] }-${product['id']}/" class="product-link">
                  <center class="class_image" style="background: url('${product['image']}');">
                    <span class="product-year">
                      ${product['year']}
                    </span>
                  </center>
                    <h6 class="product-title cut-text">
                        ${category.toUpperCase()} - ${product['name']}
                    </h6>
                    <div class="product-price cut-text">
                      ${product_price}
                    
                    </div>
                  <div class="ml-1 cut-text" style="font-size: 0.8rem;">
                    <img src="https://img.icons8.com/material-rounded/30/28A745/marker.png" width="15" />
                    <span class="">${product['state__name_' + LC ].toUpperCase()}, ${product['city']}</span>
                  </div>
                  <div class="product-price text-right"> <span>${product['views']}</span> <img src="${src_2}" width="15" alt=""> &nbsp; <span>${product['likes_count']}</span> <img style="padding-bottom: 2px;" src="${src_3}" width="15"> </div>
                </a>
              </div>  
            `
          
            }
            catch{

            }
          }
          
          if ( i >= data.length - 1){
            
            clearInterval(interval);
          }
          i=i+1
        }
        interval = setInterval(loop, 200)
        loop()
     } else{
        function loop(){
          row = data[i]
          let div = document.createElement('div');
          div.className = 'pt-3 ml-auto mr-auto'
          div.innerHTML =
          `
            <div class="row">
              <div class="col-12">
                <div class="d-flex align-items-center mb-1">
                      <span class='ml-auto'>
                        <img src="${row[3]}" alt="" width="30">
                      </span>
                    <h6 class="mx-2 mb-0" onclick="window.location.href='${row[1]}'">${row[0]}</h6>
                </div>
              </div>
            </div>  
            <div>
              <div id="${row[0]}_products">
              </div>
            </div>
                ` ;
          container.appendChild(div)
          var products_div = document.getElementById( row[0] + '_products')
          
          for(product of row[2]){
            try{
              
              var exchange_display = 'none'
              if (product['exchange'] ){
                exchange_display = 'block'
              }

              if (product['price'] ){
                var product_price = `<span style="color:var(--green)">مليون ${ product['price'] }</span>`
                
              }
              else if (product.given_price ){
                var product_price =`عطاولو : <span style="color:var(--red)">مليون ${product['given_price']} </span>`
              }
              else{
                var product_price = `<span style="color:var(--red)">${ trans_3 }</span>`
              }
              
              let category = product['other_category'] || product['category_name']

              products_div.innerHTML = products_div.innerHTML + 
              `
                <div class="mr-2" style="flex-shrink: 0; position: relative; width: 180px;">
                
                    <span style="display:${ exchange_display };"  class='exchange-icon'>
                      <img src="${ src_1 }" alt="" width="30px">
                    </span>
                  <a href="/ar/product/${ product['user'] }/${ product['slug'] }-${product['id']}/" class="product-link">
                    <center style="background: url('${product['image']}'); position: relative;" class="mb-2 class_image">
                      <span class='product-year'>
                        ${product['year']}
                      </span>
                    </center>
                      <h6 class="product-title cut-text">
                          ${category} - ${product['name']}
                      </h6>
                      <div class="product-price cut-text text-right">
                        ${product_price}
                      </div>
                    <div class="pr-1 cut-text text-right" style="font-size: 0.8rem;">
                      <img src="https://img.icons8.com/material-rounded/30/28A745/marker.png" width="15" />
                      <span class="">${product['state__name_' + LC]}, ${product['city']}</span>
                      
                    </div>
                    <div class="product-price text-right cut-text"> <span>${product['views']}</span> <img src="${ src_2 }" width="15" alt=""> &nbsp; <span>${product['likes_count']}</span> <img style="padding-bottom: 2px;" src="${ src_3 }" width="15" alt=""> </div>
                  </a>
                </div>  
              `
          
            }
            catch{

            }
          }
          
          if ( i >= data.length - 1){
            
            clearInterval(interval);
          }
          i = i+1
        }
        interval = setInterval(loop, 200)
        loop()
    }
      
    }
  });
})




