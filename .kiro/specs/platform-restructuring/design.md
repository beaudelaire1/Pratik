# Architecture Technique PRATIK
## Design et Modèles de Données

---

## 1. MODÈLES DE DONNÉES

### 1.1 Modèle User (Étendu)

```python
class User(AbstractUser):
    """Utilisateur de base avec profil polymorphique"""
    USER_TYPES = [
        ('STUDENT', 'Étudiant'),
        ('COMPANY', 'Entreprise'),
        ('RECRUITER', 'Recruteur'),
        ('SCHOOL', 'École'),
        ('TRAINING_CENTER', 'Centre de Formation'),
        ('LANDLORD', 'Particulier/Propriétaire'),
        ('DRIVER', 'Chauffeur/Taxi'),
        ('PARTNER', 'Partenaire Institutionnel'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)


### 1.2 Modèle CompanyProfile (Enrichi)

```python
class CompanyProfile(models.Model):
    """Profil entreprise avec fonctionnalités partenariat"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    siret = models.CharField(max_length=14, unique=True)
    
    # Informations de base
    sector = models.CharField(max_length=100)  # NOUVEAU
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    website = models.URLField(blank=True)
    
    # Partenariat PRATIK
    is_partner = models.BooleanField(default=False)  # NOUVEAU
    partner_since = models.DateField(null=True, blank=True)  # NOUVEAU
    partner_badge = models.BooleanField(default=False)  # NOUVEAU
    
    # Statistiques
    total_interns_hosted = models.IntegerField(default=0)  # NOUVEAU
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    # Visibilité
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    is_visible_on_partners_page = models.BooleanField(default=True)  # NOUVEAU
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil Entreprise"
        verbose_name_plural = "Profils Entreprises"


### 1.3 Modèle InternRecommendation (NOUVEAU)

```python
class InternRecommendation(models.Model):
    """Recommandation d'un stagiaire par une entreprise"""
    RATING_CHOICES = [(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(1, 6)]
    
    # Relations
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='recommendations_given')
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='recommendations_received')
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, related_name='recommendations')
    
    # Évaluation
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    # Points forts
    autonomy = models.BooleanField(default=False)
    teamwork = models.BooleanField(default=False)
    rigor = models.BooleanField(default=False)
    creativity = models.BooleanField(default=False)
    punctuality = models.BooleanField(default=False)
    
    # Compétences validées
    skills_validated = models.JSONField(default=list)  # Liste de compétences
    
    # Commentaire
    comment = models.TextField()
    
    # Domaines recommandés
    recommended_domains = models.JSONField(default=list)
    
    # Visibilité
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Recommandation"
        verbose_name_plural = "Recommandations"
        unique_together = ['company', 'student', 'internship']
        ordering = ['-created_at']


### 1.4 Modèle StudentEvolutionTracking (NOUVEAU)

```python
class StudentEvolutionTracking(models.Model):
    """Suivi de l'évolution d'un étudiant par une entreprise"""
    STATUS_CHOICES = [
        ('STUDYING', 'En études'),
        ('EMPLOYED', 'En emploi'),
        ('AVAILABLE', 'Disponible'),
        ('SEEKING', 'En recherche'),
    ]
    
    # Relations
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='tracked_students')
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='tracking_companies')
    
    # Informations suivies
    current_level = models.CharField(max_length=100)  # Ex: "M1 Informatique"
    domain = models.CharField(max_length=200)  # Ex: "Développement Web, IA"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Historique
    evolution_history = models.JSONField(default=list)  # Historique des changements
    
    # Notifications
    notify_on_level_change = models.BooleanField(default=True)
    notify_on_status_change = models.BooleanField(default=True)
    notify_on_availability = models.BooleanField(default=True)
    
    # Métadonnées
    started_tracking_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Suivi Évolution Étudiant"
        verbose_name_plural = "Suivis Évolution Étudiants"
        unique_together = ['company', 'student']


### 1.5 Modèle InternshipCalendar (NOUVEAU)

```python
class InternshipCalendar(models.Model):
    """Calendrier de stages par filière publié par les écoles"""
    # Relations
    school = models.ForeignKey('SchoolProfile', on_delete=models.CASCADE, related_name='internship_calendars')
    program_manager = models.ForeignKey('ProgramManager', on_delete=models.SET_NULL, null=True, related_name='managed_calendars')
    
    # Informations filière
    program_name = models.CharField(max_length=200)  # Ex: "L3 AES"
    program_level = models.CharField(max_length=50)  # Ex: "Licence 3", "BTS 2ème année"
    
    # Période de stage
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Détails
    number_of_students = models.IntegerField()
    skills_sought = models.JSONField(default=list)  # Compétences recherchées
    description = models.TextField(blank=True)
    
    # Visibilité
    is_published = models.BooleanField(default=False)
    is_visible_to_companies = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Calendrier de Stage"
        verbose_name_plural = "Calendriers de Stages"
        ordering = ['start_date']


