"""
Script pour créer des données de démonstration pour la plateforme Pratik
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.profile_models import (
    StudentProfile, CompanyProfile, SchoolProfile, TrainingCenterProfile,
    RecruiterProfile, LandlordProfile, DriverProfile, PartnerProfile
)
from apps.users.models_school import Teacher, StudentSchoolEnrollment
from apps.internships.models import Internship
from apps.services.models import HousingOffer, CarpoolingOffer
from apps.calendars.models import InternshipCalendar
from apps.tracking.models import InternshipTracking
from apps.events.models import Event
from apps.hub.models import Training

User = get_user_model()

def clear_all_data():
    """Supprime tous les utilisateurs et données associées"""
    print("🗑️  Suppression de toutes les données existantes...")
    
    # Supprimer les formations d'abord (pour éviter les conflits de slug)
    from apps.hub.models import Training
    Training.objects.all().delete()
    
    # Supprimer tous les utilisateurs (cascade sur les autres données)
    User.objects.all().delete()
    
    print("✅ Données supprimées")

def create_users():
    """Crée les utilisateurs de base"""
    print("\n👥 Création des utilisateurs...")
    
    users = {}
    
    # 1. Étudiant
    users['etudiant1'] = User.objects.create_user(
        username='etudiant1',
        email='etudiant1@pratik.gf',
        password='user1234',
        first_name='Jean',
        last_name='Dupont',
        user_type='student',
        phone='0694123456'
    )
    StudentProfile.objects.create(
        user=users['etudiant1'],
        school='Université de Guyane',
        current_level='Licence 3',
        field_of_study='Administration Économique et Sociale',
        domain='Gestion',
        status='STUDYING',
        looking_for_internship=True,
        skills='Comptabilité, Excel, Communication'
    )
    
    # 2. École
    users['ecole1'] = User.objects.create_user(
        username='ecole1',
        email='ecole1@pratik.gf',
        password='user1234',
        first_name='Lycée',
        last_name='Félix Éboué',
        user_type='school',
        phone='0594123456'
    )
    SchoolProfile.objects.create(
        user=users['ecole1'],
        institution_name='Lycée Félix Éboué',
        institution_type='HIGH_SCHOOL',
        address='Avenue Léopold Héder',
        city='Cayenne',
        postal_code='97300',
        phone='0594123456',
        email='contact@lycee-eboue.gf',
        description='Établissement d\'enseignement secondaire de référence en Guyane',
        total_students=850
    )
    
    # 3. Entreprise
    users['entreprise1'] = User.objects.create_user(
        username='entreprise1',
        email='entreprise1@pratik.gf',
        password='user1234',
        first_name='Tech',
        last_name='Guyane',
        user_type='company',
        phone='0594234567'
    )
    CompanyProfile.objects.create(
        user=users['entreprise1'],
        company_name='Tech Guyane SARL',
        siret='12345678901234',
        sector='Informatique et Services',
        description='Entreprise spécialisée dans le développement web et mobile',
        address='Zone Industrielle de Collery',
        city='Cayenne',
        postal_code='97300',
        is_partner=True,
        partner_since=datetime.now().date()
    )
    
    # 4. Centre de Formation
    users['formation1'] = User.objects.create_user(
        username='formation1',
        email='formation1@pratik.gf',
        password='user1234',
        first_name='Centre',
        last_name='Formation Pro',
        user_type='training_center',
        phone='0594345678'
    )
    TrainingCenterProfile.objects.create(
        user=users['formation1'],
        center_name='Centre de Formation Professionnelle de Guyane',
        certification_number='CERT-GF-2024-001',
        address='Rue du Commerce',
        city='Cayenne',
        postal_code='97300',
        phone='0594345678',
        email='contact@cfp-guyane.gf',
        description='Formation professionnelle continue et alternance',
        specializations='Informatique, Commerce, Gestion',
        is_certified=True,
        placement_rate=78.5
    )
    
    # 5. Recruteur
    users['recruteur1'] = User.objects.create_user(
        username='recruteur1',
        email='recruteur1@pratik.gf',
        password='user1234',
        first_name='Marie',
        last_name='Talent',
        user_type='recruiter',
        phone='0694456789'
    )
    RecruiterProfile.objects.create(
        user=users['recruteur1'],
        agency_name='Talents Guyane',
        specialization='Recrutement IT et Digital',
        phone='0694456789',
        professional_email='marie@talents-guyane.gf',
        bio='Spécialiste du recrutement dans le secteur numérique en Guyane'
    )
    
    # 6. Propriétaire
    users['proprietaire1'] = User.objects.create_user(
        username='proprietaire1',
        email='proprietaire1@pratik.gf',
        password='user1234',
        first_name='Pierre',
        last_name='Logement',
        user_type='landlord',
        phone='0694567890',
        is_verified=True
    )
    LandlordProfile.objects.create(
        user=users['proprietaire1'],
        full_name='Pierre Logement',
        phone='0694567890',
        email='pierre@logements-guyane.gf',
        address='Rue Christophe Colomb',
        city='Cayenne',
        postal_code='97300',
        total_properties=3,
        available_properties=1
    )
    
    # 7. Chauffeur
    users['chauffeur1'] = User.objects.create_user(
        username='chauffeur1',
        email='chauffeur1@pratik.gf',
        password='user1234',
        first_name='Paul',
        last_name='Transport',
        user_type='driver',
        phone='0694678901',
        is_verified=True
    )
    DriverProfile.objects.create(
        user=users['chauffeur1'],
        full_name='Paul Transport',
        phone='0694678901',
        email='paul@transport-guyane.gf',
        vehicle_make='Renault',
        vehicle_model='Clio',
        vehicle_year=2020,
        vehicle_color='Bleu',
        license_plate='AB-123-CD',
        seats_available=3,
        license_number='123456789',
        license_expiry=datetime.now().date() + timedelta(days=365*2),
        insurance_company='AXA Guyane',
        insurance_policy_number='POL-2024-001',
        insurance_expiry=datetime.now().date() + timedelta(days=365)
    )
    
    # 8. Partenaire
    users['partenaire1'] = User.objects.create_user(
        username='partenaire1',
        email='partenaire1@pratik.gf',
        password='user1234',
        first_name='CTG',
        last_name='Guyane',
        user_type='partner',
        phone='0594789012'
    )
    PartnerProfile.objects.create(
        user=users['partenaire1'],
        organization_name='Collectivité Territoriale de Guyane',
        partner_type='GOVERNMENT',
        address='Place Léopold Héder',
        city='Cayenne',
        postal_code='97300',
        phone='0594789012',
        email='contact@ctguyane.fr',
        description='Institution publique de la Guyane',
        mission='Développement économique et social du territoire',
        is_featured=True
    )
    
    print(f"✅ {len(users)} utilisateurs créés")
    return users

def create_school_hierarchy(users):
    """Crée la hiérarchie école -> enseignants -> élèves"""
    print("\n🏫 Création de la hiérarchie école...")
    
    # Créer des enseignants
    teacher1 = Teacher.objects.create(
        school=users['ecole1'],
        first_name='Sophie',
        last_name='Martin',
        email='sophie.martin@lycee-eboue.gf',
        phone='0594111111',
        subjects='Économie, Gestion',
        is_active=True
    )
    
    teacher2 = Teacher.objects.create(
        school=users['ecole1'],
        first_name='Thomas',
        last_name='Bernard',
        email='thomas.bernard@lycee-eboue.gf',
        phone='0594222222',
        subjects='Informatique, Mathématiques',
        is_active=True
    )
    
    # Inscrire l'étudiant dans l'école
    enrollment = StudentSchoolEnrollment.objects.create(
        student=users['etudiant1'],
        school=users['ecole1'],
        teacher=teacher1,
        class_name='Terminale STMG',
        program='Sciences et Technologies du Management et de la Gestion',
        academic_year='2025-2026',
        student_number='STU-2025-001',
        is_active=True
    )
    
    print(f"✅ 2 enseignants et 1 inscription créés")
    return teacher1, teacher2, enrollment

def create_internships(users):
    """Crée des offres de stage"""
    print("\n💼 Création des offres de stage...")
    
    internships = []
    
    internships.append(Internship.objects.create(
        title='Stage Développeur Web Junior',
        company=users['entreprise1'],
        description='Rejoignez notre équipe pour développer des applications web modernes. Vous travaillerez sur des projets réels avec React et Django.',
        location='Cayenne',
        salary='Gratification légale (600€/mois)',
        duration='3 mois',
        is_active=True
    ))
    
    internships.append(Internship.objects.create(
        title='Assistant Marketing Digital',
        company=users['entreprise1'],
        description='Participez à nos campagnes marketing digital, gestion des réseaux sociaux et création de contenu.',
        location='Cayenne',
        salary='Gratification légale',
        duration='6 mois',
        is_active=True
    ))
    
    print(f"✅ {len(internships)} offres de stage créées")
    return internships

def create_housing_offers(users):
    """Crée des offres de logement"""
    print("\n🏠 Création des offres de logement...")
    
    offers = []
    
    offers.append(HousingOffer.objects.create(
        owner=users['proprietaire1'],
        title='Studio meublé proche université',
        description='Studio de 25m² entièrement meublé et équipé. Cuisine équipée, salle de bain, internet inclus. Idéal pour étudiant.',
        housing_type='studio',
        location='Cayenne Centre',
        price=280.00,
        contact_email='pierre@logements-guyane.gf',
        contact_phone='0694567890',
        is_available=True
    ))
    
    offers.append(HousingOffer.objects.create(
        owner=users['proprietaire1'],
        title='Chambre chez l\'habitant',
        description='Chambre confortable dans maison familiale. Accès cuisine, wifi, ambiance conviviale.',
        housing_type='room',
        location='Rémire-Montjoly',
        price=250.00,
        contact_email='pierre@logements-guyane.gf',
        contact_phone='0694567890',
        is_available=True
    ))
    
    print(f"✅ {len(offers)} offres de logement créées")
    return offers

def create_carpooling_offers(users):
    """Crée des offres de covoiturage"""
    print("\n🚗 Création des offres de covoiturage...")
    
    offers = []
    
    tomorrow = datetime.now() + timedelta(days=1)
    
    offers.append(CarpoolingOffer.objects.create(
        driver=users['chauffeur1'],
        departure='Cayenne',
        destination='Saint-Laurent-du-Maroni',
        date_time=tomorrow.replace(hour=7, minute=0),
        seats_available=3,
        price=45.00,
        description='Départ tôt le matin, retour le soir même possible.',
        is_active=True
    ))
    
    next_week = datetime.now() + timedelta(days=7)
    
    offers.append(CarpoolingOffer.objects.create(
        driver=users['chauffeur1'],
        departure='Cayenne',
        destination='Kourou',
        date_time=next_week.replace(hour=14, minute=30),
        seats_available=2,
        price=15.00,
        description='Trajet régulier, possibilité d\'arrangement pour trajets récurrents.',
        is_active=True
    ))
    
    print(f"✅ {len(offers)} offres de covoiturage créées")
    return offers

def create_school_calendar(users):
    """Crée un calendrier de stage pour l'école"""
    print("\n📅 Création du calendrier de stage...")
    
    calendar = InternshipCalendar.objects.create(
        school=users['ecole1'].school_profile,
        program_name='Terminale STMG',
        program_level='Terminale',
        start_date=datetime.now().date() + timedelta(days=30),
        end_date=datetime.now().date() + timedelta(days=90),
        number_of_students=25,
        skills_sought=['Gestion', 'Commerce', 'Communication', 'Informatique'],
        description='Stage de fin d\'année pour les élèves de Terminale STMG',
        is_published=True,
        is_visible_to_companies=True
    )
    
    print("✅ Calendrier de stage créé")
    return calendar

