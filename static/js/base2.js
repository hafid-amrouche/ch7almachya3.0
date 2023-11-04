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
            }
            
        }
    });
}
const activateSW = ()=>{
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/firebase-messaging-sw.js')
            .then((registration) => {
            console.log('Service Worker registered with scope:', registration.scope);
            if (getOrUpdateToken){
                getToken(registration)
            }
           
            })
            
            .catch((error) => {
            console.error('Service Worker registration failed:', error);
            });
    }
}




const updateTokenList =(token)=>{
    $.ajax({
        url : '/update-notifications-token-list',
        data : {
            token : token
        },
        success: (data)=>{
            data = JSON.parse(data)
        }
    })
}


var getTokenTries = 0
const getTokenGetToken =(messaging)=>{
    if (getTokenTries > 100) {return}
    getTokenTries += 1
    
    messaging.usePublicVapidKey("BGM30SVq4D5Dh6nLQC3OW1MmMxIgZOu92a0FOeQHNqgq7URJl0gvUkX-JqzJKNJu6n5Cob_d0Hhsx9mnd7Ly-NM");
    // Subscribe to the registration token
    messaging.getToken({ vapidKey: "BGM30SVq4D5Dh6nLQC3OW1MmMxIgZOu92a0FOeQHNqgq7URJl0gvUkX-JqzJKNJu6n5Cob_d0Hhsx9mnd7Ly-NM" }).then((currentToken) => {
        console.log("Current token:", currentToken);
        updateTokenList(currentToken)
        // Send this token to your server for later use when sending notifications.
    }).catch((err) => {
        console.log("An error occurred while getting the token:", err);
        getTokenGetToken(messaging)
    });
    // Listen for messages
    messaging.onMessage((payload) => {
        console.log("Message received:", payload);
        // Create and display a notification
        const notificationTitle = payload.notification.title;
        const notificationOptions = {
            body: payload.notification.body,
            icon: payload.notification.icon,
            tag : payload.data['type']
        };

        const notif = new Notification(notificationTitle + '-BASE', notificationOptions)
        notif.onclick = (event)=>{
            notif.close()
            window.open(payload.data['link'], '_blank')
            
        }
    });
}

const getToken = (registration)=>{
   
    console.log(getTokenTries)
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
    messaging.useServiceWorker(registration);
    //
    getTokenGetToken(messaging)
}

$('document').ready(function(){
    load_unseen()
})

if ('Notification' in window) {
    // Request permission to show notifications

    if (Notification.permission !== 'granted') {
        Notification.requestPermission().then((permission) => {
            // If the user accepts, let's create a notification
            if (permission === "granted") {
               console.log('Permission granted')
                activateSW()
            }
            else{
                console.log('Permission not granted!!!')
            }
          });;
    }else{
        activateSW()
        console.log('Permission already granted')
    }
    
} 





window.addEventListener('message', function(event) {

    // Ensure the message is coming from the service worker
    if (event.source && event.source instanceof ServiceWorker) {
        console.log('NMCount')
        if (event.data.type === 'NMCount'){
            // Handle the received data
            var NMCount = event.data.NMCount;
            if (NMCount [0] != 0){
            
                document.getElementById('notificationsCountHtml').className = 'btn btn-success rounded-circle'
                document.getElementById('notificationsCountHtml').innerHTML = data[0]
                
            }else{
                document.getElementById('notificationsCountHtml').innerHTML = ""
                document.getElementById('notificationsCountHtml').className = ''
            }
            if (NMCount [1] != 0){
                document.getElementById('messagesCountHtml').className = 'btn btn-success rounded-circle'
                document.getElementById('messagesCountHtml').innerHTML  = data[1]
                
            }else{
                document.getElementById('messagesCountHtml').innerHTML  = ""
                document.getElementById('messagesCountHtml').className = ''
            }
            
            var count = NMCount [0] + data[1]
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
        }
      
    }
});