### 1.6 Modèle ProgramManager (NOUVEAU)

```python
class ProgramManager(models.Model):
    """Responsable de stage par filière"""
    # Relations
    school = models.ForeignKey('SchoolProfile', on_delete=models.CASCADE, related_name='program_managers')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Informations personnelles
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)  # Ex: "Dr.", "Pr.", "M.", "Mme"
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Filières gérées
    programs = models.JSONField(default=list)  # Liste des filières: ["L3 AES", "M1 AES"]
    
    # Statistiques
    active_conventions = models.IntegerField(default=0)
    total_conventions_managed = models.IntegerField(default=0)
    
    # Disponibilité
    is_active = models.BooleanField(default=True)
    office_hours = models.TextField(blank=True)  # Horaires de disponibilité
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Responsable de Stage"
        verbose_name_plural = "Responsables de Stage"
        
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"


### 1.7 Modèle VerificationDocument (NOUVEAU)

```python
class VerificationDocument(models.Model):
    """Documents de vérification pour particuliers et chauffeurs"""
    DOCUMENT_TYPES = [
        ('ID_CARD', 'Carte d\'identité'),
        ('PASSPORT', 'Passeport'),
        ('PROPERTY_PROOF', 'Justificatif de propriété'),
        ('ADDRESS_PROOF', 'Justificatif de domicile'),
        ('DRIVER_LICENSE', 'Permis de conduire'),
        ('VEHICLE_REGISTRATION', 'Carte grise'),
        ('INSURANCE', 'Attestation d\'assurance'),
        ('CRIMINAL_RECORD', 'Casier judiciaire'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
        ('EXPIRED', 'Expiré'),
    ]
    
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_documents')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_documents')
    
    # Document
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='verification_documents/')
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)
    
    # Dates
    expiry_date = models.DateField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Document de Vérification"
        verbose_name_plural = "Documents de Vérification"
        ordering = ['-submitted_at']


---

## 2. SERVICES ET LOGIQUE MÉTIER

### 2.1 RecommendationService

