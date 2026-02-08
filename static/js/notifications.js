// Notifications and Messages Badge Management

// Update notification count
function updateNotificationCount() {
    fetch('/notifications/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notification-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count > 99 ? '99+' : data.count;
                    badge.classList.remove('hidden');
                } else {
                    badge.classList.add('hidden');
                }
            }
        })
        .catch(error => console.error('Error fetching notification count:', error));
}

// Update message count
function updateMessageCount() {
    fetch('/messaging/unread-count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('message-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count > 99 ? '99+' : data.count;
                    badge.classList.remove('hidden');
                    badge.classList.add('flex');
                } else {
                    badge.classList.add('hidden');
                    badge.classList.remove('flex');
                }
            }
        })
        .catch(error => console.error('Error fetching message count:', error));
}

// Load recent notifications in dropdown
function loadNotificationsDropdown() {
    fetch('/notifications/?format=json&limit=5')
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById('notif-dropdown');
            if (!dropdown) return;
            
            if (data.notifications && data.notifications.length > 0) {
                dropdown.innerHTML = data.notifications.map(notif => `
                    <div class="p-4 border-b border-gray-700 hover:bg-gray-800 transition ${notif.is_read ? '' : 'bg-blue-900/10'}">
                        <div class="flex items-start gap-3">
                            <span class="text-2xl">${getNotificationIcon(notif.notification_type)}</span>
                            <div class="flex-1 min-w-0">
                                <h4 class="text-white font-semibold text-sm">${notif.title}</h4>
                                <p class="text-gray-400 text-xs mt-1">${notif.message}</p>
                                <span class="text-gray-500 text-xs mt-1 block">${notif.created_at}</span>
                            </div>
                            ${!notif.is_read ? '<span class="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 mt-1"></span>' : ''}
                        </div>
                    </div>
                `).join('');
            } else {
                dropdown.innerHTML = '<div class="p-8 text-center text-gray-500">Aucune notification</div>';
            }
        })
        .catch(error => {
            console.error('Error loading notifications:', error);
            const dropdown = document.getElementById('notif-dropdown');
            if (dropdown) {
                dropdown.innerHTML = '<div class="p-4 text-center text-gray-500">Erreur de chargement</div>';
            }
        });
}

// Get icon for notification type
function getNotificationIcon(type) {
    const icons = {
        'application_received': '📥',
        'application_accepted': '✅',
        'application_rejected': '❌',
        'new_internship': '💼',
        'message_received': '💬',
        'system': '🔔'
    };
    return icons[type] || '🔔';
}

// Mark all notifications as read
function markAllNotificationsRead() {
    fetch('/notifications/mark-all-read/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNotificationCount();
            loadNotificationsDropdown();
        }
    })
    .catch(error => console.error('Error marking notifications as read:', error));
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Update counts immediately
    updateNotificationCount();
    updateMessageCount();
    
    // Update counts every 30 seconds
    setInterval(function() {
        updateNotificationCount();
        updateMessageCount();
    }, 30000);
    
    // Load notifications when dropdown is opened
    const notifButton = document.querySelector('[x-data] button');
    if (notifButton) {
        notifButton.addEventListener('click', function() {
            setTimeout(loadNotificationsDropdown, 100);
        });
    }
});
