var CACHE_NAME = "my-site-cache-v1";
var filesToCache = [
    '/static/js/bootstrap/bootstrap.bundle.min.js',
    '/static/js/dashboard/create_item.js',
    '/static/js/dashboard/edit_item.js',
    '/static/js/message/messages_box.js',
    '/static/js/message/messages_list.js',
    '/static/js/product/product.js',
    '/static/js/product/single_comment.js',
    '/static/js/settings/profile.js',
    '/static/js/user/profile.js',
    '/static/js/base.js',
    '/static/js/base2.js',
    '/static/js/home.js',
    '/static/js/jquery-2.0.0.min.js',
    '/static/js/notifications.js',
    '/static/js/register.js',
    '/static/js/script.js',
    '/static/js/search.js',
    '/static/js/category.js',
    '/static/css/bootstrap/bootstrap.min.css',
    '/static/css/dashboard/create_item.css',
    '/static/css/dashboard/your_items.css',
    '/static/css/message/messages_box.css',
    '/static/css/message/messages_list.css',
    '/static/css/product/product.css',
    '/static/css/settings/profile.css',
    '/static/css/user/profile.css',
    '/static/css/base.css',
    '/static/css/home.css',
    '/static/css/mine.css',
    '/static/css/notifications.css',
    '/static/css/search.css'
]

self.addEventListener('install', function(e){
    e.waitUntil(
        caches.open(CACHE_NAME).then(
            function(cache){
                return cache.addAll(filesToCache)
            }
        )
    )
})

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(clients.matchAll({
        type: "window"
    }).then(function(clientList) {
        for (var i = 0; i < clientList.length; i++) {
        var client = clientList[i];
        if (client.url == self.registration.scope && 'focus' in client) {
            return client.focus();
        }
        }
        if (clients.openWindow) {
            return clients.openWindow(event.notification.data);
        }
    }));
});

function showNotification(title, body, icon, url) {
    const notificationOptions = {
    title: title,
    body: body,
    icon: icon,
    tag : title,
    data : url
    };
    
    self.registration.showNotification(notificationOptions.title, notificationOptions);
       
}


function load_browser_notifications(){
    if (Notification.permission === 'granted'){
       fetch('/browser-notifications').then(response => {
        return response.json();
        }).then(data => {
            for ( notification of data ){
                try{
                   title = notification.title
                    body = notification.text
                    icon = notification.image_url
                    url = notification.url
                    showNotification(title, body, icon, url) 
                }catch{
    
                }
                
            }	
                        
        }).catch(error => {
        // Handle any errors that occurred during the fetch request
        }); 
    }
}

setInterval(()=>{
    try{
        if (Notification.permission === 'granted'){
            load_browser_notifications()
        }

    }
    catch{
    }
}, 2000)
