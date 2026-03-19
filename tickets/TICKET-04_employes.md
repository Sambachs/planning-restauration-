# TICKET-04 — Module Employés (CRUD)

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-04 |
| Module | `employees/` |
| Priorité | Haute |
| Statut | À faire |
| Dépendances | TICKET-02 |
| Fonctionnalités | F07, F08, F09, F10, F11 |
| Accès | Manager uniquement |

## Description

Espace de gestion des salariés. Le manager peut consulter, créer, modifier et désactiver des comptes employés. La suppression définitive n'est pas permise : on désactive uniquement.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F07 | Affichage de la liste de tous les employés |
| F08 | Création d'un nouvel employé |
| F09 | Modification des informations d'un employé |
| F10 | Désactivation d'un compte (sans suppression) |
| F11 | Recherche et filtrage par poste ou statut |

## Tâches

### 1. `employees/forms.py` — Formulaires

#### Formulaire `EmployeeForm` (création + édition)

| Champ | Type WTForms | Validation |
|---|---|---|
| nom | StringField | Obligatoire, max 50 |
| prenom | StringField | Obligatoire, max 50 |
| email | EmailField | Obligatoire, unique en BDD |
| password | PasswordField | Obligatoire à la création, optionnel à l'édition |
| telephone | StringField | Optionnel |
| post_id | SelectField | Obligatoire (liste des postes depuis BDD) |
| contrat | SelectField | Obligatoire (CDI / CDD / Extra / Apprenti) |
| date_embauche | DateField | Obligatoire |
| role | SelectField | Obligatoire (manager / employe) |

---

### 2. `employees/routes.py` — Routes

#### `GET /employees/` — Liste des employés (F07, F11)
- Récupérer tous les employés (actifs par défaut)
- Filtres via paramètres URL :
  - `?poste=<post_id>` — filtrer par poste
  - `?statut=actif|inactif|tous` — filtrer par statut
- Passer la liste des postes pour le menu de filtre

#### `GET/POST /employees/new` — Création (F08)
- GET : afficher le formulaire vide
- POST :
  1. Valider le formulaire
  2. Vérifier que l'email n'existe pas déjà
  3. Hacher le mot de passe avec bcrypt
  4. Créer et sauvegarder l'employé
  5. Flash message de succès → rediriger vers la liste

#### `GET /employees/<id>` — Fiche employé (F07)
- Afficher toutes les informations de l'employé
- Afficher ses 5 prochains créneaux
- Boutons : Modifier, Désactiver/Activer

#### `GET/POST /employees/<id>/edit` — Modification (F09)
- GET : formulaire prérempli avec les données actuelles
- POST :
  1. Valider le formulaire
  2. Si un nouveau mot de passe est fourni, le hacher et le mettre à jour
  3. Vérifier l'unicité de l'email si modifié
  4. Sauvegarder les modifications
  5. Flash message de succès → rediriger vers la fiche

#### `POST /employees/<id>/toggle` — Activation/Désactivation (F10)
- Basculer `actif` entre `True` et `False`
- Flash message adapté ("Employé désactivé" / "Employé réactivé")
- Rediriger vers la fiche

---

### 3. Templates

#### `templates/employees/list.html`
- Tableau avec colonnes : Nom, Prénom, Poste, Contrat, Statut, Actions
- Formulaire de filtre (poste + statut) en haut
- Badge coloré pour le statut (Actif / Inactif)
- Bouton « Ajouter un employé »

#### `templates/employees/form.html`
- Formulaire de création/édition (réutilisé pour les deux)
- Titre dynamique selon le contexte (Création / Modification)
- Messages d'erreur par champ

#### `templates/employees/detail.html`
- Fiche complète de l'employé
- Tableau des prochains créneaux
- Boutons d'action

---

## Critères de validation

- [ ] La liste affiche tous les employés avec filtrage fonctionnel
- [ ] La création d'un employé avec un email déjà existant est refusée avec message d'erreur
- [ ] Le mot de passe est stocké hashé (jamais en clair)
- [ ] La modification ne change pas le mot de passe si le champ est laissé vide
- [ ] La désactivation ne supprime pas l'employé de la BDD
- [ ] Un employé désactivé ne peut plus se connecter (vérifié dans TICKET-02)
- [ ] Toutes les routes sont inaccessibles à un employé (erreur 403)