def create_trainings(users):
    """Crée des formations"""
    print("\n📚 Création des formations...")
    
    trainings = []
    
    trainings.append(Training.objects.create(
        title='Initiation au Développement Web',
        description='Apprenez les bases du développement web avec HTML, CSS et JavaScript',
        objectives='- Maîtriser HTML5 et CSS3\n- Créer des sites web responsives\n- Comprendre JavaScript',
        prerequisites='Aucun prérequis, formation accessible à tous',
        difficulty='beginner',
        duration_hours=40,
        instructor_name='Thomas Bernard',
        instructor_bio='Développeur web avec 10 ans d\'expérience',
        is_active=True,
        is_featured=True
    ))
    
    trainings.append(Training.objects.create(
        title='Gestion de Projet Agile',
        description='Maîtrisez les méthodes agiles pour gérer vos projets efficacement',
        objectives='- Comprendre Scrum et Kanban\n- Organiser des sprints\n- Gérer une équipe agile',
        prerequisites='Expérience en gestion de projet recommandée',
        difficulty='intermediate',
        duration_hours=24,
        instructor_name='Sophie Martin',
        instructor_bio='Chef de projet certifiée Scrum Master',
        is_active=True
    ))
    
    print(f"✅ {len(trainings)} formations créées")
    return trainings

