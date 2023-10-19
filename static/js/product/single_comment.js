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
    $.ajax({
        url: window.location.href + "-ajax",
        success:function(data){
            comment = JSON.parse(data)
            if ( user_id == comment['comment_owner_id'] || comment['product_owner_id'] == user_id ){
                popUp = 
                `
                    <button style="display: inline-block; width: auto;position: absolute; right: 12px;top:3px" type="button" onclick="toggle_div('${comment['id']}')">
                    <img src="https://img.icons8.com/ios-glyphs/26/737373/more.png"/>
                    </button>
                    <div class="collapse hide" id="collapse_div_${comment['id']}" style="position: absolute;right: 11px;top: 26px; width:150px; border: 1px solid var(--transparent-dark); border-radius: 5px;">
                        <div class="text-center p-2">
                            <button onclick="delete_this_comment('${comment["id"]}', this)">${ trans_1 }</button>
                        </div>
                    </div>
                `
            }
            else{
                popUp = ''
            }
          
            comment_container.innerHTML =
            ` 
                <div class="m-auto" style="max-width: 800px;" id="comment_${ comment['id']}">
                    <img src="/static/images/icons/go%20down.png" style="cursor: pointer; transform: rotate(90deg); display:block; margin-bottom:12px" width="40" alt="" id="go-back">
                    <div class="p-2" style="position:relative; border-radius: 3px; border: solid 1px var(--transparent-dark); background-color:var(--white)">
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
                        <p class="check comment-space">${comment['text']}</p>
                    </div>
                </div>
            `  

            document.getElementById('go-back').addEventListener('click', function(){
                window.location.href = window.location.href.replace('comment-' + comment['id'],'');
            })
        }
        })
       

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
        window.location.href = window.location.href.replace('comment-' + comment['id'],'');
      } 
      
