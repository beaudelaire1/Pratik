# 🔑 Identifiants de Connexion - Plateforme Pratik

## 🌐 URL de la Plateforme
**http://localhost:8000**

---

## 👥 Tous les Comptes

### Mot de passe universel: `user1234`

---

## 📋 Liste des Comptes

| Type | Email | Nom | Fonctionnalités |
|------|-------|-----|-----------------|
| 👨‍🎓 **Étudiant** | `etudiant1@pratik.gf` | Jean Dupont | Consulter stages, postuler, logement, covoiturage |
| 🏫 **École** | `ecole1@pratik.gf` | Lycée Félix Éboué | Gérer enseignants, élèves, calendriers, suivis |
| 🏢 **Entreprise** | `entreprise1@pratik.gf` | Tech Guyane SARL | Publier stages, gérer candidatures |
| 📚 **Formation** | `formation1@pratik.gf` | Centre Formation Pro | Créer formations, gérer inscriptions |
| 💼 **Recruteur** | `recruteur1@pratik.gf` | Marie Talent | Publier offres, gérer entreprises |
| 🏠 **Propriétaire** | `proprietaire1@pratik.gf` | Pierre Logement | Publier logements (max 300€) |
| 🚗 **Chauffeur** | `chauffeur1@pratik.gf` | Paul Transport | Proposer trajets covoiturage |
| 🤝 **Partenaire** | `partenaire1@pratik.gf` | CTG Guyane | Créer événements, forums |

---

## 🔐 Compte Administrateur

- **Email:** `admin@pratik.gf`
- **Mot de passe:** `user1234`
- **URL:** http://localhost:8000/admin/

---

## 🚀 Connexion Rapide

1. Allez sur http://localhost:8000
2. Cliquez sur "Se connecter"
3. Entrez un email de la liste ci-dessus
4. Entrez le mot de passe: `user1234`
5. Cliquez sur "Connexion"

---

## 📊 Données Disponibles

- ✅ 2 offres de stage
- ✅ 2 offres de logement  
- ✅ 2 offres de covoiturage
- ✅ 2 formations
- ✅ 1 événement
- ✅ 2 enseignants
- ✅ 1 élève inscrit
- ✅ 1 calendrier de stage

---

## 🧪 Tests Recommandés

### Test 1: Parcours Étudiant
```
Email: etudiant1@pratik.gf
Mot de passe: user1234
```
- Consulter les offres de stage
- Rechercher un logement
- Trouver un covoiturage

### Test 2: Gestion École
```
Email: ecole1@pratik.gf
Mot de passe: user1234
```
- Gérer les enseignants (2 déjà créés)
- Gérer les élèves (1 déjà inscrit)
- Créer un suivi de stage

### Test 3: Gestion Entreprise
```
Email: entreprise1@pratik.gf
Mot de passe: user1234
```
- Voir les offres publiées (2)
- Créer une nouvelle offre
- Consulter les candidatures

---

## 🔄 Réinitialiser les Données

Pour recréer toutes les données:

```bash
.venv\Scripts\activate
python create_demo_data.py
```

⚠️ **Attention:** Supprime TOUTES les données existantes!

---

**Bonne exploration! 🎉**
