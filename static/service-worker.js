// var CACHE_NAME = "my-site-cache-v1";
// var filesToCache = [
//     '/static/js/bootstrap/bootstrap.bundle.min.js',
//     '/static/js/dashboard/create_item.js',
//     '/static/js/dashboard/edit_item.js',
//     '/static/js/message/messages_box.js',
//     '/static/js/message/messages_list.js',
//     '/static/js/product/product.js',
//     '/static/js/product/single_comment.js',
//     '/static/js/settings/profile.js',
//     '/static/js/user/profile.js',
//     '/static/js/base.js',
//     '/static/js/base2.js',
//     '/static/js/home.js',
//     '/static/js/jquery-2.0.0.min.js',
//     '/static/js/notifications.js',
//     '/static/js/register.js',
//     '/static/js/script.js',
//     '/static/js/search.js',
//     '/static/js/category.js',
//     '/static/css/bootstrap/bootstrap.min.css',
//     '/static/css/dashboard/create_item.css',
//     '/static/css/dashboard/your_items.css',
//     '/static/css/message/messages_box.css',
//     '/static/css/message/messages_list.css',
//     '/static/css/product/product.css',
//     '/static/css/settings/profile.css',
//     '/static/css/user/profile.css',
//     '/static/css/base.css',
//     '/static/css/home.css',
//     '/static/css/mine.css',
//     '/static/css/notifications.css',
//     '/static/css/search.css'
// ]

// self.addEventListener('install', function(e){
//     e.waitUntil(
//         caches.open(CACHE_NAME).then(
//             function(cache){
//                 return cache.addAll(filesToCache)
//             }
//         )
//     )
// })

//////////////////////////////


addEventListener("message", (event) => {
    console.log(`Message received: ${event.data}`);
  });
