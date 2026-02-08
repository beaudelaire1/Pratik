# ⚡ Démarrage Rapide - Pratik

## 🚀 Lancer la Plateforme

### Option 1: Double-clic (Windows)
```
Double-cliquez sur: start.bat
```

### Option 2: Ligne de commande
```bash
.venv\Scripts\activate
python manage.py runserver
```

Puis ouvrez: **http://localhost:8000**

---

## 🔑 Se Connecter

**Mot de passe pour TOUS les comptes:** `user1234`

### Comptes Disponibles

| Email | Type |
|-------|------|
| `etudiant1@pratik.gf` | 👨‍🎓 Étudiant |
| `ecole1@pratik.gf` | 🏫 École |
| `entreprise1@pratik.gf` | 🏢 Entreprise |
| `formation1@pratik.gf` | 📚 Formation |
| `recruteur1@pratik.gf` | 💼 Recruteur |
| `proprietaire1@pratik.gf` | 🏠 Propriétaire |
| `chauffeur1@pratik.gf` | 🚗 Chauffeur |
| `partenaire1@pratik.gf` | 🤝 Partenaire |
| `admin@pratik.gf` | 🔐 Admin |

---

## 🧪 Tester les Fonctionnalités

### Test École (Recommandé)
1. Connectez-vous avec `ecole1@pratik.gf`
2. Cliquez sur "Gérer les enseignants" → Voir les 2 enseignants
3. Cliquez sur "Gérer les élèves" → Voir l'élève inscrit
4. Cliquez sur "Ajouter un suivi" → Créer un suivi de stage

### Test Entreprise
1. Connectez-vous avec `entreprise1@pratik.gf`
2. Voir les 2 offres de stage publiées
3. Créer une nouvelle offre

### Test Étudiant
1. Connectez-vous avec `etudiant1@pratik.gf`
2. Consulter les offres de stage
3. Rechercher un logement
4. Trouver un covoiturage

---

## 🔄 Réinitialiser les Données

Si vous voulez recommencer avec des données fraîches:

```bash
.venv\Scripts\activate
python create_demo_data.py
```

⚠️ **Attention:** Supprime TOUTES les données!

---

## 📚 Plus d'Informations

- **Identifiants complets:** Voir `IDENTIFIANTS.md`
- **Guide détaillé:** Voir `COMPTES_DEMO.md`
- **Documentation:** Voir `README.md`

---

## ❓ Problèmes?

### Le serveur ne démarre pas
```bash
.venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

### Pas de données
```bash
python create_demo_data.py
```

### Erreur de connexion
- Vérifiez que vous utilisez le bon email
- Le mot de passe est: `user1234`
- Essayez avec `admin@pratik.gf`

---

**C'est tout! Bonne exploration! 🎉**
