# 🎯 Comptes de Démonstration - Plateforme Pratik

## 🌐 Accès à la Plateforme
**URL:** http://localhost:8000

---

## 👥 Comptes Utilisateurs

Tous les comptes utilisent le même mot de passe: **`user1234`**

### 1. 👨‍🎓 Étudiant
- **Email:** etudiant1@pratik.gf
- **Nom:** Jean Dupont
- **Profil:** Licence 3 AES, Université de Guyane
- **Fonctionnalités:**
  - Consulter les offres de stage
  - Postuler aux stages
  - Rechercher un logement
  - Trouver du covoiturage
  - Accéder aux formations

### 2. 🏫 École
- **Email:** ecole1@pratik.gf
- **Nom:** Lycée Félix Éboué
- **Fonctionnalités:**
  - Gérer les enseignants (2 enseignants créés)
  - Gérer les élèves (1 élève inscrit: Jean Dupont)
  - Publier des calendriers de stage (1 calendrier créé)
  - Effectuer le suivi des stages
  - Assigner des enseignants référents

### 3. 🏢 Entreprise
- **Email:** entreprise1@pratik.gf
- **Nom:** Tech Guyane SARL
- **Fonctionnalités:**
  - Publier des offres de stage (2 offres créées)
  - Gérer les candidatures
  - Consulter les calendriers des écoles
  - Suivre l'évolution des stagiaires

### 4. 📚 Centre de Formation
- **Email:** formation1@pratik.gf
- **Nom:** Centre de Formation Professionnelle de Guyane
- **Fonctionnalités:**
  - Créer et gérer des formations (2 formations créées)
  - Gérer les inscriptions
  - Publier des contenus pédagogiques

### 5. 💼 Recruteur
- **Email:** recruteur1@pratik.gf
- **Nom:** Marie Talent (Talents Guyane)
- **Fonctionnalités:**
  - Publier des offres de stage
  - Gérer plusieurs entreprises
  - Consulter les profils étudiants

### 6. 🏠 Propriétaire
- **Email:** proprietaire1@pratik.gf
- **Nom:** Pierre Logement
- **Statut:** ✅ Vérifié
- **Fonctionnalités:**
  - Publier des offres de logement (2 offres créées)
  - Gérer les candidatures
  - Maximum 300€/mois (protection étudiants)

### 7. 🚗 Chauffeur
- **Email:** chauffeur1@pratik.gf
- **Nom:** Paul Transport
- **Statut:** ✅ Vérifié
- **Véhicule:** Renault Clio 2020 (Bleu)
- **Fonctionnalités:**
  - Proposer des trajets (2 trajets créés)
  - Gérer les réservations
  - 3 places disponibles

### 8. 🤝 Partenaire
- **Email:** partenaire1@pratik.gf
- **Nom:** Collectivité Territoriale de Guyane
- **Fonctionnalités:**
  - Créer des événements (1 événement créé)
  - Organiser des forums
  - Visibilité sur la carte des partenaires

---

## 🔐 Compte Administrateur

- **Email:** admin@pratik.gf
- **Mot de passe:** user1234
- **URL Admin:** http://localhost:8000/admin/
- **Accès complet** à toutes les fonctionnalités d'administration

---

## 📊 Données Créées

### Offres de Stage (2)
1. **Stage Développeur Web Junior**
   - Entreprise: Tech Guyane SARL
   - Durée: 3 mois
   - Gratification: 600€/mois
   - Lieu: Cayenne

2. **Assistant Marketing Digital**
   - Entreprise: Tech Guyane SARL
   - Durée: 6 mois
   - Lieu: Cayenne

### Offres de Logement (2)
1. **Studio meublé proche université**
   - Type: Studio
   - Prix: 280€/mois
   - Lieu: Cayenne Centre
   - Propriétaire: Pierre Logement

2. **Chambre chez l'habitant**
   - Type: Chambre
   - Prix: 250€/mois
   - Lieu: Rémire-Montjoly
   - Propriétaire: Pierre Logement

