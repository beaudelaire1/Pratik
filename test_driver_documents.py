"""
Script de test pour simuler un chauffeur ajoutant des documents.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.base import ContentFile
from apps.users.models import CustomUser
from apps.users.models_documents import UserDocument
from core.services.document_checklist_service import DocumentChecklistService

def create_test_driver():
    """Créer ou récupérer un utilisateur chauffeur de test."""
    driver, created = CustomUser.objects.get_or_create(
        email='chauffeur.test@pratik.fr',
        defaults={
            'username': 'chauffeur_test',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'user_type': 'driver',
            'phone': '+33612345678',
            'location': 'Paris',
        }
    )
    if created:
        driver.set_password('test1234')
        driver.save()
        print(f"✅ Chauffeur créé: {driver.email}")
    else:
        print(f"ℹ️ Chauffeur existant: {driver.email}")
    return driver

def show_checklist(driver):
    """Afficher la checklist du chauffeur."""
    service = DocumentChecklistService()
    checklist = service.get_checklist(driver)
    completion = service.get_completion_percentage(driver)
    all_approved = service.are_all_required_approved(driver)
    
    print(f"\n📋 Checklist pour {driver.get_display_name()} ({driver.user_type}):")
    print(f"   Progression: {completion}%")
    print(f"   Tous approuvés: {'✅ Oui' if all_approved else '❌ Non'}")
    print("-" * 50)
    
    for item in checklist:
        status_icon = {
            'missing': '⚪',
            'pending': '⏳',
            'approved': '✅',
            'rejected': '❌'
        }.get(item.status, '?')
        print(f"   {status_icon} {item.label}: {item.status}")
    
    return checklist

def create_fake_pdf():
    """Créer un faux fichier PDF pour les tests."""
    # Contenu minimal d'un PDF valide
    pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n199\n%%EOF'
    return ContentFile(pdf_content, name='document.pdf')

def add_document(driver, doc_type, title):
    """Ajouter un document pour le chauffeur."""
    # Vérifier si le document existe déjà
    existing = UserDocument.objects.filter(user=driver, document_type=doc_type).first()
    if existing:
        print(f"   ℹ️ Document '{title}' existe déjà (statut: {existing.status})")
        return existing
    
    doc = UserDocument.objects.create(
        user=driver,
        document_type=doc_type,
        title=title,
        file=create_fake_pdf(),
        description=f"Document de test: {title}",
        status='pending'
    )
    print(f"   ✅ Document ajouté: {title} (ID: {doc.id})")
    return doc

def main():
    print("=" * 60)
    print("🚗 TEST: Chauffeur ajoutant des documents")
    print("=" * 60)
    
    # 1. Créer le chauffeur
    driver = create_test_driver()
    
    # 2. Afficher la checklist initiale
    print("\n📊 ÉTAT INITIAL:")
    show_checklist(driver)
    
    # 3. Ajouter les documents requis pour un chauffeur
    print("\n📤 AJOUT DES DOCUMENTS:")
    documents_to_add = [
        ('id_card', 'Carte d\'identité - Jean Dupont'),
        ('address_proof', 'Justificatif de domicile - Facture EDF'),
        ('driver_license', 'Permis de conduire B'),
    ]
    
    for doc_type, title in documents_to_add:
        add_document(driver, doc_type, title)
    
    # 4. Afficher la checklist après ajout
    print("\n📊 APRÈS AJOUT DE 3 DOCUMENTS:")
    show_checklist(driver)
    
    # 5. Ajouter les documents restants
    print("\n📤 AJOUT DES DOCUMENTS RESTANTS:")
    remaining_docs = [
        ('vehicle_insurance', 'Assurance véhicule - MAIF'),
        ('vehicle_registration', 'Carte grise - Renault Clio'),
    ]
    
    for doc_type, title in remaining_docs:
        add_document(driver, doc_type, title)
    
    # 6. Afficher la checklist finale
    print("\n📊 APRÈS AJOUT DE TOUS LES DOCUMENTS:")
    show_checklist(driver)
    
    # 7. Vérifier les notifications créées
    from apps.notifications.models import Notification
    notifications = Notification.objects.filter(recipient__is_staff=True).order_by('-created_at')[:5]
    
    print("\n🔔 DERNIÈRES NOTIFICATIONS ADMIN:")
    for notif in notifications:
        print(f"   - {notif.title}: {notif.message[:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ")
    print("=" * 60)
    print(f"\n👤 Connectez-vous avec: chauffeur.test@pratik.fr / test1234")
    print(f"🔗 URL: http://127.0.0.1:8000/accounts/login/")

if __name__ == '__main__':
    main()
