# Commandes Utiles - Plateforme PRATIK

**Guide de référence rapide pour les commandes courantes**

---

## 🚀 Démarrage

### Installation Initiale
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### Lancer les Services (Développement)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Celery Worker:**
```bash
celery -A config worker -l info
```

**Terminal 3 - Celery Beat:**
```bash
celery -A config beat -l info
```

**Terminal 4 - Serveur Django:**
```bash
python manage.py runserver
```

---

## 🗄️ Base de Données

### Migrations
```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir l'état des migrations
python manage.py showmigrations

# Annuler une migration
python manage.py migrate app_name migration_name

# Réinitialiser toutes les migrations (ATTENTION!)
python manage.py migrate --run-syncdb
```

### Gestion des Données
```bash
# Créer des données de test
python manage.py shell
>>> from create_test_data import create_test_data
>>> create_test_data()

# Exporter des données
python manage.py dumpdata app_name > data.json

# Importer des données
python manage.py loaddata data.json

# Vider la base de données
python manage.py flush
```

---

## 🧪 Tests

### Exécuter les Tests
```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=apps --cov=core --cov=api

# Tests avec rapport HTML
pytest --cov=apps --cov=core --cov=api --cov-report=html

# Test spécifique
pytest tests/test_recommendation_models.py

# Tests en parallèle
pytest -n auto

# Tests avec sortie détaillée
pytest -v

# Tests avec arrêt au premier échec
pytest -x
```

### Couverture de Code
```bash
# Générer un rapport de couverture
coverage run -m pytest
coverage report
coverage html

# Ouvrir le rapport HTML
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux
```

---

## 🔧 Django Management

### Shell Django
```bash
# Ouvrir le shell Django
python manage.py shell

# Ouvrir le shell avec IPython
python manage.py shell -i ipython
```

### Exemples dans le Shell
```python
# Importer les modèles
from apps.users.models import CustomUser
from apps.recommendations.models import InternRecommendation

# Créer un utilisateur
user = CustomUser.objects.create_user(
    username='test',
    email='test@example.com',
    password='password123',
    user_type='STUDENT'
)

# Requêtes
users = CustomUser.objects.filter(user_type='COMPANY')
recommendations = InternRecommendation.objects.filter(rating=5)

# Compter
CustomUser.objects.count()
InternRecommendation.objects.filter(is_public=True).count()
```

---

## 📊 Celery

### Gestion des Workers
```bash
# Démarrer un worker
celery -A config worker -l info

# Démarrer avec plusieurs workers
celery -A config worker -l info --concurrency=4

# Démarrer beat (tâches périodiques)
celery -A config beat -l info

# Démarrer worker + beat ensemble
celery -A config worker -B -l info

# Voir les tâches actives
celery -A config inspect active

# Voir les tâches enregistrées
celery -A config inspect registered

# Purger toutes les tâches
celery -A config purge
```

### Tester les Tâches
```python
# Dans le shell Django
from core.tasks.notification_tasks import send_evolution_notifications

# Exécuter immédiatement (synchrone)
send_evolution_notifications()

# Exécuter en arrière-plan (asynchrone)
send_evolution_notifications.delay()

# Exécuter avec délai
send_evolution_notifications.apply_async(countdown=60)  # Dans 60 secondes
```

---

## 🔍 Débogage

### Logs Django
```bash
# Voir les logs en temps réel
tail -f logs/pratik.log

# Chercher dans les logs
grep "ERROR" logs/pratik.log
```

### Vérifications
```bash
# Vérifier la configuration
python manage.py check

# Vérifier pour la production
python manage.py check --deploy

# Vérifier les migrations
python manage.py makemigrations --check --dry-run

# Voir les requêtes SQL
python manage.py shell
>>> from django.db import connection
>>> connection.queries
```

---

## 🌐 API

### Tester l'API avec cURL

