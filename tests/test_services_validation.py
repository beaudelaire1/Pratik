"""
Tests for HousingOffer and CarpoolingOffer validation
"""
import pytest
from django.core.exceptions import ValidationError
from apps.services.models import HousingOffer, CarpoolingOffer
from apps.users.models import CustomUser
from decimal import Decimal
from django.utils import timezone


@pytest.mark.django_db
class TestHousingOfferValidation:
    """Test HousingOffer model validation"""
    
    def test_housing_offer_price_cap_enforced(self):
        """Test that housing offers cannot exceed 300€ rent"""
        user = CustomUser.objects.create_user(
            username='landlord1',
            email='landlord@test.com',
            password='testpass123',
            user_type='LANDLORD',
            is_verified=True
        )
        
        # Create offer with price > 300€
        offer = HousingOffer(
            title='Expensive Studio',
            description='Test description',
            housing_type='studio',
            location='Cayenne',
            price=Decimal('350.00'),
            contact_email='test@test.com',
            owner=user
        )
        
        # Should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            offer.clean()
        
        assert 'price' in exc_info.value.message_dict
        assert '300€' in str(exc_info.value.message_dict['price'])
    
    def test_housing_offer_price_cap_valid(self):
        """Test that housing offers at or below 300€ are valid"""
        user = CustomUser.objects.create_user(
            username='landlord2',
            email='landlord2@test.com',
            password='testpass123',
            user_type='LANDLORD',
            is_verified=True
        )
        
        # Create offer with price = 300€
        offer = HousingOffer(
            title='Affordable Studio',
            description='Test description',
            housing_type='studio',
            location='Cayenne',
            price=Decimal('300.00'),
            contact_email='test@test.com',
            owner=user
        )
        
        # Should not raise ValidationError
        offer.clean()
        offer.save()
        assert offer.price == Decimal('300.00')
    
    def test_housing_offer_requires_verified_landlord(self):
        """Test that only verified landlords can publish housing offers"""
        user = CustomUser.objects.create_user(
            username='unverified_landlord',
            email='unverified@test.com',
            password='testpass123',
            user_type='LANDLORD',
            is_verified=False
        )
        
        offer = HousingOffer(
            title='Studio',
            description='Test description',
            housing_type='studio',
            location='Cayenne',
            price=Decimal('250.00'),
            contact_email='test@test.com',
            owner=user
        )
        
        # Should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            offer.clean()
        
        assert 'owner' in exc_info.value.message_dict
        assert 'vérifiés' in str(exc_info.value.message_dict['owner'])


@pytest.mark.django_db
class TestCarpoolingOfferValidation:
    """Test CarpoolingOffer model validation"""
    
    def test_carpooling_requires_verified_driver(self):
        """Test that only verified drivers can publish carpooling offers"""
        user = CustomUser.objects.create_user(
            username='unverified_driver',
            email='driver@test.com',
            password='testpass123',
            user_type='DRIVER',
            is_verified=False
        )
        
        offer = CarpoolingOffer(
            driver=user,
            departure='Cayenne',
            destination='Kourou',
            date_time=timezone.now(),
            seats_available=3,
            price=Decimal('15.00')
        )
        
        # Should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            offer.clean()
        
        assert 'driver' in exc_info.value.message_dict
        assert 'vérifiés' in str(exc_info.value.message_dict['driver'])
    
    def test_carpooling_verified_driver_valid(self):
        """Test that verified drivers can publish carpooling offers"""
        user = CustomUser.objects.create_user(
            username='verified_driver',
            email='verified_driver@test.com',
            password='testpass123',
            user_type='DRIVER',
            is_verified=True
        )
        
        offer = CarpoolingOffer(
            driver=user,
            departure='Cayenne',
            destination='Kourou',
            date_time=timezone.now(),
            seats_available=3,
            price=Decimal('15.00')
        )
        
        # Should not raise ValidationError
        offer.clean()
        offer.save()
        assert offer.driver == user
