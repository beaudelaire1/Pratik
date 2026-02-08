"""
Script pour créer des données de test pour Pratik
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.internships.models import Internship
from apps.services.models import HousingOffer, CarpoolingOffer, ForumPost, ForumComment
from apps.notifications.models import Notification
from datetime import datetime, timedelta

User = get_user_model()

def create_users():
    """Créer des utilisateurs de test"""
    print("📝 Création des utilisateurs...")
    
    # Étudiants
    students = [
        {
            'email': 'marie.dubois@email.com',
            'username': 'marie_dubois',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'user_type': 'student',
            'school': 'Université de Guyane',
            'field_of_study': 'Informatique',
            'graduation_year': 2026,
            'location': 'Cayenne',
            'bio': 'Étudiante en 3ème année d\'informatique, passionnée par le développement web.',
            'skills': 'Python, Django, JavaScript, React',
            'languages': 'Français, Anglais, Créole',
        },
        {
            'email': 'jean.martin@email.com',
            'username': 'jean_martin',
            'first_name': 'Jean',
            'last_name': 'Martin',
            'user_type': 'student',
            'school': 'Lycée Félix Éboué',
            'field_of_study': 'Commerce',
            'graduation_year': 2025,
            'location': 'Kourou',
            'bio': 'Étudiant en BTS Commerce, intéressé par le marketing digital.',
            'skills': 'Marketing, Communication, Excel',
            'languages': 'Français, Anglais',
        },
        {
            'email': 'sophie.leroy@email.com',
            'username': 'sophie_leroy',
            'first_name': 'Sophie',
            'last_name': 'Leroy',
            'user_type': 'student',
            'school': 'Université de Guyane',
            'field_of_study': 'Biologie',
            'graduation_year': 2026,
            'location': 'Saint-Laurent-du-Maroni',
            'bio': 'Passionnée par la biodiversité amazonienne.',
            'skills': 'Recherche, Analyse, Rédaction scientifique',
            'languages': 'Français, Anglais, Espagnol',
        },
    ]
    
    # Entreprises
    companies = [
        {
            'email': 'contact@guyatech.gf',
            'username': 'GuyaTech',
            'user_type': 'company',
            'company_name': 'GuyaTech Solutions',
            'company_description': 'Entreprise innovante spécialisée dans le développement de solutions digitales pour la Guyane.',
            'industry': 'Technologie',
            'company_size': '10-50 employés',
            'location': 'Cayenne',
            'siret': '12345678900012',
            'website': 'https://guyatech.gf',
        },
        {
            'email': 'rh@amazonia-market.gf',
            'username': 'Amazonia_Market',
            'user_type': 'company',
            'company_name': 'Amazonia Market',
            'company_description': 'Leader de la distribution en Guyane, nous proposons des produits locaux et importés.',
            'industry': 'Commerce',
            'company_size': '50-200 employés',
            'location': 'Cayenne',
            'siret': '98765432100023',
        },
        {
            'email': 'contact@ecoguyana.gf',
            'username': 'EcoGuyana',
            'user_type': 'company',
            'company_name': 'EcoGuyana',
            'company_description': 'Association dédiée à la préservation de l\'environnement en Guyane.',
            'industry': 'Environnement',
            'company_size': '1-10 employés',
            'location': 'Kourou',
        },
        {
            'email': 'contact@digital-guyane.gf',
            'username': 'Digital_Guyane',
            'user_type': 'company',
            'company_name': 'Digital Guyane',
            'company_description': 'Agence de communication digitale spécialisée dans le web et les réseaux sociaux.',
            'industry': 'Communication',
            'company_size': '10-50 employés',
            'location': 'Cayenne',
        },
    ]
    
    created_students = []
    created_companies = []
    
    for student_data in students:
        user, created = User.objects.get_or_create(
            email=student_data['email'],
            defaults={**student_data, 'password': 'password123'}
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  ✅ Étudiant créé: {user.get_display_name()}")
        created_students.append(user)
    
    for company_data in companies:
        user, created = User.objects.get_or_create(
            email=company_data['email'],
            defaults={**company_data, 'password': 'password123'}
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  ✅ Entreprise créée: {user.get_display_name()}")
        created_companies.append(user)
    
    return created_students, created_companies


def create_internships(companies):
    """Créer des offres de stage"""
    print("\n💼 Création des offres de stage...")
    
    internships_data = [
        {
            'company': companies[0],  # GuyaTech
            'title': 'Développeur Web Full Stack',
            'description': '''Nous recherchons un développeur web passionné pour rejoindre notre équipe dynamique.

Missions :
- Développement d'applications web avec Django et React
- Participation à la conception de nouvelles fonctionnalités
- Maintenance et amélioration du code existant
- Travail en équipe agile

Profil recherché :
- Étudiant en informatique (Bac+3 minimum)
- Connaissances en Python, JavaScript
- Autonome et motivé
- Bon esprit d'équipe

Rémunération : 600€/mois
Date de début souhaitée : Dans 1 mois
Date limite de candidature : Dans 15 jours''',
            'location': 'Cayenne',
            'duration': '6 mois',
            'salary': '600€/mois',
            'is_active': True,
        },
        {
            'company': companies[1],  # Amazonia Market
            'title': 'Assistant Marketing Digital',
            'description': '''Rejoignez notre équipe marketing pour développer notre présence en ligne.

Missions :
- Gestion des réseaux sociaux (Facebook, Instagram, TikTok)
- Création de contenu visuel et rédactionnel
- Analyse des performances des campagnes
- Participation aux événements promotionnels

Profil recherché :
- Étudiant en marketing/communication (BTS/Licence)
- Créatif et à l'aise avec les outils digitaux
- Bonne expression écrite
- Connaissance du marché guyanais appréciée

Rémunération : 500€/mois
Durée : 4 mois''',
            'location': 'Cayenne',
            'duration': '4 mois',
            'salary': '500€/mois',
            'is_active': True,
        },
        {
            'company': companies[2],  # EcoGuyana
            'title': 'Chargé de Mission Environnement',
            'description': '''Participez à nos projets de préservation de la biodiversité amazonienne.

Missions :
- Participation aux études de terrain
- Sensibilisation du public à l'environnement
- Rédaction de rapports d'activité
- Organisation d'événements éco-responsables

Profil recherché :
- Étudiant en biologie/environnement (Licence minimum)
- Passionné par la nature guyanaise
- Capacité à travailler en extérieur
- Permis B souhaité

Stage non rémunéré (indemnités de transport possibles)
Durée : 3 mois''',
            'location': 'Kourou',
            'duration': '3 mois',
            'is_active': True,
        },
        {
            'company': companies[3],  # Digital Guyane
            'title': 'Community Manager',
            'description': '''Nous cherchons un community manager créatif pour gérer nos clients.

Missions :
- Animation des communautés en ligne
- Création de contenus engageants
- Veille concurrentielle
- Reporting des performances

Profil recherché :
- Étudiant en communication (BTS minimum)
- Excellente maîtrise des réseaux sociaux
- Créatif et réactif
- Orthographe irréprochable

Rémunération : 550€/mois
Durée : 6 mois''',
            'location': 'Cayenne',
            'duration': '6 mois',
            'salary': '550€/mois',
            'is_active': True,
        },
        {
            'company': companies[0],  # GuyaTech
            'title': 'Assistant Chef de Projet IT',
            'description': '''Assistez notre chef de projet dans la gestion de projets digitaux.

Missions :
- Suivi des projets clients
- Coordination avec les équipes techniques
- Rédaction de documentation
- Participation aux réunions clients

Profil recherché :
- Étudiant en informatique/gestion de projet (Bac+3)
- Organisé et rigoureux
- Bonnes capacités de communication
- Intérêt pour la gestion de projet

Rémunération : 580€/mois
Durée : 5 mois''',
            'location': 'Cayenne',
            'duration': '5 mois',
            'salary': '580€/mois',
            'is_active': True,
        },
    ]
    
    created_internships = []
    for internship_data in internships_data:
        internship, created = Internship.objects.get_or_create(
            title=internship_data['title'],
            company=internship_data['company'],
            defaults=internship_data
        )
        if created:
            print(f"  ✅ Stage créé: {internship.title} chez {internship.company.get_display_name()}")
        created_internships.append(internship)
    
    return created_internships


def create_housing_offers(students):
    """Créer des offres de logement"""
    print("\n🏠 Création des offres de logement...")
    
    housing_data = [
        {
            'owner': students[0],
            'title': 'Studio meublé - Centre Cayenne',
            'description': '''Studio de 25m² entièrement meublé en plein centre de Cayenne.

Équipements :
- Cuisine équipée
- Salle de bain avec douche
- Climatisation
- WiFi inclus
- Proche transports en commun

Idéal pour étudiant en stage.''',
            'location': 'Cayenne',
            'price': 450,
            'housing_type': 'studio',
            'contact_email': students[0].email,
        },
        {
            'owner': students[1],
            'title': 'Colocation T3 - Kourou',
            'description': '''Chambre disponible dans T3 en colocation à Kourou.

Détails :
- Chambre meublée de 12m²
- Cuisine et salon partagés
- 2 colocataires sympas
- Proche du centre spatial
- Parking disponible

Ambiance conviviale garantie !''',
            'location': 'Kourou',
            'price': 300,
            'housing_type': 'coloc',
            'contact_email': students[1].email,
        },
        {
            'owner': students[2],
            'title': 'Appartement F2 - Saint-Laurent',
            'description': '''Bel appartement F2 de 45m² à Saint-Laurent-du-Maroni.

Caractéristiques :
- 1 chambre spacieuse
- Salon lumineux
- Cuisine américaine équipée
- Balcon avec vue
- Parking sécurisé

Calme et bien situé.''',
            'location': 'Saint-Laurent-du-Maroni',
            'price': 550,
            'housing_type': 'apartment',
            'contact_email': students[2].email,
        },
    ]
    
    for housing in housing_data:
        offer, created = HousingOffer.objects.get_or_create(
            title=housing['title'],
            owner=housing['owner'],
            defaults=housing
        )
        if created:
            print(f"  ✅ Logement créé: {offer.title}")


def create_carpooling_offers(students):
    """Créer des offres de covoiturage"""
    print("\n🚗 Création des offres de covoiturage...")
    
    carpooling_data = [
        {
            'driver': students[0],
            'departure': 'Cayenne',
            'destination': 'Kourou',
            'date_time': datetime.now() + timedelta(days=2, hours=8),
            'seats_available': 3,
            'price': 15,
            'description': 'Trajet régulier Cayenne-Kourou tous les lundis matin. Départ 8h devant l\'université.',
        },
        {
            'driver': students[1],
            'departure': 'Kourou',
            'destination': 'Cayenne',
            'date_time': datetime.now() + timedelta(days=3, hours=18),
            'seats_available': 2,
            'price': 15,
            'description': 'Retour Kourou-Cayenne vendredi soir. Départ 18h du centre spatial.',
        },
        {
            'driver': students[2],
            'departure': 'Saint-Laurent-du-Maroni',
            'destination': 'Cayenne',
            'date_time': datetime.now() + timedelta(days=5, hours=7),
            'seats_available': 4,
            'price': 25,
            'description': 'Trajet Saint-Laurent vers Cayenne. Départ tôt le matin, retour possible le soir.',
        },
    ]
    
    for carpooling in carpooling_data:
        offer, created = CarpoolingOffer.objects.get_or_create(
            driver=carpooling['driver'],
            departure=carpooling['departure'],
            destination=carpooling['destination'],
            date_time=carpooling['date_time'],
            defaults=carpooling
        )
        if created:
            print(f"  ✅ Covoiturage créé: {offer.departure} → {offer.destination}")


def create_forum_posts(students):
    """Créer des posts de forum"""
    print("\n💬 Création des posts de forum...")
    
    posts_data = [
        {
            'author': students[0],
            'title': 'Conseils pour trouver un stage en informatique ?',
            'content': '''Bonjour à tous !

Je suis en 3ème année d'informatique et je cherche un stage pour valider mon diplôme. 
Auriez-vous des conseils pour trouver un stage en développement web en Guyane ?

Quelles entreprises contacter en priorité ? Comment se démarquer ?

Merci d'avance pour vos retours ! 😊''',
        },
        {
            'author': students[1],
            'title': 'Logement étudiant à Cayenne - Vos bons plans ?',
            'content': '''Salut la communauté !

Je vais faire mon stage à Cayenne à partir de mars et je cherche un logement pas trop cher.

Vous avez des bons plans ? Des quartiers à privilégier ou à éviter ?

Budget max : 500€/mois

Merci ! 🏠''',
        },
        {
            'author': students[2],
            'title': 'Retour d\'expérience : Stage chez EcoGuyana',
            'content': '''Hello !

Je voulais partager mon expérience de stage chez EcoGuyana. 

Points positifs :
- Équipe super sympa et accueillante
- Missions variées et intéressantes
- Découverte de la biodiversité guyanaise
- Ambiance de travail détendue

Points à améliorer :
- Stage non rémunéré (prévoir un budget)
- Déplacements fréquents en forêt

Dans l'ensemble, une expérience enrichissante que je recommande aux passionnés d'environnement ! 🌿

N'hésitez pas si vous avez des questions !''',
        },
    ]
    
    created_posts = []
    for post_data in posts_data:
        post, created = ForumPost.objects.get_or_create(
            title=post_data['title'],
            author=post_data['author'],
            defaults=post_data
        )
        if created:
            print(f"  ✅ Post créé: {post.title}")
        created_posts.append(post)
    
    # Ajouter des commentaires
    comments_data = [
        {
            'post': created_posts[0],
            'author': students[1],
            'content': 'Salut ! Je te conseille de regarder du côté de GuyaTech et Digital Guyane, ils recrutent souvent des stagiaires. Bon courage ! 💪',
        },
        {
            'post': created_posts[1],
            'author': students[0],
            'content': 'Le quartier de Baduel est pas mal pour les étudiants, bien desservi et pas trop cher. Évite le centre si tu as un budget serré.',
        },
        {
            'post': created_posts[2],
            'author': students[0],
            'content': 'Merci pour ce retour ! Ça donne envie. Tu as fait combien de temps de stage ?',
        },
    ]
    
    for comment_data in comments_data:
        comment, created = ForumComment.objects.get_or_create(
            post=comment_data['post'],
            author=comment_data['author'],
            content=comment_data['content'],
        )
        if created:
            print(f"  ✅ Commentaire ajouté sur: {comment.post.title}")


def main():
    """Fonction principale"""
    print("🚀 Création des données de test pour Pratik\n")
    print("=" * 60)
    
    # Créer les utilisateurs
    students, companies = create_users()
    
    # Créer les stages
    internships = create_internships(companies)
    
    # Créer les offres de logement
    create_housing_offers(students)
    
    # Créer les offres de covoiturage
    create_carpooling_offers(students)
    
    # Créer les posts de forum
    create_forum_posts(students)
    
    print("\n" + "=" * 60)
    print("✅ Données de test créées avec succès !")
    print("\n📊 Résumé :")
    print(f"  - {len(students)} étudiants")
    print(f"  - {len(companies)} entreprises")
    print(f"  - {len(internships)} offres de stage")
    print(f"  - 3 offres de logement")
    print(f"  - 3 offres de covoiturage")
    print(f"  - 3 posts de forum")
    
    print("\n🔐 Identifiants de connexion :")
    print("\n  Étudiants :")
    for student in students:
        print(f"    - {student.email} / password123")
    
    print("\n  Entreprises :")
    for company in companies:
        print(f"    - {company.email} / password123")
    
    print("\n🌐 Accédez au site : http://127.0.0.1:8000/")
    print("=" * 60)


if __name__ == '__main__':
    main()
