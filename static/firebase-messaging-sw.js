importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

const firebaseConfig = {   
    apiKey: "AIzaSyCvQPhgNrO3VqmOLTNG-K3IIdu_n00q9u4", 
    authDomain: "ch7al-machya-web-fcm.firebaseapp.com",   
    projectId: "ch7al-machya-web-fcm",   
    storageBucket: "ch7al-machya-web-fcm.appspot.com",   
    messagingSenderId: "920203073524",   
    appId: "1:920203073524:web:f863eb5ca537c90ea38ba1",   
    measurementId: "G-QBKVL6V01W"
};

firebase.initializeApp(firebaseConfig);


const showNotification = (payload)=>{
    self.registration.showNotification(payload.notification.title, {
        body: payload.notification.body,
        icon: payload.notification.icon,
        data : payload.data,
        tag : payload.data.type
    });
}

self.addEventListener('push', (event) => {
    const payload = event.data.json();
    if (payload.data.FCM_type === 'Notification'){
        showNotification(payload)
        updateNMCount(payload)
    }
    
    self.registration
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    let link = event.notification.data.link
    event.waitUntil(clients.matchAll({
        type: "window"
    }).then(function(clientList) {return clients.openWindow(link);}));
});


self.addEventListener('activate', function(event) {
    event.waitUntil(
      self.clients.claim() // Activate the service worker immediately.
    );
});

self.addEventListener('message', function(event) {
    // Data to be sent to the web page's JavaScript
    var dataToSend = { key1: 'value1', key2: 'value2' };
  
    // Use postMessage to send the data to the web page
    event.source.postMessage(dataToSend);
  });

const updateNMCount = (payload)=>{
    let NMCount = JSON.parse(payload.data.NMCount)
    console.log(self.clients)
    self.clients.matchAll().then(clients => {
        clients.forEach(client => {
            client.postMessage(()=>{
                return { NMCount: NMCount, type : 'NMCount' }
            });
        });
    });
                
}

console.log(ServiceWorkerClients.matchAll({includeUncontrolled: true, type: 'window'}))