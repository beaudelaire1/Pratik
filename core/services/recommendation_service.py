"""
Recommendation Service

Handles business logic for company recommendations of students/interns.
"""

from django.db.models import Count, Avg, Q
from apps.recommendations.models import InternRecommendation


class RecommendationService:
    """Service for managing intern recommendations by companies"""
    
    @staticmethod
    def create_recommendation(company, student, internship, data):
        """
        Create a recommendation for a student by a company.
        
        Args:
            company: CompanyProfile instance
            student: StudentProfile instance
            internship: Internship instance
            data: dict containing recommendation data
                - rating (int): 1-5 stars
                - autonomy (bool): optional
                - teamwork (bool): optional
                - rigor (bool): optional
                - creativity (bool): optional
                - punctuality (bool): optional
                - skills_validated (list): optional
                - comment (str): required
                - recommended_domains (list): optional
        
        Returns:
            InternRecommendation instance
        """
        recommendation = InternRecommendation.objects.create(
            company=company,
            student=student,
            internship=internship,
            rating=data['rating'],
            autonomy=data.get('autonomy', False),
            teamwork=data.get('teamwork', False),
            rigor=data.get('rigor', False),
            creativity=data.get('creativity', False),
            punctuality=data.get('punctuality', False),
            skills_validated=data.get('skills_validated', []),
            comment=data['comment'],
            recommended_domains=data.get('recommended_domains', []),
        )
        
        # Update student profile statistics
        student.total_recommendations = student.recommendations_received.count()
        student.save()
        
        # TODO: Trigger notification to student
        # NotificationService.send_recommendation_notification(student, company)
        
        return recommendation
    
    @staticmethod
    def get_student_recommendations(student):
        """
        Get all public recommendations for a student.
        
        Args:
            student: StudentProfile instance
        
        Returns:
            QuerySet of InternRecommendation instances
        """
        return InternRecommendation.objects.filter(
            student=student,
            is_public=True
        ).select_related('company', 'company__user', 'internship').order_by('-created_at')
    
    @staticmethod
    def get_recommended_students(filters=None):
        """
        Get students with recommendations, with optional filtering and sorting.
        
        Args:
            filters: dict with optional keys:
                - min_rating (float): minimum average rating
                - sector (str): filter by recommended domain/sector
                - min_recommendations (int): minimum number of recommendations
        
        Returns:
            QuerySet of StudentProfile instances with annotations:
                - recommendation_count: number of recommendations
                - avg_rating: average rating across recommendations
        """
        from apps.users.profile_models import StudentProfile
        
        students = StudentProfile.objects.filter(
            recommendations_received__isnull=False
        ).annotate(
            recommendation_count=Count('recommendations_received', distinct=True),
            avg_rating=Avg('recommendations_received__rating')
        ).distinct()
        
        if filters:
            if 'min_rating' in filters and filters['min_rating']:
                students = students.filter(avg_rating__gte=filters['min_rating'])
            
            if 'sector' in filters and filters['sector']:
                students = students.filter(
                    recommendations_received__recommended_domains__contains=[filters['sector']]
                )
            
            if 'min_recommendations' in filters and filters['min_recommendations']:
                students = students.filter(
                    recommendation_count__gte=filters['min_recommendations']
                )
        
        return students.order_by('-recommendation_count', '-avg_rating')
