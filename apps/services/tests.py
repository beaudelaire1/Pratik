"""
Tests for services app.
"""
import pytest
from apps.services.models import HousingOffer, CarpoolingOffer, ForumPost, ForumComment


@pytest.mark.django_db
class TestServicesModels:
    """Test services models."""
    
    def test_create_housing_offer(self, student_user):
        """Test creating a housing offer."""
        housing = HousingOffer.objects.create(
            user=student_user,
            title='Chambre à louer',
            description='Belle chambre meublée',
            location='Cayenne',
            price=400,
            available_from='2026-03-01'
        )
        
        assert housing.title == 'Chambre à louer'
        assert housing.price == 400
        assert housing.user == student_user
    
    def test_create_carpooling_offer(self, student_user):
        """Test creating a carpooling offer."""
        carpooling = CarpoolingOffer.objects.create(
            user=student_user,
            departure='Cayenne',
            destination='Kourou',
            date='2026-03-15',
            time='08:00',
            seats_available=3,
            price_per_seat=10
        )
        
        assert carpooling.departure == 'Cayenne'
        assert carpooling.destination == 'Kourou'
        assert carpooling.seats_available == 3
    
    def test_create_forum_post(self, student_user):
        """Test creating a forum post."""
        post = ForumPost.objects.create(
            author=student_user,
            title='Question about internships',
            content='How do I find a good internship?'
        )
        
        assert post.title == 'Question about internships'
        assert post.author == student_user
        assert post.slug is not None
    
    def test_create_forum_comment(self, student_user, company_user):
        """Test creating a forum comment."""
        post = ForumPost.objects.create(
            author=student_user,
            title='Test Post',
            content='Test content'
        )
        
        comment = ForumComment.objects.create(
            post=post,
            author=company_user,
            content='Great question!'
        )
        
        assert comment.post == post
        assert comment.author == company_user
        assert comment in post.comments.all()


@pytest.mark.django_db
class TestServicesViews:
    """Test services views."""
    
    def test_housing_list_view(self, client):
        """Test housing list view."""
        response = client.get('/services/housing/')
        assert response.status_code == 200
        assert 'services/housing_list.html' in [t.name for t in response.templates]
    
    def test_carpooling_list_view(self, client):
        """Test carpooling list view."""
        response = client.get('/services/carpooling/')
        assert response.status_code == 200
        assert 'services/transport_list.html' in [t.name for t in response.templates]
    
    def test_forum_list_view(self, client):
        """Test forum list view."""
        response = client.get('/services/forum/')
        assert response.status_code == 200
        assert 'services/forum_list.html' in [t.name for t in response.templates]
    
    def test_calendar_view(self, client):
        """Test calendar view."""
        response = client.get('/services/calendar/')
        assert response.status_code == 200
        assert 'services/calendar.html' in [t.name for t in response.templates]
