// // Connect to WebSocket server
// var socket = io('http://localhost:5000');  // Ensure this is your correct WebSocket URL

// // Listen for new event notifications
// socket.on('new_event_notification', function(event) {
//     console.log("New Event Received:", event);

//     var notificationList = document.getElementById('notificationList');
//     var notificationBadge = document.getElementById('notificationBadge');
//     var emptyMessage = document.getElementById('emptyMessage');

//     // Hide the "No messages" text when there's a new notification
//     emptyMessage.style.display = "none";

//     // Create new notification item
//     var newNotification = document.createElement('li');
//     newNotification.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
//     newNotification.innerHTML = `
//         <div>
//             <strong>${event.title}</strong> - ${event.type} on ${event.event_date}
//         </div>
//         <i class="bi bi-trash fs-5 text-danger" onclick="deleteNotification(event, this)"></i>
//     `;

//     // Add the new notification at the top of the list
//     notificationList.prepend(newNotification);

//     // Update the notification badge count
//     let currentCount = parseInt(notificationBadge.textContent) || 0;
//     console.log("Current Badge Count: " + currentCount);
//     notificationBadge.textContent = currentCount + 1;
//     notificationBadge.style.display = "inline"; // Show the notification badge
// });

// // Function to delete notification
// function deleteNotification(event, element) {
//     var notificationItem = element.closest('.list-group-item');
//     notificationItem.remove();

//     // Update notification count
//     var notificationBadge = document.getElementById('notificationBadge');
//     let currentCount = parseInt(notificationBadge.textContent) || 0;
//     notificationBadge.textContent = currentCount - 1;

//     // If there are no notifications left, show the "No messages" message
//     var notificationList = document.getElementById('notificationList');
//     if (notificationList.children.length === 0) {
//         document.getElementById('emptyMessage').style.display = "block";
//     }
// }
