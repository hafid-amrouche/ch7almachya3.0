$('document').ready(function(){
    function load_unseen(){
        $.ajax({
            url: '/NM-count',
            success: function(data){
                data = JSON.parse(data);
                if (data){
                    if (data[0] != 0){
                        
                        document.getElementById('notificationsCountHtml').className = 'btn btn-success rounded-circle'
                        document.getElementById('notificationsCountHtml').innerHTML = data[0]
                        
                    }else{
                        document.getElementById('notificationsCountHtml').innerHTML = ""
                        document.getElementById('notificationsCountHtml').className = ''
                    }
                    if (data[1] != 0){
                        document.getElementById('messagesCountHtml').className = 'btn btn-success rounded-circle'
                        document.getElementById('messagesCountHtml').innerHTML  = data[1]
                        
                    }else{
                        document.getElementById('messagesCountHtml').innerHTML  = ""
                        document.getElementById('messagesCountHtml').className = ''
                    }
                    

                    var count = Number(data[0]) + Number(data[1])
                    if (count > 99){
                        count = '+99'
                    }
                    if( count ){
                        all_counts.style.display='block'
                        all_counts.innerHTML = count
                        all_counts_2.style.display='block'
                        all_counts_2.innerHTML = count
                    }
                    else{
                        all_counts_2.style.display='none'
                        all_counts.style.display='none'
                    }
                }else{
                    window.location.href = '/log-in'
                }
                
            }
        });
    }
    setInterval(load_unseen, 2000)
    load_unseen()

})




if ('Notification' in window) {
	// Request permission to show notifications
	if (Notification.permission !== 'granted') {
	    Notification.requestPermission();
	}
	
} else {
}

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/static/service-worker.js')
        .then(registration => {
        })
        .catch(error => {
        });
    });
}

function showNotification(title, body, icon, url) {
    const notificationOptions = {
    title: title,
    body: body,
    icon: icon,
    tag : title,
    };
    const notification = new Notification(notificationOptions.title, notificationOptions);  
    notification.onclick = () => {
        window.location.href = url
    }
}

function load_browser_notifications(){
    if (Notification.permission === 'granted'){
       fetch('/browser-notifications').then(response => {
        // Parsing the response data as JSON
        return response.json();
        }).then(data => {
            for ( notification of data ){
                title = notification.title
                body = notification.text
                icon = notification.image_url
                url = notification.url
                showNotification(title, body, icon, url)
            }	
                        
        }).catch(error => {
        // Handle any errors that occurred during the fetch request
        }); 
    }else{
        Notification.requestPermission();
    }
    

}

setInterval(()=>{
    try{
        load_browser_notifications()
    }
    catch{
        }
}, 4000)