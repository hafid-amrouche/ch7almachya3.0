///////////////////////////////////
//FUNCTIONS
///////////////////////////////////

function load_unseen(){
    $.ajax({
        url: '/NM-count',
        success: function(data){
            let NMCount = JSON.parse(data)
            broadcastChannel.postMessage({ NMCount : NMCount, type : 'NMCountDisplay' });
            NMCountUIUpdater(NMCount)
        }
    });

}

const updateTokenListInServer =(token)=>{
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

const listenToFBMessages =(messaging)=>{
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

/////////////////////////////////////////////
//
/////////////////////////////////////////////

const getTokenGetToken =(messaging)=>{
 

    messaging.getToken().then((currentToken) => {
        console.log("Current token:", currentToken);
        updateTokenListInServer(currentToken) // Send this token to your server for later use when sending notifications.

    }).catch((err) => {
        console.log("An error occurred while getting the token:", err);
        //getTokenGetToken(messaging)
    });
    //////////////////// Listen for messages
    listenToFBMessages(messaging)
}

//////////////////////////////////
//
//////////////////////////////////
const getToken = (registration)=>{
   
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
    messaging.usePublicVapidKey("BGM30SVq4D5Dh6nLQC3OW1MmMxIgZOu92a0FOeQHNqgq7URJl0gvUkX-JqzJKNJu6n5Cob_d0Hhsx9mnd7Ly-NM");
    messaging.useServiceWorker(registration);
    getTokenGetToken(messaging)
}

var NCount = 0
var MCount = 0
var count = 0

const NMCountUIUpdater = (NMCount)=>{
    NMCount[0] >= 0 ? NCount = NMCount[0] : null

    NMCount[1] >= 0 ? MCount = NMCount[1] : null
    
    if (NCount > 0){
        
        document.getElementById('notificationsCountHtml').className = 'btn btn-success rounded-40'
        document.getElementById('notificationsCountHtml').innerHTML = NCount
        
    }else if (NCount === 0){
        document.getElementById('notificationsCountHtml').innerHTML = ""
        document.getElementById('notificationsCountHtml').className = ''
    }
    if (MCount > 0){
        document.getElementById('messagesCountHtml').className = 'btn btn-success rounded-40'
        document.getElementById('messagesCountHtml').innerHTML  = MCount
        
    }else if (MCount === 0){
        document.getElementById('messagesCountHtml').innerHTML  = ""
        document.getElementById('messagesCountHtml').className = ''
    }
    
    count = NCount + MCount
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

const listenToClientsMessages =()=>{
    navigator.serviceWorker.addEventListener("message", ({data}) => {
        if (data.type === 'NMCount'){
            // Handle the received data
            var NMCount = data.NMCount;
            NMCountUIUpdater(NMCount)
        }
    });
}

////////////////////////////////////////
// BROADCASTING SOME VARIABLES UPDATE TO ALL TABS
///////////////////////////////////////
const broadcastChannel = new BroadcastChannel('count_channel');
broadcastChannel.onmessage = (event) => {
    if (event.data.type === 'NMCountDisplay'){
        let NMCount = event.data.NMCount
        NMCountUIUpdater(NMCount) 
    }  
  };


///////////////////////////////////
// LOADING SW FILE TO BROSER
///////////////////////////////////

if ('Notification' in window) {
    // Request permission to show notifications

    if (Notification.permission !== 'granted') {
        Notification.requestPermission().then((permission) => {
            // If the user accepts, let's create a notification
            if (permission === "granted") {
               console.log('Permission granted')
            }
            else{
                console.log('Permission not granted!!!')
            }
          });;
    }else{
        console.log('Permission already granted')
    }
    
} 


////////////////////////////////////
//
///////////////////////////////////
const deleteToken= ()=>{
    if ('serviceWorker' in navigator) {
        if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({deleteToken : true});
          } else {
            console.warn('Service worker is not controlling the page.');
          }
        
    }
}

///////////////////////////////////
// ACTIVATING SERVICE WORKER
//////////////////////////////////
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/firebase-messaging-sw.js', {scope : ''})
        .then((registration) => {
            listenToClientsMessages()
            console.log('Service Worker registered with scope:', registration.scope);
            if (getOrUpdateToken){
                getToken(registration)
            }
       
        })
        .catch((error) => {
        console.error('Service Worker registration failed:', error);
        });
}




//////////////////////////////////
// AFTER HTML LOADING
/////////////////////////////////

$('document').ready(function(){
    load_unseen()
})


/////////////////////////////////////
//
/////////////////////////////////////
document.getElementById('logout-a').onclick = (event)=>{
    event.preventDefault()
    deleteToken()
    //window.location.href = document.getElementById('logout-a').getAttribute('href')
}