```python
class RecommendationService:
    """Service de gestion des recommandations"""
    
    @staticmethod
    def create_recommendation(company, student, internship, data):
        """Créer une recommandation"""
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
        
        # Mettre à jour le profil étudiant
        student.total_recommendations += 1
        student.save()
        
        # Notification à l'étudiant
        NotificationService.send_recommendation_notification(student, company)
        
        return recommendation
    
    @staticmethod
    def get_student_recommendations(student):
        """Récupérer toutes les recommandations d'un étudiant"""
        return InternRecommendation.objects.filter(
            student=student,
            is_public=True
        ).select_related('company', 'internship')
    
    @staticmethod
    def get_recommended_students(filters=None):
        """Récupérer les étudiants recommandés avec filtres"""
        students = StudentProfile.objects.filter(
            recommendations_received__isnull=False
        ).annotate(
            recommendation_count=Count('recommendations_received'),
            avg_rating=Avg('recommendations_received__rating')
        ).distinct()
        
        if filters:
            if 'min_rating' in filters:
                students = students.filter(avg_rating__gte=filters['min_rating'])
            if 'sector' in filters:
                students = students.filter(
                    recommendations_received__recommended_domains__contains=filters['sector']
                )
        
        return students.order_by('-recommendation_count', '-avg_rating')


### 2.2 StudentEvolutionService

```python
class StudentEvolutionService:
    """Service de suivi de l'évolution des étudiants"""
    
    @staticmethod
    def start_tracking(company, student):
        """Commencer à suivre un étudiant"""
        tracking, created = StudentEvolutionTracking.objects.get_or_create(
            company=company,
            student=student,
            defaults={
                'current_level': student.current_level,
                'domain': student.domain,
                'status': student.status,
                'evolution_history': []
            }
        )
        return tracking
    
    @staticmethod
    def update_student_evolution(student, new_level=None, new_domain=None, new_status=None):
        """Mettre à jour l'évolution d'un étudiant et notifier les entreprises"""
        trackings = StudentEvolutionTracking.objects.filter(student=student)
        
        for tracking in trackings:
            changes = []
            
            if new_level and new_level != tracking.current_level:
                if tracking.notify_on_level_change:
                    changes.append(f"Niveau: {tracking.current_level} → {new_level}")
                tracking.current_level = new_level
            
            if new_domain and new_domain != tracking.domain:
                changes.append(f"Domaine: {tracking.domain} → {new_domain}")
                tracking.domain = new_domain
            
            if new_status and new_status != tracking.status:
                if tracking.notify_on_status_change:
                    changes.append(f"Statut: {tracking.status} → {new_status}")
                tracking.status = new_status
            
            if changes:
                # Ajouter à l'historique
                tracking.evolution_history.append({
                    'date': timezone.now().isoformat(),
                    'changes': changes
                })
                tracking.save()
                
                # Notifier l'entreprise
                NotificationService.send_evolution_notification(
                    tracking.company,
                    student,
                    changes
                )
    
    @staticmethod
    def get_tracked_students(company, filters=None):
        """Récupérer les étudiants suivis par une entreprise"""
        trackings = StudentEvolutionTracking.objects.filter(
            company=company
        ).select_related('student')
        
        if filters:
            if 'status' in filters:
                trackings = trackings.filter(status=filters['status'])
            if 'domain' in filters:
                trackings = trackings.filter(domain__icontains=filters['domain'])
        
        return trackings.order_by('-last_updated_at')


### 2.3 InternshipCalendarService

