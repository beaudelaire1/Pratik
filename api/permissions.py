"""
Custom API Permissions for PRATIK Platform
"""
from rest_framework import permissions


class IsCompany(permissions.BasePermission):
    """
    Permission to check if user is a company.
    """
    message = "Only companies can perform this action."

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'COMPANY'
        )


class IsSchool(permissions.BasePermission):
    """
    Permission to check if user is a school.
    """
    message = "Only schools can perform this action."

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'SCHOOL'
        )


class IsVerified(permissions.BasePermission):
    """
    Permission to check if user is verified.
    """
    message = "Only verified users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_verified
        )


class CanPublishListing(permissions.BasePermission):
    """
    Permission to check if user can publish listings (housing/carpooling).
    Requires verification for landlords and drivers.
    """
    message = "You must be verified to publish listings."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Landlords and drivers must be verified
        if request.user.user_type in ['LANDLORD', 'DRIVER']:
            return request.user.is_verified
        
        # Other user types can publish without verification
        return True
