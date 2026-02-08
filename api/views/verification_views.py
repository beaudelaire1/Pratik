"""
Verification API Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from apps.verification.models import VerificationDocument
from api.serializers.verification_serializers import (
    VerificationDocumentSerializer,
    SubmitVerificationSerializer,
    VerifyDocumentSerializer
)
from core.services.verification_service import VerificationService


class SubmitVerificationView(APIView):
    """
    Submit verification documents.
    Any authenticated user can submit documents.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Submit verification documents."""
        serializer = SubmitVerificationSerializer(data=request.data)
        if serializer.is_valid():
            documents_data = serializer.validated_data['documents']
            
            # Use service to submit documents
            service = VerificationService()
            documents = service.submit_verification_documents(
                user=request.user,
                documents_data=documents_data
            )
            
            result_serializer = VerificationDocumentSerializer(documents, many=True)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyDocumentView(APIView):
    """
    Verify or reject a document.
    Only admins can verify documents.
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request, document_id):
        """Verify or reject a document."""
        try:
            document = VerificationDocument.objects.get(id=document_id)
        except VerificationDocument.DoesNotExist:
            return Response(
                {"error": "Document not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = VerifyDocumentSerializer(data=request.data)
        if serializer.is_valid():
            # Use service to verify document
            service = VerificationService()
            verified_document = service.verify_document(
                document=document,
                admin_user=request.user,
                approved=serializer.validated_data['approved'],
                rejection_reason=serializer.validated_data.get('rejection_reason', '')
            )
            
            result_serializer = VerificationDocumentSerializer(verified_document)
            return Response(result_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingVerificationsView(generics.ListAPIView):
    """
    List all pending verification documents.
    Only admins can view pending verifications.
    """
    serializer_class = VerificationDocumentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['document_type', 'user__user_type']
    ordering_fields = ['submitted_at']
    ordering = ['submitted_at']
    
    def get_queryset(self):
        """Get all pending documents."""
        service = VerificationService()
        return service.get_pending_verifications()


class UserVerificationStatusView(APIView):
    """
    Get verification status for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user verification status."""
        service = VerificationService()
        is_verified = service.check_full_verification(request.user)
        
        # Get user's documents
        documents = VerificationDocument.objects.filter(user=request.user)
        serializer = VerificationDocumentSerializer(documents, many=True)
        
        return Response({
            'is_verified': is_verified,
            'documents': serializer.data
        })