```python
class InternshipCalendarService:
    """Service de gestion des calendriers de stages"""
    
    @staticmethod
    def create_calendar(school, program_manager, data):
        """Créer un calendrier de stage"""
        calendar = InternshipCalendar.objects.create(
            school=school,
            program_manager=program_manager,
            program_name=data['program_name'],
            program_level=data['program_level'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            number_of_students=data['number_of_students'],
            skills_sought=data.get('skills_sought', []),
            description=data.get('description', ''),
        )
        return calendar
    
    @staticmethod
    def publish_calendar(calendar):
        """Publier un calendrier"""
        calendar.is_published = True
        calendar.published_at = timezone.now()
        calendar.save()
        
        # Notifier les entreprises partenaires
        NotificationService.notify_partners_new_calendar(calendar)
        
        return calendar
    
    @staticmethod
    def get_public_calendars(filters=None):
        """Récupérer les calendriers publics"""
        calendars = InternshipCalendar.objects.filter(
            is_published=True,
            is_visible_to_companies=True
        ).select_related('school', 'program_manager')
        
        if filters:
            if 'school' in filters:
                calendars = calendars.filter(school=filters['school'])
            if 'program_level' in filters:
                calendars = calendars.filter(program_level__icontains=filters['program_level'])
            if 'start_date_from' in filters:
                calendars = calendars.filter(start_date__gte=filters['start_date_from'])
            if 'start_date_to' in filters:
                calendars = calendars.filter(start_date__lte=filters['start_date_to'])
        
        return calendars.order_by('start_date')
    
    @staticmethod
    def get_upcoming_calendars(months_ahead=6):
        """Récupérer les calendriers à venir"""
        today = timezone.now().date()
        future_date = today + timedelta(days=30 * months_ahead)
        
        return InternshipCalendar.objects.filter(
            is_published=True,
            start_date__gte=today,
            start_date__lte=future_date
        ).select_related('school', 'program_manager').order_by('start_date')


### 2.4 VerificationService

```python
class VerificationService:
    """Service de vérification des profils"""
    
    @staticmethod
    def submit_verification_documents(user, documents_data):
        """Soumettre des documents pour vérification"""
        documents = []
        for doc_data in documents_data:
            document = VerificationDocument.objects.create(
                user=user,
                document_type=doc_data['type'],
                file=doc_data['file'],
                expiry_date=doc_data.get('expiry_date')
            )
            documents.append(document)
        
        # Notifier l'équipe PRATIK
        NotificationService.notify_admin_new_verification(user, documents)
        
        return documents
    
    @staticmethod
    def verify_document(document, admin_user, approved, rejection_reason=None):
        """Vérifier un document"""
        document.verified_by = admin_user
        document.verified_at = timezone.now()
        
        if approved:
            document.status = 'APPROVED'
        else:
            document.status = 'REJECTED'
            document.rejection_reason = rejection_reason
        
        document.save()
        
        # Vérifier si tous les documents requis sont approuvés
        user = document.user
        if VerificationService.check_full_verification(user):
            user.is_verified = True
            user.verified_at = timezone.now()
            user.verified_by = admin_user
            user.save()
            
            # Notifier l'utilisateur
            NotificationService.send_verification_approved(user)
        elif not approved:
            # Notifier le rejet
            NotificationService.send_verification_rejected(user, document, rejection_reason)
        
        return document
    
    @staticmethod
    def check_full_verification(user):
        """Vérifier si tous les documents requis sont approuvés"""
        if user.user_type == 'LANDLORD':
            required_types = ['ID_CARD', 'PROPERTY_PROOF', 'ADDRESS_PROOF']
        elif user.user_type == 'DRIVER':
            required_types = ['DRIVER_LICENSE', 'VEHICLE_REGISTRATION', 'INSURANCE']
        else:
            return False
        
        approved_docs = VerificationDocument.objects.filter(
            user=user,
            status='APPROVED',
            document_type__in=required_types
        ).values_list('document_type', flat=True)
        
        return set(required_types).issubset(set(approved_docs))
    
    @staticmethod
    def get_pending_verifications():
        """Récupérer les vérifications en attente"""
        return VerificationDocument.objects.filter(
            status='PENDING'
        ).select_related('user').order_by('submitted_at')


### 2.5 PartnerPageService

```python
class PartnerPageService:
    """Service pour la page entreprises partenaires"""
    
    @staticmethod
    def get_partner_companies(filters=None):
        """Récupérer les entreprises partenaires"""
        companies = CompanyProfile.objects.filter(
            is_partner=True,
            is_visible_on_partners_page=True
        ).select_related('user')
        
        if filters:
            if 'sector' in filters:
                companies = companies.filter(sector__icontains=filters['sector'])
            if 'city' in filters:
                companies = companies.filter(city=filters['city'])
            if 'search' in filters:
                companies = companies.filter(
                    Q(company_name__icontains=filters['search']) |
                    Q(sector__icontains=filters['search'])
                )
        
        return companies.order_by('company_name')
    
    @staticmethod
    def get_sectors_list():
        """Récupérer la liste des secteurs"""
        return CompanyProfile.objects.filter(
            is_partner=True
        ).values_list('sector', flat=True).distinct().order_by('sector')
    
    @staticmethod
    def get_partner_stats():
        """Récupérer les statistiques des partenaires"""
        return {
            'total_partners': CompanyProfile.objects.filter(is_partner=True).count(),
            'total_interns_hosted': CompanyProfile.objects.filter(
                is_partner=True
            ).aggregate(Sum('total_interns_hosted'))['total_interns_hosted__sum'] or 0,
            'sectors_count': CompanyProfile.objects.filter(
                is_partner=True
            ).values('sector').distinct().count(),
            'average_rating': CompanyProfile.objects.filter(
                is_partner=True
            ).aggregate(Avg('average_rating'))['average_rating__avg'] or 0,
        }


---

## 3. VUES ET ENDPOINTS API

### 3.1 API Recommandations

```python
# views/recommendations.py

