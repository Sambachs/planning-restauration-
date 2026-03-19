# TICKET-00 — Initialisation du projet

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-00 |
| Module | Setup global |
| Priorité | Critique |
| Statut | À faire |
| Dépendances | Aucune |

## Description

Mise en place de l'environnement de développement, de la structure de dossiers du projet et des fichiers de configuration de base. Ce ticket est le point de départ obligatoire avant tout développement.

## Tâches

### 1. Mettre à jour `requirements.txt`

Ajouter toutes les dépendances nécessaires :

```
Flask==2.3.3
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-WTF==1.2.1
Flask-SQLAlchemy==3.1.1
WTForms==3.1.1
```

---

### 2. Créer la structure de dossiers

```
planning_restauration/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── employees/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── shifts/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── absences/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── planning/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── employees/
│   │   ├── shifts/
│   │   ├── absences/
│   │   └── planning/
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── planning.js
├── config.py
├── run.py
├── planning.db
└── requirements.txt
```

---

### 3. Créer `config.py`

Contenu attendu :
- `SECRET_KEY` (clé secrète Flask — ne jamais exposer en production)
- `SQLALCHEMY_DATABASE_URI` pointant vers `planning.db`
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`
- `WTF_CSRF_ENABLED = True`

---

### 4. Créer `app/__init__.py`

Responsabilités :
- Instancier l'application Flask (factory pattern)
- Initialiser les extensions : `db`, `login_manager`, `bcrypt`, `csrf`
- Enregistrer les Blueprints : `auth`, `employees`, `shifts`, `absences`, `planning`
- Configurer `login_manager.login_view = 'auth.login'`

---

### 5. Créer `run.py`

Point d'entrée de l'application :
- Importer l'app factory
- Lancer en mode debug pour le développement

---

## Critères de validation

- [ ] `pip install -r requirements.txt` s'exécute sans erreur
- [ ] `python run.py` démarre le serveur Flask sans erreur
- [ ] La structure de dossiers est conforme au Document de Conception (section 1.2)
- [ ] L'application répond sur `http://localhost:5000`
