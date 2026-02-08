"""
Verification API Serializers
"""
from rest_framework import serializers
from apps.verification.models import VerificationDocument


class VerificationDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for VerificationDocument model.
    """
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    verified_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VerificationDocument
        fields = [
            'id', 'user', 'user_name', 'user_email', 'document_type',
            'file', 'status', 'rejection_reason', 'expiry_date',
            'submitted_at', 'verified_at', 'verified_by', 'verified_by_name'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'verified_at', 'verified_by',
            'submitted_at'
        ]
    
    def get_user_name(self, obj):
        """Get user full name."""
        if obj.user.user_type == 'COMPANY':
            return obj.user.company_name
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_verified_by_name(self, obj):
        """Get verifier name."""
        if obj.verified_by:
            return f"{obj.verified_by.first_name} {obj.verified_by.last_name}"
        return None


class SubmitVerificationSerializer(serializers.Serializer):
    """
    Serializer for submitting verification documents.
    """
    documents = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of documents with document_type, file, and optional expiry_date"
    )
    
    def validate_documents(self, value):
        """Validate documents list."""
        if not value:
            raise serializers.ValidationError("At least one document is required.")
        
        valid_types = [choice[0] for choice in VerificationDocument.DOCUMENT_TYPE_CHOICES]
        
        for doc in value:
            if 'document_type' not in doc:
                raise serializers.ValidationError("Each document must have a document_type.")
            if doc['document_type'] not in valid_types:
                raise serializers.ValidationError(f"Invalid document_type: {doc['document_type']}")
            if 'file' not in doc:
                raise serializers.ValidationError("Each document must have a file.")
        
        return value


class VerifyDocumentSerializer(serializers.Serializer):
    """
    Serializer for verifying a document.
    """
    approved = serializers.BooleanField()
    rejection_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Required if approved is False"
    )
    
    def validate(self, data):
        """Validate rejection reason is provided if not approved."""
        if not data.get('approved') and not data.get('rejection_reason'):
            raise serializers.ValidationError(
                "Rejection reason is required when rejecting a document."
            )
        return data