class RecommendationCreateView(APIView):
    """Créer une recommandation"""
    permission_classes = [IsAuthenticated, IsCompany]
    
    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            recommendation = RecommendationService.create_recommendation(
                company=request.user.companyprofile,
                student=serializer.validated_data['student'],
                internship=serializer.validated_data['internship'],
                data=serializer.validated_data
            )
            return Response(
                RecommendationSerializer(recommendation).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRecommendationsView(APIView):
    """Récupérer les recommandations d'un étudiant"""
    
    def get(self, request, student_id):
        student = get_object_or_404(StudentProfile, id=student_id)
        recommendations = RecommendationService.get_student_recommendations(student)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

class RecommendedStudentsView(APIView):
    """Récupérer les étudiants recommandés avec filtres"""
    
    def get(self, request):
        filters = {
            'min_rating': request.query_params.get('min_rating'),
            'sector': request.query_params.get('sector'),
        }
        students = RecommendationService.get_recommended_students(filters)
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)
```

### 3.2 API Suivi Évolution

```python
# views/evolution.py

class StartTrackingView(APIView):
    """Commencer à suivre un étudiant"""
    permission_classes = [IsAuthenticated, IsCompany]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        student = get_object_or_404(StudentProfile, id=student_id)
        tracking = StudentEvolutionService.start_tracking(
            company=request.user.companyprofile,
            student=student
        )
        return Response(
            StudentEvolutionTrackingSerializer(tracking).data,
            status=status.HTTP_201_CREATED
        )

class TrackedStudentsView(APIView):
    """Récupérer les étudiants suivis"""
    permission_classes = [IsAuthenticated, IsCompany]
    
    def get(self, request):
        filters = {
            'status': request.query_params.get('status'),
            'domain': request.query_params.get('domain'),
        }
        trackings = StudentEvolutionService.get_tracked_students(
            company=request.user.companyprofile,
            filters=filters
        )
        serializer = StudentEvolutionTrackingSerializer(trackings, many=True)
        return Response(serializer.data)
```

### 3.3 API Calendriers

```python
# views/calendars.py

