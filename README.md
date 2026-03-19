# Application de Gestion de Planning — Restauration

Projet universitaire — Licence G&M 3ème année
Matière : Développement d'Application de Gestion
Année universitaire 2025–2026

---

## Présentation

Application web de gestion de planning destinée aux établissements de restauration. Elle permet de centraliser la gestion des employés, l'affectation des créneaux horaires, le suivi des absences et congés, ainsi que la visualisation du planning hebdomadaire et mensuel.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Langage backend | Python 3.x |
| Framework web | Flask 2.3 + Blueprints |
| Base de données | SQLite + SQLAlchemy |
| Templates | Jinja2 |
| Frontend | HTML / CSS / JavaScript |
| Authentification | Flask-Login |
| Hachage mots de passe | Flask-Bcrypt (bcrypt) |
| Formulaires | Flask-WTF + WTForms |

---

## Prérequis

- Python 3.10+
- pip

---

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd planning_restauration
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Initialiser la base de données

```bash
python init_db.py
```

Cette commande crée `planning.db` et insère :
- Les 5 postes par défaut (Serveur, Cuisinier, Hôte/Hôtesse, Bar, Caisse)
- Un compte manager de test
- 6 employés mock avec des créneaux sur la semaine en cours
- 4 absences de démonstration

### 5. Lancer le serveur

```bash
python run.py
```

L'application est accessible à l'adresse : **http://localhost:5000**

---

## Comptes de test

| Rôle | Email | Mot de passe |
|---|---|---|
| Manager | `admin@restaurant.fr` | `Admin1234` |
| Employé | `sophie.martin@restaurant.fr` | `Employe1234` |
| Employé | `lucas.bernard@restaurant.fr` | `Employe1234` |
| Employé | `emma.leroy@restaurant.fr` | `Employe1234` |
| Employé | `thomas.moreau@restaurant.fr` | `Employe1234` |
| Employé | `camille.petit@restaurant.fr` | `Employe1234` |
| Employé | `hugo.garnier@restaurant.fr` | `Employe1234` |

---

## Structure du projet

```
planning_restauration/
├── app/
│   ├── __init__.py          # Factory Flask, init extensions, blueprints
│   ├── models.py            # Modèles SQLAlchemy (User, Post, Shift, Absence)
│   ├── auth/                # Authentification (login, logout, décorateur manager)
│   ├── main/                # Dashboard (manager et employé)
│   ├── employees/           # CRUD employés
│   ├── shifts/              # Gestion des créneaux horaires
│   ├── absences/            # Congés et absences
│   ├── planning/            # Vue calendrier semaine/mois
│   ├── templates/           # Templates Jinja2
│   └── static/              # CSS et JavaScript
├── tickets/                 # Spécifications par feature
├── config.py                # Configuration Flask
├── run.py                   # Point d'entrée
├── init_db.py               # Script d'initialisation BDD
├── requirements.txt         # Dépendances Python
├── planning.db              # Base de données SQLite (générée)
├── COMPTES_TEST.md          # Identifiants de test
├── Cahier_des_Charges_Planning_Restauration.pdf
└── Document_de_Conception_Planning_Restauration.pdf
```

---

## Fonctionnalités

### Rôle Manager
- Tableau de bord avec résumé (employés, créneaux, demandes en attente)
- Gestion des employés : création, modification, désactivation
- Affectation de créneaux horaires avec détection de conflits
- Duplication de créneaux sur une plage de dates
- Traitement des demandes de congés (approbation / refus)
- Saisie d'absences imprévues (maladie, injustifiée)
- Vue planning hebdomadaire et mensuelle avec filtres

### Rôle Employé
- Tableau de bord avec son planning de la semaine
- Consultation de son planning (semaine / mois)
- Soumission et annulation de demandes de congés
- Suivi du statut de ses demandes

---

## Base de données

```
users ────┐
          ├── shifts (user_id, created_by)
          ├── absences (user_id, traite_par)
posts ────┤
          ├── users (post_id)
          └── shifts (post_id)
```

---

## Sécurité

- Mots de passe hachés avec **bcrypt**
- Protection **CSRF** sur tous les formulaires POST (Flask-WTF)
- Routes protégées par `@login_required`
- Routes manager protégées par `@manager_required`
- Isolation des données : un employé n'accède qu'à ses propres informations

---

## Réinitialiser la base de données

```bash
rm planning.db
python init_db.py
```