**Obtenir un token:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password123"}'
```

**Utiliser le token:**
```bash
curl -X GET http://localhost:8000/api/evolution/tracked/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Créer une recommandation:**
```bash
curl -X POST http://localhost:8000/api/recommendations/create/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "internship": 1,
    "rating": 5,
    "autonomy": 5,
    "teamwork": 4,
    "rigor": 5,
    "creativity": 4,
    "punctuality": 5,
    "comment": "Excellent!"
  }'
```

### Tester l'API avec Python
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Obtenir un token
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "user@example.com",
    "password": "password123"
})
token = response.json()["access"]

# Utiliser le token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/evolution/tracked/", headers=headers)
print(response.json())
```

---

## 📦 Dépendances

### Gestion des Packages
```bash
# Installer un nouveau package
pip install package_name

# Mettre à jour requirements.txt
pip freeze > requirements.txt

# Installer depuis requirements.txt
pip install -r requirements.txt

# Mettre à jour un package
pip install --upgrade package_name

# Désinstaller un package
pip uninstall package_name

# Lister les packages installés
pip list

# Voir les packages obsolètes
pip list --outdated
```

---

## 🔐 Sécurité

### Générer une Clé Secrète
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Changer le Mot de Passe d'un Utilisateur
```bash
python manage.py changepassword username
```

### Créer un Superutilisateur
```bash
python manage.py createsuperuser
```

---

## 🚢 Déploiement

### Préparation
```bash
# Vérifier la configuration de production
python manage.py check --deploy

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Avec Gunicorn
```bash
# Installer Gunicorn
pip install gunicorn

# Lancer Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Avec workers
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# En arrière-plan
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --daemon
```

---

## 🧹 Maintenance

### Nettoyage
```bash
# Supprimer les fichiers .pyc
find . -type f -name "*.pyc" -delete

# Supprimer les dossiers __pycache__
find . -type d -name "__pycache__" -delete

# Supprimer les migrations (ATTENTION!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Nettoyer les sessions expirées
python manage.py clearsessions
```

### Optimisation
```bash
# Optimiser la base de données (SQLite)
python manage.py shell
>>> from django.db import connection
>>> connection.cursor().execute("VACUUM")

# Analyser les requêtes lentes
python manage.py shell
>>> from django.db import connection
>>> from django.db import reset_queries
>>> reset_queries()
>>> # Exécuter vos requêtes
>>> print(connection.queries)
```

---

## 📝 Utilitaires

### Créer une Nouvelle App
```bash
python manage.py startapp app_name
```

### Créer un Fichier de Migration Vide
```bash
python manage.py makemigrations --empty app_name
```

### Voir le SQL d'une Migration
```bash
python manage.py sqlmigrate app_name migration_number
```

### Créer un Dump de la Base de Données
```bash
# SQLite
sqlite3 db.sqlite3 .dump > backup.sql

# PostgreSQL
pg_dump dbname > backup.sql
```

---

## 🔗 Liens Utiles

### Accès Local
- **Site:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/
- **API Docs:** http://localhost:8000/api/docs/ (après config Swagger)

### Documentation
- **Django:** https://docs.djangoproject.com/
- **DRF:** https://www.django-rest-framework.org/
- **Celery:** https://docs.celeryproject.org/
- **Pytest:** https://docs.pytest.org/

---

## 💡 Astuces

### Raccourcis Shell
```bash
# Alias utiles (ajouter à .bashrc ou .zshrc)
alias dj="python manage.py"
alias djrun="python manage.py runserver"
alias djmig="python manage.py migrate"
alias djmake="python manage.py makemigrations"
alias djshell="python manage.py shell"
alias djtest="pytest"
```

### Variables d'Environnement
```bash
# Windows
set DEBUG=True
set SECRET_KEY=your-secret-key

# Linux/Mac
export DEBUG=True
export SECRET_KEY=your-secret-key
```

---

**Dernière Mise à Jour:** 8 février 2026  
**Version:** 1.0
