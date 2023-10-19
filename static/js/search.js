function toggleRightSidebar(){
    sidebar = document.getElementById('rightSidebar');
    if(sidebar.style.transform != 'translate(0%)' ){
        sidebar.style.transition = '0.5s';
        sidebar.style.transform = 'translate(0%)';
        mySidebar.style.transform = 'translate(-100%)';
    }
    else{
        sidebar.style.transform = 'translate(100%)';
    }
}

        
$('[aria-label="Search"]').val(keyword)

var ajax_url = link_1



var page = 1
var loading = document.getElementById('loading-animations')
var products_count = 0

function search(){
    loading.style.display = 'block'
    $.ajax({
        type: 'POST',
        url: ajax_url,
        data:{
            keyword : keyword,
            search_type : text_1,
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            SPID: text_2,
            page: page,
        },
        success: function(data){
            createProducts(data)
            loading.style.display = 'none'
            document.getElementById('filter-bar').style.display = 'block'
        },
    })

}
function load_page(){
    page = this.innerHTML
    document.getElementById('products-container').innerHTML = ''
    loading.style.display ='block'
    pagination.innerHTML=''
    search()
}

function createProducts(data){
    data = JSON.parse(data)
    var pages_count = data[3]
    
    data = data[0]
    var searchContainer = document.getElementById('products-container')
    products_count = data.length
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
                                        <img src="${ link_3 }" alt="" width="30px">
                                    </span>
                                `
                            }
                            
                            if (product['price'] ){
                                var product_price = `${ trans_1 } <span style="color:var(--green)">${ product['price'] } Mi </span>`
                            }
                            else if (product['given_price'] ){
                                var product_price =`${ trans_2 } <span style="color:var(--red)">${product['given_price']} Mi </span>`
                            }
                            else{
                                var product_price = `<span style="color:var(--red)">${ trans_3 }</span>`
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
                                <div class="col-6 col-md-4 col-lg-3 p-1 post" style="flex-shrink: 0; position: relative">
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
                                            <button class="btn btn-danger style-3" style="display:${ all_options_display };">${ trans_4 }</button>
                                            <button class="btn btn-success style-3" >${ product['destance'] } Km</button>
                                            <button class="btn btn-success style-3" >${ product['fuel_name'] }</button>
                                            <button class="btn btn-success style-3">${ product['gear_box_name'] }</button>
                                            <button class="btn btn-danger style-3" style="display:${ store_display };">${ trans_5 }</button>                
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
                                        <div class="product-price text-right mr-2" style="margin-top: -7px;"> <span style="">${ product['views'] }</span> <img src="${ link_4 }" width="15" alt=""> &nbsp; <span style="">${ product['likes_count'] }</span> <img style="padding-bottom: 2px;" src="${ link_5 }" width="15" alt=""> </div>
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
                                <img src="${ link_3 }" alt="" width="30px">
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
                        var product_price = `<span style="color:var(--red)">${ trans_3 }</span>`
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
                                    <button class="btn btn-danger style-3" style="display:${ all_options_display }">${ trans_4 }</button>
                                    <button class="btn btn-success style-3">${ product['destance'] } كم </button>
                                    <button class="btn btn-success style-3" >${ product['fuel_name'] }</button>
                                    <button class="btn btn-success style-3">${ product['gear_box_name'] }</button>
                                    <button class="btn btn-danger style-3" style="display:${ store_display }">${ trans_5 }</button>                
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
                                <div class="product-price text-right mr-2" style="margin-top: -7px;"> <span style="">${ product['views'] }</span> <img src="${ link_4 }" width="15" alt=""> &nbsp; <span style="">${ product['likes_count'] }</span> <img style="padding-bottom: 2px;" src="${ link_5 }" width="15" alt=""> </div>
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
        pagination.innerHTML = ''
        for( var i = 1; i <= pages_count; i++){
            var button = document.createElement('button')
            button.innerHTML = i
            if (page != i){
                button.className = 'btn btn-success m-1'
                button.addEventListener('click', load_page)
            }
            else{
                button.className = 'btn btn-outline-success m-1 disabled'
            }
            
            pagination.appendChild(button)
        }
        
    }
    else {
        people.click()
        pagination.innerHTML = ''
        searchContainer.innerHTML =
        `
        <div class="p-4 col-12" style="min-height: calc(100vh - 329px) !important; display: flex; justify-content: center; align-items: center; flex-direction:column">
            <h4 class="text-center">
                    ${ trans_6 }
            </h4>
            <h4>:(</h4>
        </div>
        `
    }
    
}

$(document).ready(function(){
    search()
});