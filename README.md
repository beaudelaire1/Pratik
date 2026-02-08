# 🎓 Pratik - Plateforme d'Accompagnement des Étudiants en Guyane

Plateforme web complète pour faciliter l'insertion professionnelle et l'accompagnement des étudiants en Guyane française.

---

## 🌟 Fonctionnalités Principales

### Pour les Étudiants
- 🔍 Recherche d'offres de stage
- 📝 Candidatures en ligne
- 🏠 Recherche de logement (max 300€/mois)
- 🚗 Covoiturage entre étudiants
- 📚 Accès aux formations en ligne
- 📊 Suivi de progression

### Pour les Écoles
- 👨‍🏫 Gestion des enseignants
- 👨‍🎓 Gestion des élèves/inscriptions
- 📅 Publication de calendriers de stage
- 📈 Suivi numérique des stages
- 📋 Évaluations mi-parcours et finales
- 📄 Gestion des conventions

### Pour les Entreprises
- 💼 Publication d'offres de stage
- 📬 Gestion des candidatures
- 🤝 Statut partenaire
- 📊 Suivi des stagiaires

### Pour les Autres Acteurs
- 📚 **Centres de Formation:** Gestion des formations
- 💼 **Recruteurs:** Multi-entreprises
- 🏠 **Propriétaires:** Offres de logement
- 🚗 **Chauffeurs:** Covoiturage
- 🤝 **Partenaires:** Événements et forums

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- SQLite (inclus)
- Node.js (pour Tailwind CSS)

### Installation

```bash
# 1. Cloner le projet
git clone https://github.com/beaudelaire1/Pratik.git
cd Pratik

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer les données de démonstration
python create_demo_data.py

# 6. Lancer le serveur
python manage.py runserver
```

### Accès
- **Plateforme:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/

---

## 🔑 Identifiants de Test

**Mot de passe universel:** `user1234`

| Type | Email |
|------|-------|
| Étudiant | `etudiant1@pratik.gf` |
| École | `ecole1@pratik.gf` |
| Entreprise | `entreprise1@pratik.gf` |
| Formation | `formation1@pratik.gf` |
| Recruteur | `recruteur1@pratik.gf` |
| Propriétaire | `proprietaire1@pratik.gf` |
| Chauffeur | `chauffeur1@pratik.gf` |
| Partenaire | `partenaire1@pratik.gf` |
| **Admin** | `admin@pratik.gf` |

📄 Voir [IDENTIFIANTS.md](IDENTIFIANTS.md) pour plus de détails

---

## 📁 Structure du Projet

```
Pratik/
├── apps/                      # Applications Django
│   ├── users/                 # Gestion des utilisateurs
│   ├── internships/           # Offres de stage
│   ├── services/              # Logement, covoiturage
│   ├── calendars/             # Calendriers de stage
│   ├── tracking/              # Suivi des stages
│   ├── hub/                   # Formations
│   ├── events/                # Événements
│   ├── partners/              # Partenaires
│   └── ...
├── api/                       # API REST
├── core/                      # Services métier
├── templates/                 # Templates HTML
├── static/                    # Fichiers statiques
├── config/                    # Configuration Django
├── docs/                      # Documentation
└── create_demo_data.py        # Script de données de test
```

---

## 🏗️ Architecture

### Backend
- **Framework:** Django 5.2
- **Base de données:** SQLite (dev) / PostgreSQL (prod)
- **API:** Django REST Framework
- **Tâches asynchrones:** Celery + Redis
- **Documentation API:** drf-yasg (Swagger)

### Frontend
- **CSS:** Tailwind CSS
- **JavaScript:** Vanilla JS + HTMX
- **Templates:** Django Templates

### Fonctionnalités Techniques
- ✅ 8 types d'utilisateurs avec profils dédiés
- ✅ Hiérarchie École → Enseignants → Élèves
- ✅ CRUD complet pour tous les dashboards
- ✅ API REST complète
- ✅ Système de notifications
- ✅ Vérification des utilisateurs (propriétaires, chauffeurs)
- ✅ Limite de prix logement (300€ max)
- ✅ Isolation des données par école

---

## 📚 Documentation

- [IDENTIFIANTS.md](IDENTIFIANTS.md) - Comptes de test
- [COMPTES_DEMO.md](COMPTES_DEMO.md) - Guide complet des comptes
- [API_QUICK_START.md](API_QUICK_START.md) - Documentation API
- [docs/](docs/) - Documentation technique complète

---

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Tests avec couverture
pytest --cov=apps --cov-report=html

# Vérifier le code
python manage.py check
```

---

## 🔧 Commandes Utiles

```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Lancer Celery (tâches asynchrones)
celery -A config worker -l info

# Lancer Celery Beat (tâches planifiées)
celery -A config beat -l info
```

---

## 🌍 Déploiement

### Variables d'Environnement

Créer un fichier `.env`:

```env
DEBUG=False
SECRET_KEY=votre-clé-secrète
ALLOWED_HOSTS=pratik.gf,www.pratik.gf
DATABASE_URL=postgres://user:pass@host:5432/pratik
REDIS_URL=redis://localhost:6379/0
```

### Production

```bash
# Installer les dépendances de production
pip install -r requirements-prod.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer avec Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 🤝 Contribution

Les contributions sont les bienvenues!

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Équipe

Développé pour faciliter l'insertion professionnelle des étudiants en Guyane française.

---

## 📞 Support

Pour toute question ou problème:
- 📧 Email: contact@pratik.gf
- 🐛 Issues: [GitHub Issues](https://github.com/beaudelaire1/Pratik/issues)

---

## 🎯 Roadmap

- [ ] Application mobile (React Native)
- [ ] Système de messagerie interne
- [ ] Notifications push
- [ ] Intégration avec France Travail
- [ ] Export PDF des conventions
- [ ] Statistiques avancées
- [ ] Multi-langue (FR/EN)

---

**Fait avec ❤️ pour les étudiants de Guyane**
