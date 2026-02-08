"""
Evolution Tracking API Serializers
"""
from rest_framework import serializers
from apps.tracking.models import StudentEvolutionTracking


class StudentEvolutionTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentEvolutionTracking model.
    """
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    student_name = serializers.SerializerMethodField()
    student_email = serializers.EmailField(source='student.email', read_only=True)
    
    class Meta:
        model = StudentEvolutionTracking
        fields = [
            'id', 'company', 'company_name', 'student', 'student_name',
            'student_email', 'current_level', 'domain', 'status',
            'evolution_history', 'notify_on_level_change',
            'notify_on_status_change', 'notify_on_availability',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'company', 'evolution_history']
    
    def get_student_name(self, obj):
        """Get student full name."""
        return f"{obj.student.first_name} {obj.student.last_name}"


class StartTrackingSerializer(serializers.Serializer):
    """
    Serializer for starting to track a student.
    """
    student_id = serializers.IntegerField()
    current_level = serializers.ChoiceField(
        choices=StudentEvolutionTracking.LEVEL_CHOICES,
        required=False,
        default='BEGINNER'
    )
    domain = serializers.CharField(max_length=100, required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=StudentEvolutionTracking.STATUS_CHOICES,
        required=False,
        default='AVAILABLE'
    )
    
    def validate_student_id(self, value):
        """Validate student exists and is a student."""
        from apps.users.models import CustomUser
        try:
            student = CustomUser.objects.get(id=value)
            if student.user_type != 'STUDENT':
                raise serializers.ValidationError("User must be a student.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Student not found.")
        return value


class UpdateEvolutionSerializer(serializers.Serializer):
    """
    Serializer for updating student evolution.
    """
    current_level = serializers.ChoiceField(
        choices=StudentEvolutionTracking.LEVEL_CHOICES,
        required=False
    )
    domain = serializers.CharField(max_length=100, required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=StudentEvolutionTracking.STATUS_CHOICES,
        required=False
    )