def create_events(users):
    """Crée des événements"""
    print("\n📅 Création des événements...")
    
    events = []
    
    next_month = datetime.now() + timedelta(days=30)
    
    events.append(Event.objects.create(
        user=users['partenaire1'],
        title='Forum de l\'Emploi et des Stages',
        description='Rencontrez les entreprises qui recrutent en Guyane',
        event_type='conference',
        start_date=next_month.date(),
        start_time=datetime.strptime('09:00', '%H:%M').time(),
        end_date=next_month.date(),
        end_time=datetime.strptime('17:00', '%H:%M').time(),
        location='Palais des Congrès de Cayenne',
        is_public=True
    ))
    
    print(f"✅ {len(events)} événements créés")
    return events

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 CRÉATION DES DONNÉES DE DÉMONSTRATION PRATIK")
    print("=" * 60)
    
    # Supprimer les données existantes
    clear_all_data()
    
    # Créer les utilisateurs
    users = create_users()
    
    # Créer la hiérarchie école
    teacher1, teacher2, enrollment = create_school_hierarchy(users)
    
    # Créer les offres de stage
    internships = create_internships(users)
    
    # Créer les offres de logement
    housing_offers = create_housing_offers(users)
    
    # Créer les offres de covoiturage
    carpooling_offers = create_carpooling_offers(users)
    
    # Créer le calendrier de stage
    calendar = create_school_calendar(users)
    
    # Créer les formations
    trainings = create_trainings(users)
    
    # Créer les événements
    events = create_events(users)
    
    print("\n" + "=" * 60)
    print("✅ DONNÉES DE DÉMONSTRATION CRÉÉES AVEC SUCCÈS!")
    print("=" * 60)
    print("\n📋 COMPTES CRÉÉS (tous avec mot de passe: user1234):")
    print("-" * 60)
    print("👨‍🎓 Étudiant:        etudiant1@pratik.gf")
    print("🏫 École:           ecole1@pratik.gf")
    print("🏢 Entreprise:      entreprise1@pratik.gf")
    print("📚 Formation:       formation1@pratik.gf")
    print("💼 Recruteur:       recruteur1@pratik.gf")
    print("🏠 Propriétaire:    proprietaire1@pratik.gf")
    print("🚗 Chauffeur:       chauffeur1@pratik.gf")
    print("🤝 Partenaire:      partenaire1@pratik.gf")
    print("-" * 60)
    print("\n📊 DONNÉES CRÉÉES:")
    print(f"  • {len(internships)} offres de stage")
    print(f"  • {len(housing_offers)} offres de logement")
    print(f"  • {len(carpooling_offers)} offres de covoiturage")
    print(f"  • {len(trainings)} formations")
    print(f"  • {len(events)} événements")
    print(f"  • 2 enseignants")
    print(f"  • 1 inscription élève")
    print(f"  • 1 calendrier de stage")
    print("\n🌐 Accédez à la plateforme: http://localhost:8000")
    print("=" * 60)

if __name__ == '__main__':
    main()
