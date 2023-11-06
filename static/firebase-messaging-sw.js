///////////////////////////////////
// ON SW ACTIVATION
//////////////////////////////////
self.addEventListener('activate', (event) => {
    event.waitUntil(
        ////////////////
        self.clients.claim()
    );
    
  });

///////////////////////////////////
// FIREBASE INITIATION
//////////////////////////////////
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
const messaging = firebase.messaging();

///////////////////////////////////
// USE FIREBASE MESSAGES
///////////////////////////////////

self.addEventListener('push', (event) => {
    const payload = event.data.json();
    if (payload.data.FCM_type === 'Notification'){
        showNotification(payload)
        updateNMCount(payload)
    }else if (payload.data.FCM_type === 'NMCount'){
        updateNMCount(payload) 
    }
    
    self.registration
});

////////////////////////////////////
// HANDLE NOTIFICATIONS CLICK
///////////////////////////////////

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    let link = event.notification.data.link
    event.waitUntil(clients.matchAll({
        type: "window"
    }).then(function(clientList) {return clients.openWindow(link);}));
});

////////////////////////////////
// LISTEN TO MESSAGE FROM CLIENT
///////////////////////////////

self.addEventListener('message', (event) => {
    if (event.data.deleteToken) {
        console.log('TRYING')
        try {deleteToken(messaging)}
        catch(err) {console.log('TOKEN NOT DELETED :', err)}
    }
  });


/////////////////////////////////
// FUNCTIONS
////////////////////////////////

const showNotification = (payload)=>{
    self.registration.showNotification(payload.notification.title, {
        body: payload.notification.body,
        icon: payload.notification.icon,
        data : payload.data,
        tag : payload.data.type
    });
}

//////////////////////
// BORADCAST A UI UPADTE FOR NMCount
/////////////////////
const updateNMCount = (payload)=>{
    let NMCount = JSON.parse(payload.data.NMCount)
    sendMessage({type : 'NMCount', NMCount : NMCount})
}


const sendMessage = async (msg) =>{
    allClients = await clients.matchAll({includeUncontrolled:true})
    return Promise.all(
        allClients.map(client=>{
            return client.postMessage(msg)
        })
        
    )
}


const deleteToken = (messaging)=>{
    messaging.deleteToken().then(function() {
        console.log('Token deleted successfully');
      }).catch(function(error) {
        if (error.code === 'messaging/token-not-found') {
          // The token doesn't exist, which is expected.
          console.log('Token not found; it may have already been deleted.');
        } else {
          // Handle other errors gracefully.
          console.error('Error deleting token:', error);
        }
      });
}

/////////////////////////////
// CONNECT CURRENT SEESION ID WITH A NEW TOKEN
////////////////////////////
const refreshTokenInServer = (token)=>{

    fetch('/refresh-token', {
        method: 'GET', // You can specify the HTTP method you need (e.g., 'POST', 'GET', etc.)
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Set the content type as needed
        },
        body: `token=${token}`,
    })
    .then((response) => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        // Handle the JSON response data
        console.log(data);
    })
    .catch((error) => {
        console.warn('Fetch request error:', error);
    });

}