# TICKET-01 — Modèles de base de données

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-01 |
| Module | `models.py` |
| Priorité | Critique |
| Statut | À faire |
| Dépendances | TICKET-00 |

## Description

Définition de tous les modèles SQLAlchemy correspondant aux 4 tables de la base de données, ainsi que le script d'initialisation qui crée la BDD, insère les postes par défaut et crée un compte manager de test.

## Tâches

### 1. Modèle `Post` — table `posts`

| Colonne | Type | Contraintes |
|---|---|---|
| id | Integer | PK, Autoincrement |
| nom | String(50) | NOT NULL, UNIQUE |
| couleur | String(7) | NOT NULL (code HEX ex: `#FF5722`) |
| description | Text | NULLABLE |

Postes à insérer au démarrage : **Serveur**, **Cuisinier**, **Hôte/Hôtesse**, **Bar**, **Caisse**

Couleurs suggérées :
- Serveur → `#2196F3` (bleu)
- Cuisinier → `#FF5722` (orange)
- Hôte/Hôtesse → `#9C27B0` (violet)
- Bar → `#4CAF50` (vert)
- Caisse → `#FFC107` (jaune)

---

### 2. Modèle `User` — table `users`

| Colonne | Type | Contraintes |
|---|---|---|
| id | Integer | PK, Autoincrement |
| nom | String(50) | NOT NULL |
| prenom | String(50) | NOT NULL |
| email | String(120) | NOT NULL, UNIQUE |
| password_hash | String(255) | NOT NULL |
| telephone | String(20) | NULLABLE |
| post_id | Integer | FK → posts.id, NULLABLE |
| contrat | String(20) | NOT NULL (CDI / CDD / Extra / Apprenti) |
| date_embauche | Date | NOT NULL |
| role | String(10) | NOT NULL, DEFAULT 'employe' |
| actif | Boolean | NOT NULL, DEFAULT True |
| created_at | DateTime | NOT NULL, DEFAULT now() |

Méthodes à implémenter sur le modèle :
- `set_password(password)` — hache et stocke le mot de passe
- `check_password(password)` — vérifie le mot de passe
- Implémenter l'interface `UserMixin` de Flask-Login

---

### 3. Modèle `Shift` — table `shifts`

| Colonne | Type | Contraintes |
|---|---|---|
| id | Integer | PK, Autoincrement |
| user_id | Integer | NOT NULL, FK → users.id |
| post_id | Integer | NOT NULL, FK → posts.id |
| date_service | Date | NOT NULL |
| heure_debut | Time | NOT NULL |
| heure_fin | Time | NOT NULL |
| note | Text | NULLABLE |
| created_at | DateTime | NOT NULL, DEFAULT now() |
| created_by | Integer | FK → users.id, NULLABLE |

> **Contrainte métier :** deux créneaux d'un même employé ne peuvent pas se chevaucher sur la même journée. Cette vérification est faite côté serveur dans TICKET-05.

---

### 4. Modèle `Absence` — table `absences`

| Colonne | Type | Contraintes |
|---|---|---|
| id | Integer | PK, Autoincrement |
| user_id | Integer | NOT NULL, FK → users.id |
| type_absence | String(30) | NOT NULL (`conge_paye` / `sans_solde` / `maladie` / `injustifie`) |
| date_debut | Date | NOT NULL |
| date_fin | Date | NOT NULL |
| motif | Text | NULLABLE |
| statut | String(15) | NOT NULL, DEFAULT `en_attente` (`en_attente` / `approuve` / `refuse`) |
| commentaire_manager | Text | NULLABLE |
| traite_par | Integer | FK → users.id, NULLABLE |
| created_at | DateTime | NOT NULL, DEFAULT now() |

---

### 5. Script d'initialisation `init_db.py`

- Créer toutes les tables (`db.create_all()`)
- Insérer les 5 postes par défaut si absents
- Créer un compte manager de test :
  - Email : `admin@restaurant.fr`
  - Mot de passe : `Admin1234`
  - Rôle : `manager`

---

## Critères de validation

- [ ] `python init_db.py` crée `planning.db` sans erreur
- [ ] Les 4 tables sont présentes dans la BDD
- [ ] Les 5 postes par défaut sont insérés
- [ ] Le compte manager de test existe et est fonctionnel
- [ ] Les relations FK sont correctement définies (vérifiable via SQLAlchemy `relationship`)
