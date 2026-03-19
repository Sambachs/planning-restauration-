# TICKET-02 — Module Authentification

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-02 |
| Module | `auth/` |
| Priorité | Critique |
| Statut | À faire |
| Dépendances | TICKET-01 |
| Fonctionnalités | F01, F02, F03, F04, F05, F06 |

## Description

Mise en place du système de connexion/déconnexion sécurisé. Toutes les pages de l'application (sauf `/login`) nécessitent une session active. La redirection après connexion dépend du rôle de l'utilisateur.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F01 | Page de connexion avec champ email et mot de passe |
| F02 | Authentification sécurisée avec hachage bcrypt |
| F03 | Maintien de la connexion le temps de la session |
| F04 | Déconnexion manuelle |
| F05 | Redirection automatique selon le rôle |
| F06 | Protection des pages : accès refusé sans connexion |

## Tâches

### 1. `auth/forms.py` — Formulaire de connexion

Champs :
- `email` (EmailField) — obligatoire
- `password` (PasswordField) — obligatoire
- `submit` (SubmitField)
- Token CSRF automatique via Flask-WTF

---

### 2. `auth/routes.py` — Routes

#### `GET/POST /login`
- GET : afficher le formulaire de connexion
- POST :
  1. Valider le formulaire (CSRF + champs)
  2. Rechercher l'utilisateur par email
  3. Vérifier le mot de passe avec `check_password()`
  4. Vérifier que le compte est actif (`actif == True`)
  5. Créer la session avec `login_user()`
  6. Rediriger selon le rôle :
     - `manager` → `/dashboard`
     - `employe` → `/dashboard`
  7. En cas d'échec : afficher un message d'erreur générique (ne pas préciser si c'est l'email ou le mot de passe)

#### `GET /logout`
- Détruire la session avec `logout_user()`
- Rediriger vers `/login`

#### `load_user(user_id)`
- Fonction Flask-Login : récupérer l'utilisateur depuis la BDD par son ID

---

### 3. Décorateur `manager_required`

Créer un décorateur réutilisable dans `auth/` :
- Vérifie que l'utilisateur connecté a `role == 'manager'`
- Sinon : retourne une erreur 403

---

### 4. Template `templates/auth/login.html`

Éléments :
- Formulaire avec champs email et mot de passe
- Bouton de connexion
- Affichage des messages d'erreur Flask (`flash`)
- Design sobre et centré (héritage de `base.html`)

---

### 5. Template `templates/base.html`

Éléments communs à toutes les pages :
- Barre de navigation avec :
  - Logo / nom de l'application
  - Liens selon le rôle (Manager vs Employé)
  - Bouton de déconnexion
- Zone de contenu principale (`{% block content %}`)
- Affichage des messages flash (succès / erreur / info)

---

## Critères de validation

- [ ] Un utilisateur non connecté est redirigé vers `/login` pour toute page protégée
- [ ] La connexion avec des identifiants valides crée une session et redirige vers `/dashboard`
- [ ] La connexion avec des identifiants invalides affiche un message d'erreur sans révéler lequel est incorrect
- [ ] Un compte désactivé (`actif = False`) ne peut pas se connecter
- [ ] La déconnexion détruit la session et redirige vers `/login`
- [ ] Le token CSRF est présent et validé sur le formulaire POST
- [ ] Le décorateur `manager_required` retourne 403 pour un employé
