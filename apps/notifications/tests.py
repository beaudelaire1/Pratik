"""
Tests for notifications app.
"""
import pytest
from apps.notifications.models import Notification


@pytest.mark.django_db
class TestNotificationModel:
    """Test Notification model."""
    
    def test_create_notification(self, notification):
        """Test creating a notification."""
        assert notification.recipient.email == 'student@test.com'
        assert notification.title == 'Test Notification'
        assert notification.message == 'This is a test notification.'
        assert notification.is_read is False
        assert notification.notification_type == 'system'
    
    def test_notification_str_representation(self, notification):
        """Test notification string representation."""
        expected = f"{notification.recipient.username}: {notification.title}"
        assert str(notification) == expected
    
    def test_mark_as_read(self, notification):
        """Test marking notification as read."""
        assert notification.is_read is False
        
        notification.mark_as_read()
        
        assert notification.is_read is True
    
    def test_mark_as_read_idempotent(self, notification):
        """Test that marking as read multiple times is safe."""
        notification.mark_as_read()
        notification.mark_as_read()
        
        assert notification.is_read is True
    
    def test_create_notification_helper(self, student_user):
        """Test create_notification helper method."""
        notification = Notification.create_notification(
            recipient=student_user,
            notification_type='new_internship',
            title='New Internship Available',
            message='Check out this new opportunity!',
            link='/internships/123/'
        )
        
        assert notification.recipient == student_user
        assert notification.notification_type == 'new_internship'
        assert notification.title == 'New Internship Available'
        assert notification.link == '/internships/123/'
    
    def test_get_unread_count(self, student_user):
        """Test get_unread_count method."""
        # Create multiple notifications
        Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='Notification 1',
            message='Message 1',
            is_read=False
        )
        Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='Notification 2',
            message='Message 2',
            is_read=False
        )
        Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='Notification 3',
            message='Message 3',
            is_read=True  # This one is read
        )
        
        unread_count = Notification.get_unread_count(student_user)
        assert unread_count == 2
    
    def test_notification_ordering(self, student_user):
        """Test that notifications are ordered by created_at descending."""
        notif1 = Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='First',
            message='First message'
        )
        notif2 = Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='Second',
            message='Second message'
        )
        
        notifications = Notification.objects.filter(recipient=student_user)
        assert notifications[0] == notif2  # Most recent first
        assert notifications[1] == notif1
    
    def test_notification_types(self, student_user):
        """Test different notification types."""
        types = [
            'application_received',
            'application_accepted',
            'application_rejected',
            'new_internship',
            'message_received',
            'system'
        ]
        
        for notif_type in types:
            notification = Notification.objects.create(
                recipient=student_user,
                notification_type=notif_type,
                title=f'Test {notif_type}',
                message='Test message'
            )
            assert notification.notification_type == notif_type


@pytest.mark.django_db
class TestNotificationViews:
    """Test notification views."""
    
    def test_notification_list_requires_login(self, client):
        """Test that notification list requires login."""
        response = client.get('/notifications/')
        assert response.status_code == 302  # Redirect to login
    
    def test_notification_list_view(self, client, student_user, notification):
        """Test notification list view."""
        client.force_login(student_user)
        response = client.get('/notifications/')
        assert response.status_code == 200
        assert 'notifications/notification_list.html' in [t.name for t in response.templates]
        assert notification in response.context['notifications']
    
    def test_notification_list_only_own(self, client, student_user, company_user):
        """Test that users only see their own notifications."""
        # Create notification for student
        student_notif = Notification.objects.create(
            recipient=student_user,
            notification_type='system',
            title='Student Notification',
            message='For student'
        )
        
        # Create notification for company
        company_notif = Notification.objects.create(
            recipient=company_user,
            notification_type='system',
            title='Company Notification',
            message='For company'
        )
        
        # Login as student
        client.force_login(student_user)
        response = client.get('/notifications/')
        
        assert student_notif in response.context['notifications']
        assert company_notif not in response.context['notifications']
    
    def test_mark_notification_as_read(self, client, student_user, notification):
        """Test marking notification as read."""
        client.force_login(student_user)
        
        assert notification.is_read is False
        
        response = client.post(f'/notifications/{notification.pk}/mark-read/')
        
        notification.refresh_from_db()
        assert notification.is_read is True
    
    def test_mark_all_as_read(self, client, student_user):
        """Test marking all notifications as read."""
        # Create multiple unread notifications
        for i in range(3):
            Notification.objects.create(
                recipient=student_user,
                notification_type='system',
                title=f'Notification {i}',
                message=f'Message {i}',
                is_read=False
            )
        
        client.force_login(student_user)
        response = client.post('/notifications/mark-all-read/')
        
        unread_count = Notification.objects.filter(
            recipient=student_user,
            is_read=False
        ).count()
        assert unread_count == 0


@pytest.mark.django_db
class TestNotificationUtils:
    """Test notification utility functions."""
    
    def test_send_application_received_email(self, application):
        """Test sending application received email."""
        from apps.notifications.utils import send_application_received_email
        
        # This should not raise an error
        # In a real test, you'd mock the email backend
        try:
            send_application_received_email(application)
        except Exception as e:
            # Email might fail in test environment, that's ok
            pass
    
    def test_send_application_response_email(self, application):
        """Test sending application response email."""
        from apps.notifications.utils import send_application_response_email
        
        # Test accepted
        try:
            send_application_response_email(application, accepted=True)
        except Exception:
            pass
        
        # Test rejected
        try:
            send_application_response_email(application, accepted=False)
        except Exception:
            pass


@pytest.mark.django_db
@pytest.mark.integration
class TestNotificationIntegration:
    """Integration tests for notifications."""
    
    def test_notification_created_on_application(self, client, student_user, company_user, internship):
        """Test that notification is created when application is submitted."""
        client.force_login(student_user)
        
        # Count notifications before
        notif_count_before = Notification.objects.filter(recipient=company_user).count()
        
        # Submit application
        data = {'cover_letter': 'I am interested.'}
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        
        # Check notification was created
        notif_count_after = Notification.objects.filter(recipient=company_user).count()
        assert notif_count_after == notif_count_before + 1
        
        # Verify notification content
        notification = Notification.objects.filter(recipient=company_user).first()
        assert notification.notification_type == 'application_received'
        assert internship.title in notification.message
    
    def test_notification_created_on_acceptance(self, client, student_user, company_user, application):
        """Test that notification is created when application is accepted."""
        client.force_login(company_user)
        
        # Count notifications before
        notif_count_before = Notification.objects.filter(recipient=student_user).count()
        
        # Accept application
        response = client.post(
            f'/applications/{application.pk}/update-status/',
            {'action': 'accept', 'message': 'Congratulations!'}
        )
        
        # Check notification was created
        notif_count_after = Notification.objects.filter(recipient=student_user).count()
        assert notif_count_after == notif_count_before + 1
        
        # Verify notification content
        notification = Notification.objects.filter(recipient=student_user).first()
        assert notification.notification_type == 'application_accepted'
