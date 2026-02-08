# Implémentation de la Hiérarchie École → Enseignants → Élèves

## Date: 8 février 2026

## Problème Résolu

**Avant:** Quand une école créait un suivi de stage, elle pouvait sélectionner n'importe quel utilisateur de type "student" dans toute la plateforme.

**Après:** Structure hiérarchique claire:
- Une école gère ses enseignants
- Chaque enseignant peut avoir des élèves assignés
- Le suivi de stage ne montre que les élèves inscrits dans l'école

## Nouveaux Modèles

### 1. Teacher (apps/users/models_school.py)
Représente un enseignant rattaché à une école.

**Champs:**
- `user` - OneToOneField vers CustomUser (optionnel pour l'instant)
- `school` - ForeignKey vers CustomUser (type 'school')
- `first_name`, `last_name` - Nom de l'enseignant
- `email`, `phone` - Contact
- `subjects` - Matières enseignées (TextField, séparées par virgules)
- `is_active` - Statut actif/inactif

**Relations:**
- Un enseignant appartient à une école
- Un enseignant peut avoir plusieurs élèves (via StudentSchoolEnrollment)
- Un enseignant peut suivre plusieurs stages (via InternshipTracking)

### 2. StudentSchoolEnrollment (apps/users/models_school.py)
Représente l'inscription d'un élève dans une école.

**Champs:**
- `student` - ForeignKey vers CustomUser (type 'student')
- `school` - ForeignKey vers CustomUser (type 'school')
- `teacher` - ForeignKey vers Teacher (enseignant référent, optionnel)
- `class_name` - Classe (ex: "L3 AES", "BTS 2ème année")
- `program` - Filière (ex: "Administration Économique et Sociale")
- `academic_year` - Année scolaire (ex: "2025-2026")
- `student_number` - Numéro étudiant
- `is_active` - Statut actif/inactif
- `enrollment_date` - Date d'inscription
- `graduation_date` - Date de fin prévue

**Contraintes:**
- Unique ensemble: (student, school, academic_year)
- Index sur (school, is_active) et (teacher, is_active)

## Modifications des Modèles Existants

### InternshipTracking (apps/tracking/models.py)
**Ajout:**
- `teacher` - ForeignKey vers Teacher (enseignant référent, optionnel)

Permet d'assigner un enseignant responsable du suivi de stage.

## Nouvelles Vues (apps/dashboard/views_school_management.py)

### Gestion des Enseignants
1. **TeacherListView** - Liste des enseignants avec nombre d'élèves
2. **TeacherCreateView** - Création d'un enseignant
3. **TeacherUpdateView** - Modification d'un enseignant
4. **TeacherDeleteView** - Suppression d'un enseignant

### Gestion des Élèves
1. **StudentListView** - Liste des élèves inscrits avec filtres
2. **StudentCreateView** - Inscription d'un élève
3. **StudentUpdateView** - Modification d'une inscription
4. **StudentDeleteView** - Suppression d'une inscription

**Filtres disponibles:**
- Recherche par nom/prénom/numéro étudiant
- Filtrage par enseignant
- Filtrage par classe

## Modifications des Vues Existantes

### InternshipTrackingCreateView & UpdateView
**Changements:**
- Ajout du champ `teacher` dans les formulaires
- Limitation du champ `student` aux élèves inscrits dans l'école (via StudentSchoolEnrollment)
- Limitation du champ `teacher` aux enseignants de l'école
- Utilisation de `get_form()` pour filtrer les querysets

**Code clé:**
```python
def get_form(self, form_class=None):
    form = super().get_form(form_class)
    # Limiter aux élèves inscrits
    enrolled_students = StudentSchoolEnrollment.objects.filter(
        school=self.request.user,
        is_active=True
    ).values_list('student_id', flat=True)
    form.fields['student'].queryset = CustomUser.objects.filter(
        id__in=enrolled_students
    )
    # Limiter aux enseignants de l'école
    form.fields['teacher'].queryset = Teacher.objects.filter(
        school=self.request.user,
        is_active=True
    )
    return form
```

## Nouvelles Routes (apps/dashboard/urls.py)

### Enseignants
- `/dashboard/school/teachers/` - Liste
- `/dashboard/school/teachers/create/` - Création
- `/dashboard/school/teachers/<pk>/edit/` - Modification
- `/dashboard/school/teachers/<pk>/delete/` - Suppression

### Élèves
- `/dashboard/school/students/` - Liste
- `/dashboard/school/students/create/` - Inscription
- `/dashboard/school/students/<pk>/edit/` - Modification
- `/dashboard/school/students/<pk>/delete/` - Suppression

## Nouveaux Templates

### Enseignants (templates/dashboard/school/)
1. `teacher_list.html` - Tableau des enseignants avec actions
2. `teacher_form.html` - Formulaire création/modification
3. `teacher_confirm_delete.html` - Confirmation de suppression

### Élèves (templates/dashboard/school/)
1. `student_list.html` - Tableau des élèves avec filtres
2. `student_form.html` - Formulaire inscription/modification
3. `student_confirm_delete.html` - Confirmation de suppression

## Mise à Jour du Dashboard École

**Nouvelles actions rapides:**
- 👨‍🏫 Gérer les enseignants
- 👨‍🎓 Gérer les élèves
- 📅 Publier un calendrier
- 📋 Gérer les calendriers
- 📝 Ajouter un suivi
- 👁️ Suivis de stages

## Migrations

### users.0006_teacher_studentschoolenrollment
- Création de la table Teacher
- Création de la table StudentSchoolEnrollment
- Contraintes et index

### tracking.0005_internshiptracking_teacher
- Ajout du champ teacher à InternshipTracking

## Workflow Complet

### 1. Configuration Initiale (École)
1. L'école se connecte à son dashboard
2. Clique sur "Gérer les enseignants"
3. Ajoute ses enseignants (nom, email, matières)

### 2. Inscription des Élèves (École)
1. Clique sur "Gérer les élèves"
2. Inscrit un élève en sélectionnant:
   - L'étudiant (parmi les utilisateurs de type 'student')
   - L'enseignant référent (optionnel)
   - La classe et la filière
   - L'année scolaire
   - Le numéro étudiant

### 3. Création d'un Suivi de Stage (École)
1. Clique sur "Ajouter un suivi"
2. Sélectionne un élève **uniquement parmi les élèves inscrits**
3. Sélectionne un enseignant référent (optionnel)
4. Remplit les informations du stage
5. Le système associe automatiquement l'école

### 4. Consultation (École/Enseignant)
- L'école voit tous les suivis de ses élèves
- Peut filtrer par enseignant
- Peut voir la progression de chaque stage

## Sécurité et Validation

✅ **Isolation des données:**
- Une école ne voit que ses enseignants
- Une école ne voit que ses élèves inscrits
- Les suivis de stage sont limités aux élèves de l'école

✅ **Contraintes d'intégrité:**
- Un élève ne peut être inscrit qu'une fois par année scolaire dans une école
- Les enseignants sont uniques par école (via user)

✅ **Validation des formulaires:**
- Les querysets sont filtrés dans get_form()
- Impossible de sélectionner un élève non inscrit
- Impossible de sélectionner un enseignant d'une autre école

## Améliorations Futures (Optionnel)

1. **Compte utilisateur pour les enseignants:**
   - Créer automatiquement un compte CustomUser pour chaque enseignant
   - Permettre aux enseignants de se connecter
   - Dashboard enseignant pour voir leurs élèves

2. **Notifications:**
   - Notifier l'enseignant quand un de ses élèves commence un stage
   - Rappels pour les évaluations mi-parcours et finales

3. **Statistiques:**
   - Taux de réussite par enseignant
   - Nombre de stages par classe
   - Durée moyenne des stages

4. **Export:**
   - Export Excel de la liste des élèves
   - Export PDF des conventions de stage
   - Rapports de suivi par enseignant

## Fichiers Créés/Modifiés

### Nouveaux Fichiers (10)
- `apps/users/models_school.py` - Modèles Teacher et StudentSchoolEnrollment
- `apps/dashboard/views_school_management.py` - Vues CRUD pour enseignants et élèves
- `templates/dashboard/school/teacher_list.html`
- `templates/dashboard/school/teacher_form.html`
- `templates/dashboard/school/teacher_confirm_delete.html`
- `templates/dashboard/school/student_list.html`
- `templates/dashboard/school/student_form.html`
- `templates/dashboard/school/student_confirm_delete.html`
- `apps/users/migrations/0006_teacher_studentschoolenrollment.py`
- `apps/tracking/migrations/0005_internshiptracking_teacher.py`

### Fichiers Modifiés (5)
- `apps/tracking/models.py` - Ajout du champ teacher
- `apps/dashboard/views_school.py` - Filtrage des élèves et enseignants
- `apps/dashboard/urls.py` - Ajout des routes
- `templates/dashboard/school_dashboard.html` - Nouvelles actions rapides
- `apps/users/__init__.py` - Import des modèles

## Tests Effectués

✅ `python manage.py check` - Aucune erreur
✅ `python manage.py makemigrations` - Migrations créées
✅ `python manage.py migrate` - Migrations appliquées

## Résumé

La hiérarchie École → Enseignants → Élèves est maintenant complètement implémentée. Les écoles peuvent:
1. Gérer leurs enseignants
2. Inscrire leurs élèves avec un enseignant référent
3. Créer des suivis de stage uniquement pour leurs élèves inscrits
4. Assigner un enseignant responsable à chaque suivi

Cette structure garantit l'isolation des données et une gestion cohérente des relations entre les différents acteurs.
