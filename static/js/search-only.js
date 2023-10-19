people.addEventListener('click', ()=>{
    people_block.style.display = 'block'
    companies_block.style.display = 'none'
    people.classList = 'btn btn-success  m-2'
    cars.classList = 'btn btn-outline-success  m-2'
    companies.classList = 'btn btn-outline-success  m-2'
    people_clicked ++
    cars_container.style.display = 'none'
    companies_container.style.display = 'none'
    people_container.style.display = 'block'
    if (people_clicked == 1){
        get_people()
    }

})
cars.addEventListener('click', ()=>{
    companies_block.style.display = 'none'
    people_block.style.display = 'none'
    cars_container.style.display = 'block'
    people.classList = 'btn btn-outline-success m-2'
    companies.classList = 'btn btn-outline-success m-2'
    cars.classList = 'btn btn-success m-2'
    
})
companies.addEventListener('click', ()=>{
    companies_block.style.display = 'block'
    people_block.style.display = 'none'
    companies.classList = 'btn btn-success  m-2'
    cars.classList = 'btn btn-outline-success  m-2'
    people.classList = 'btn btn-outline-success  m-2'
    companies_clicked ++
    cars_container.style.display = 'none'
    people_container.style.display = 'none'
    companies_container.style.display = 'block'
    if (companies_clicked == 1){
        get_companies()
    }

})

var people_clicked = 0
var companies_clicked = 0
var ids_people = []
var ids_companies = []
function get_people(){
    document.getElementById('loading-animations-people').style.display = 'block'
    show_more.style.display = 'none'
    $.ajax({
            url : '/get-people/',
            data : {
                ids : ids_people,
                keyword :keyword,
            },
            success : (data)=>{
                data = JSON.parse(data)
                document.getElementById('loading-animations-people').style.display = 'none'
                for(person of data[0]){
                    people_container.innerHTML = people_container.innerHTML + 
                    `
                        <div onclick='window.location.href="/user${ person['id'] }"' class="col-12 col-sm-9 col-md-6 px-0" style="background-color:var(--white); margin: 1px auto;">
                            <div class="d-flex flex-row align-items-center py-2 pl-2 pr-0" style='width:100%'>
                                <div class="notifications_profile_pic_div">
                                    <img style="align-self: baseline;" src="/${person['profile__picture_150']}" alt="avatar" class="notifications_profile_pic">
                                </div>
                                <div style='flex-grow:1'>
                                    <p class="small pl-2 mb-0 ps-2 col-12" style="word-break: break-all; display:flex ;align-items: center"><span style="color:var(--dark)"> ${ person['first_name'] } ${ person['last_name'] }</span><span style='color:var(--green); margin: auto 1px auto auto''>${ person['scoore'] }</span><img src='/static/images/icons/star.png' width="10" height="10"></p>
                                    <p class="small ml-2 mb-0 ms-2" style="word-break: break-all;"><span style="color:var(--dark)"> @${ person['username'] }</span></p>
                                </div>
                            </div>
                        </div>
                    `
                    ids_people = ids_people.concat([person['id']])
                }
                if (data[1]){
                    show_more.style.display = 'block'
                }
                if ( people_clicked == 1 && ids_people.length === 0 ){
                    
                    people_block.innerHTML = people_block.innerHTML +

                    `
                    <div class="p-4 col-12" style="min-height: calc(100vh - 329px) !important; display: flex; justify-content: center; align-items: center;">
                        <h4 class="text-center">
                            ${ transSO2 }
                            :(
                        </h4>
                    </div>
                    `
                    if ( products_count === 0 && ids_people.length === 0 ){
                        companies.click()
                    }
                    
                    
                }
            }

        })
}

function get_companies(){
    document.getElementById('loading-animations-companies').style.display = 'block'
    show_more_companies.style.display = 'none'
    $.ajax({
            url : '/get-companies/',
            data : {
                ids : ids_companies,
                keyword :keyword,
            },
            success : (data)=>{
                data = JSON.parse(data)
                document.getElementById('loading-animations-companies').style.display = 'none'
                for(person of data[0]){
                    companies_container.innerHTML = companies_container.innerHTML + 
                    `
                        <div onclick='window.location.href="/user${ person['id'] }"' class="col-12 col-sm-9 col-md-6 px-0" style="background-color:var(--white); margin: 1px auto;">
                            <div class="d-flex flex-row align-items-center py-2 pl-2 pr-0" style='width:100%'>
                                <div class="notifications_profile_pic_div">
                                    <img style="align-self: baseline;" src="/${person['profile__picture_150']}" alt="avatar" class="notifications_profile_pic">
                                </div>
                                <div style='flex-grow:1'>
                                    <p class="small pl-2 mb-0 ps-2 col-12" style="word-break: break-all; display:flex ;align-items: center"><span style="color:var(--dark)"> ${ person['first_name'] } ${ person['last_name'] }</span><span style='color:var(--green); margin: auto 1px auto auto''>${ person['scoore'] }</span><img src='/static/images/icons/star.png' width="10" height="10"></p>
                                    <p class="small ml-2 mb-0 ms-2" style="word-break: break-all;"><span style="color:var(--dark)"> @${ person['username'] }</span></p>
                                </div>
                            </div>
                        </div>
                    `
                    ids_companies = ids_companies.concat([person['id']])
                }
                if (data[1]){
                    show_more.style.display = 'block'
                }
                if ( companies_clicked == 1 && ids_companies.length === 0 ){
                    
                    companies_block.innerHTML = companies_block.innerHTML +

                    `
                    <div class="p-4 col-12" style="min-height: calc(100vh - 329px) !important; display: flex; justify-content: center; align-items: center;">
                        <h4 class="text-center">
                            ${ transSO1 }
                            :(
                        </h4>
                    </div>
                    `
                    if ( products_count === 0 && ids_people.length === 0 && ids_companies.length === 0){
                        cars.click()
                    }
                    
                }
            }

        })
}

show_more.addEventListener('click', get_people)
show_more_companies.addEventListener('click', get_companies)