### Offres de Covoiturage (2)
1. **Cayenne → Saint-Laurent-du-Maroni**
   - Date: Demain 7h00
   - Places: 3
   - Prix: 45€/personne
   - Chauffeur: Paul Transport

2. **Cayenne → Kourou**
   - Date: Dans 7 jours à 14h30
   - Places: 2
   - Prix: 15€/personne
   - Chauffeur: Paul Transport

### Formations (2)
1. **Initiation au Développement Web**
   - Niveau: Débutant
   - Durée: 40 heures
   - Formateur: Thomas Bernard

2. **Gestion de Projet Agile**
   - Niveau: Intermédiaire
   - Durée: 24 heures
   - Formatrice: Sophie Martin

### Événements (1)
1. **Forum de l'Emploi et des Stages**
   - Date: Dans 30 jours
   - Horaire: 9h00 - 17h00
   - Lieu: Palais des Congrès de Cayenne
   - Organisateur: CTG

### Hiérarchie École
- **École:** Lycée Félix Éboué
- **Enseignants:** 2
  - Sophie Martin (Économie, Gestion)
  - Thomas Bernard (Informatique, Mathématiques)
- **Élèves inscrits:** 1
  - Jean Dupont (Terminale STMG)
- **Calendrier de stage:** 1
  - Terminale STMG (30 jours → 90 jours)

---

## 🧪 Scénarios de Test

### Scénario 1: Parcours Étudiant
1. Se connecter avec `etudiant1@pratik.gf`
2. Consulter les offres de stage
3. Postuler à une offre
4. Rechercher un logement
5. Réserver un covoiturage

### Scénario 2: Gestion École
1. Se connecter avec `ecole1@pratik.gf`
2. Consulter les enseignants
3. Voir les élèves inscrits
4. Créer un suivi de stage pour Jean Dupont
5. Publier un nouveau calendrier

### Scénario 3: Gestion Entreprise
1. Se connecter avec `entreprise1@pratik.gf`
2. Consulter les offres publiées
3. Voir les candidatures reçues
4. Créer une nouvelle offre de stage
5. Consulter les calendriers des écoles

### Scénario 4: Gestion Logement
1. Se connecter avec `proprietaire1@pratik.gf`
2. Consulter les offres de logement
3. Voir les candidatures
4. Créer une nouvelle offre (max 300€)
5. Modifier une offre existante

### Scénario 5: Gestion Covoiturage
1. Se connecter avec `chauffeur1@pratik.gf`
2. Consulter les trajets proposés
3. Créer un nouveau trajet
4. Modifier un trajet existant

### Scénario 6: Gestion Formation
1. Se connecter avec `formation1@pratik.gf`
2. Consulter les formations
3. Créer une nouvelle formation
4. Modifier une formation existante

---

## 🔄 Réinitialiser les Données

Pour recréer les données de démonstration:

```bash
.venv\Scripts\activate
python create_demo_data.py
```

**⚠️ Attention:** Cette commande supprime TOUTES les données existantes!

---

## 📝 Notes Importantes

1. **Vérification requise:**
   - Les propriétaires doivent être vérifiés pour publier des logements
   - Les chauffeurs doivent être vérifiés pour proposer du covoiturage
   - Les comptes demo sont déjà vérifiés

2. **Limite de prix:**
   - Les logements sont limités à 300€/mois maximum
   - Protection contre la vie chère en Guyane

3. **Hiérarchie école:**
   - Une école gère ses enseignants
   - Les enseignants ont des élèves assignés
   - Les suivis de stage ne montrent que les élèves inscrits

4. **Données réalistes:**
   - Toutes les adresses sont en Guyane
   - Les prix sont adaptés au contexte local
   - Les formations sont pertinentes pour le territoire

---

## 🚀 Démarrer le Serveur

```bash
.venv\Scripts\activate
python manage.py runserver
```

Puis accédez à: http://localhost:8000

---

**Bonne exploration de la plateforme Pratik! 🎉**