class InternshipCalendarCreateView(APIView):
    """Créer un calendrier de stage"""
    permission_classes = [IsAuthenticated, IsSchool]
    
    def post(self, request):
        serializer = InternshipCalendarSerializer(data=request.data)
        if serializer.is_valid():
            calendar = InternshipCalendarService.create_calendar(
                school=request.user.schoolprofile,
                program_manager=serializer.validated_data.get('program_manager'),
                data=serializer.validated_data
            )
            return Response(
                InternshipCalendarSerializer(calendar).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicCalendarsView(APIView):
    """Récupérer les calendriers publics"""
    
    def get(self, request):
        filters = {
            'school': request.query_params.get('school'),
            'program_level': request.query_params.get('program_level'),
            'start_date_from': request.query_params.get('start_date_from'),
            'start_date_to': request.query_params.get('start_date_to'),
        }
        calendars = InternshipCalendarService.get_public_calendars(filters)
        serializer = InternshipCalendarSerializer(calendars, many=True)
        return Response(serializer.data)

class UpcomingCalendarsView(APIView):
    """Récupérer les calendriers à venir"""
    
    def get(self, request):
        months = int(request.query_params.get('months', 6))
        calendars = InternshipCalendarService.get_upcoming_calendars(months)
        serializer = InternshipCalendarSerializer(calendars, many=True)
        return Response(serializer.data)
```


### 3.4 API Page Partenaires

```python
# views/partners.py

class PartnerCompaniesView(APIView):
    """Récupérer les entreprises partenaires"""
    
    def get(self, request):
        filters = {
            'sector': request.query_params.get('sector'),
            'city': request.query_params.get('city'),
            'search': request.query_params.get('search'),
        }
        companies = PartnerPageService.get_partner_companies(filters)
        serializer = CompanyProfileSerializer(companies, many=True)
        return Response(serializer.data)

class PartnerSectorsView(APIView):
    """Récupérer la liste des secteurs"""
    
    def get(self, request):
        sectors = PartnerPageService.get_sectors_list()
        return Response({'sectors': list(sectors)})

class PartnerStatsView(APIView):
    """Récupérer les statistiques des partenaires"""
    
    def get(self, request):
        stats = PartnerPageService.get_partner_stats()
        return Response(stats)
```

### 3.5 API Vérification

```python
# views/verification.py

class SubmitVerificationView(APIView):
    """Soumettre des documents pour vérification"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        documents_data = request.data.get('documents', [])
        documents = VerificationService.submit_verification_documents(
            user=request.user,
            documents_data=documents_data
        )
        serializer = VerificationDocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyDocumentView(APIView):
    """Vérifier un document (admin only)"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, document_id):
        document = get_object_or_404(VerificationDocument, id=document_id)
        approved = request.data.get('approved', False)
        rejection_reason = request.data.get('rejection_reason')
        
        document = VerificationService.verify_document(
            document=document,
            admin_user=request.user,
            approved=approved,
            rejection_reason=rejection_reason
        )
        
        return Response(
            VerificationDocumentSerializer(document).data,
            status=status.HTTP_200_OK
        )

class PendingVerificationsView(APIView):
    """Récupérer les vérifications en attente (admin only)"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        documents = VerificationService.get_pending_verifications()
        serializer = VerificationDocumentSerializer(documents, many=True)
        return Response(serializer.data)
```

---

## 4. URLS ET ROUTING

```python
# urls.py

from django.urls import path
from .views import recommendations, evolution, calendars, partners, verification

urlpatterns = [
    # Recommandations
    path('recommendations/create/', recommendations.RecommendationCreateView.as_view()),
    path('recommendations/student/<int:student_id>/', recommendations.StudentRecommendationsView.as_view()),
    path('recommendations/recommended-students/', recommendations.RecommendedStudentsView.as_view()),
    
    # Suivi évolution
    path('evolution/start-tracking/', evolution.StartTrackingView.as_view()),
    path('evolution/tracked-students/', evolution.TrackedStudentsView.as_view()),
    
    # Calendriers
    path('calendars/create/', calendars.InternshipCalendarCreateView.as_view()),
    path('calendars/public/', calendars.PublicCalendarsView.as_view()),
    path('calendars/upcoming/', calendars.UpcomingCalendarsView.as_view()),
    
    # Partenaires
    path('partners/companies/', partners.PartnerCompaniesView.as_view()),
    path('partners/sectors/', partners.PartnerSectorsView.as_view()),
    path('partners/stats/', partners.PartnerStatsView.as_view()),
    
    # Vérification
    path('verification/submit/', verification.SubmitVerificationView.as_view()),
    path('verification/verify/<int:document_id>/', verification.VerifyDocumentView.as_view()),
    path('verification/pending/', verification.PendingVerificationsView.as_view()),
]
```

---

## 5. PERMISSIONS PERSONNALISÉES

```python
# permissions.py

from rest_framework import permissions

class IsCompany(permissions.BasePermission):
    """Permission pour les entreprises"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'COMPANY'

class IsSchool(permissions.BasePermission):
    """Permission pour les écoles"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'SCHOOL'

class IsVerified(permissions.BasePermission):
    """Permission pour les utilisateurs vérifiés"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified

class CanPublishListing(permissions.BasePermission):
    """Permission pour publier une annonce (vérifié requis pour particuliers/chauffeurs)"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.user_type in ['LANDLORD', 'DRIVER']:
            return request.user.is_verified
        
        return True
```

---

## 6. SIGNAUX (SIGNALS)

```python
# signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=StudentProfile)
def update_tracking_on_student_change(sender, instance, created, **kwargs):
    """Mettre à jour le suivi quand un étudiant change"""
    if not created:
        StudentEvolutionService.update_student_evolution(
            student=instance,
            new_level=instance.current_level,
            new_domain=instance.domain,
            new_status=instance.status
        )

@receiver(post_save, sender=InternRecommendation)
def update_student_stats_on_recommendation(sender, instance, created, **kwargs):
    """Mettre à jour les stats de l'étudiant"""
    if created:
        student = instance.student
        student.total_recommendations = student.recommendations_received.count()
        student.average_recommendation_rating = student.recommendations_received.aggregate(
            Avg('rating')
        )['rating__avg'] or 0
        student.save()

@receiver(post_save, sender=VerificationDocument)
def check_verification_completion(sender, instance, **kwargs):
    """Vérifier si la vérification est complète"""
    if instance.status == 'APPROVED':
        if VerificationService.check_full_verification(instance.user):
            instance.user.is_verified = True
            instance.user.verified_at = timezone.now()
            instance.user.save()
```

---

## 7. TÂCHES ASYNCHRONES (CELERY)

```python
# tasks.py

from celery import shared_task

@shared_task
def send_evolution_notifications():
    """Envoyer les notifications d'évolution quotidiennes"""
    # Récupérer les changements de la journée
    # Envoyer les notifications groupées
    pass

@shared_task
def check_document_expiry():
    """Vérifier l'expiration des documents"""
    expired_docs = VerificationDocument.objects.filter(
        status='APPROVED',
        expiry_date__lte=timezone.now().date()
    )
    
    for doc in expired_docs:
        doc.status = 'EXPIRED'
        doc.save()
        
        # Notifier l'utilisateur
        NotificationService.send_document_expired_notification(doc.user, doc)

@shared_task
def send_upcoming_calendar_reminders():
    """Envoyer des rappels pour les calendriers à venir"""
    # Calendriers qui commencent dans 30 jours
    upcoming = InternshipCalendarService.get_upcoming_calendars(months_ahead=1)
    
    for calendar in upcoming:
        # Notifier les entreprises partenaires
        NotificationService.notify_partners_upcoming_calendar(calendar)
```

---

## 8. TESTS UNITAIRES

```python
# tests/test_recommendations.py

class RecommendationServiceTest(TestCase):
    def setUp(self):
        self.company = CompanyProfileFactory()
        self.student = StudentProfileFactory()
        self.internship = InternshipFactory()
    
    def test_create_recommendation(self):
        data = {
            'rating': 5,
            'autonomy': True,
            'teamwork': True,
            'comment': 'Excellent stagiaire',
            'skills_validated': ['Python', 'Django'],
            'recommended_domains': ['Développement web']
        }
        
        recommendation = RecommendationService.create_recommendation(
            self.company, self.student, self.internship, data
        )
        
        self.assertEqual(recommendation.rating, 5)
        self.assertTrue(recommendation.autonomy)
        self.assertEqual(self.student.total_recommendations, 1)
    
    def test_get_recommended_students(self):
        # Créer plusieurs recommandations
        RecommendationFactory(student=self.student, rating=5)
        RecommendationFactory(student=self.student, rating=4)
        
        students = RecommendationService.get_recommended_students()
        
        self.assertIn(self.student, students)
        self.assertEqual(students[0].recommendation_count, 2)
```

---

## 9. DOCUMENTATION API (Swagger)

```python
# schema.py

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="PRATIK API",
        default_version='v1',
        description="API pour la plateforme PRATIK",
        contact=openapi.Contact(email="contact@pratik.gf"),
    ),
    public=True,
)
```

---

## 10. SÉCURITÉ ET PERFORMANCE

### 10.1 Sécurité
- Authentification JWT
- HTTPS obligatoire en production
- Rate limiting sur les endpoints sensibles
- Validation stricte des uploads de fichiers
- Sanitization des inputs utilisateurs
- CORS configuré strictement

### 10.2 Performance
- Cache Redis pour les listes de partenaires
- Pagination sur toutes les listes
- Indexation des champs fréquemment recherchés
- Optimisation des requêtes (select_related, prefetch_related)
- CDN pour les fichiers statiques

### 10.3 Monitoring
- Logs structurés (JSON)
- Sentry pour le tracking d'erreurs
- Métriques Prometheus
- Alertes sur les échecs de vérification

---

**FIN DU DOCUMENT DESIGN**
