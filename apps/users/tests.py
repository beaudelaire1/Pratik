"""
Tests for users app.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    """Test CustomUser model."""
    
    def test_create_student_user(self, student_user):
        """Test creating a student user."""
        assert student_user.email == 'student@test.com'
        assert student_user.user_type == 'student'
        assert student_user.is_student is True
        assert student_user.is_company is False
        assert student_user.check_password('testpass123')
    
    def test_create_company_user(self, company_user):
        """Test creating a company user."""
        assert company_user.email == 'company@test.com'
        assert company_user.user_type == 'company'
        assert company_user.is_student is False
        assert company_user.is_company is True
        assert company_user.company_name == 'Tech Corp'
    
    def test_create_admin_user(self, admin_user):
        """Test creating an admin user."""
        assert admin_user.is_superuser is True
        assert admin_user.is_staff is True
        assert admin_user.user_type == 'admin'
    
    def test_user_str_representation(self, student_user):
        """Test user string representation."""
        assert str(student_user) == 'student@test.com'
    
    def test_get_display_name_student(self, student_user):
        """Test get_display_name for student."""
        assert student_user.get_display_name() == 'John Doe'
    
    def test_get_display_name_company(self, company_user):
        """Test get_display_name for company."""
        assert company_user.get_display_name() == 'Tech Corp'
    
    def test_get_display_name_no_name(self, db):
        """Test get_display_name when no name is set."""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        assert user.get_display_name() == 'testuser'
    
    def test_get_skills_list(self, student_user):
        """Test get_skills_list method."""
        student_user.skills = 'Python, Django, JavaScript'
        student_user.save()
        skills = student_user.get_skills_list()
        assert len(skills) == 3
        assert 'Python' in skills
        assert 'Django' in skills
        assert 'JavaScript' in skills
    
    def test_get_skills_list_empty(self, student_user):
        """Test get_skills_list when no skills."""
        assert student_user.get_skills_list() == []
    
    def test_get_languages_list(self, student_user):
        """Test get_languages_list method."""
        student_user.languages = 'Français, Anglais, Espagnol'
        student_user.save()
        languages = student_user.get_languages_list()
        assert len(languages) == 3
        assert 'Français' in languages
        assert 'Anglais' in languages
    
    def test_get_languages_list_empty(self, student_user):
        """Test get_languages_list when no languages."""
        assert student_user.get_languages_list() == []
    
    def test_email_unique_constraint(self, db):
        """Test that email must be unique."""
        User.objects.create_user(
            username='user1',
            email='unique@test.com',
            password='testpass123'
        )
        with pytest.raises(Exception):  # IntegrityError
            User.objects.create_user(
                username='user2',
                email='unique@test.com',
                password='testpass123'
            )
    
    def test_user_type_choices(self, db):
        """Test user_type choices."""
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            user_type='student'
        )
        company = User.objects.create_user(
            username='company',
            email='company@example.com',
            password='testpass123',
            user_type='company'
        )
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            user_type='admin'
        )
        
        assert student.user_type == 'student'
        assert company.user_type == 'company'
        assert admin.user_type == 'admin'


@pytest.mark.django_db
class TestUserViews:
    """Test user views."""
    
    def test_signup_view_get(self, client):
        """Test signup view GET request."""
        response = client.get('/auth/signup/')
        assert response.status_code == 200
        assert 'registration/signup.html' in [t.name for t in response.templates]
    
    def test_signup_view_post_valid(self, client, db):
        """Test signup view POST with valid data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'student'
        }
        response = client.post('/auth/signup/', data)
        assert response.status_code == 302  # Redirect after success
        assert User.objects.filter(email='newuser@test.com').exists()
    
    def test_profile_view(self, client, student_user):
        """Test profile view."""
        response = client.get(f'/users/profile/{student_user.pk}/')
        assert response.status_code == 200
        assert 'users/profile.html' in [t.name for t in response.templates]
    
    def test_edit_profile_view_requires_login(self, client):
        """Test edit profile requires login."""
        response = client.get('/users/profile/edit/')
        assert response.status_code == 302  # Redirect to login
    
    def test_edit_profile_view_authenticated(self, client, student_user):
        """Test edit profile when authenticated."""
        client.force_login(student_user)
        response = client.get('/users/profile/edit/')
        assert response.status_code == 200
        assert 'users/edit_profile.html' in [t.name for t in response.templates]
    
    def test_edit_profile_post(self, client, student_user):
        """Test editing profile."""
        client.force_login(student_user)
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'bio': 'Updated bio',
            'phone': '0594123456',
            'location': 'Cayenne',
            'school': 'Test University',
            'field_of_study': 'Engineering'
        }
        response = client.post('/users/profile/edit/', data)
        student_user.refresh_from_db()
        assert student_user.first_name == 'Jane'
        assert student_user.bio == 'Updated bio'


@pytest.mark.django_db
class TestUserForms:
    """Test user forms."""
    
    def test_custom_user_creation_form_valid(self, db):
        """Test CustomUserCreationForm with valid data."""
        from apps.users.forms import CustomUserCreationForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'student'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
    
    def test_custom_user_creation_form_password_mismatch(self, db):
        """Test form with mismatched passwords."""
        from apps.users.forms import CustomUserCreationForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!',
            'user_type': 'student'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors
    
    def test_custom_user_creation_form_duplicate_email(self, db, student_user):
        """Test form with duplicate email."""
        from apps.users.forms import CustomUserCreationForm
        
        form_data = {
            'username': 'newuser',
            'email': 'student@test.com',  # Already exists
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'student'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
