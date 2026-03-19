# Index des Tickets — Application de Planning Restauration

## Vue d'ensemble

| Ticket | Module | Priorité | Dépendances | Statut |
|---|---|---|---|---|
| [TICKET-00](./TICKET-00_initialisation.md) | Setup global | Critique | — | À faire |
| [TICKET-01](./TICKET-01_modeles_bdd.md) | `models.py` | Critique | TICKET-00 | À faire |
| [TICKET-02](./TICKET-02_authentification.md) | `auth/` | Critique | TICKET-01 | À faire |
| [TICKET-03](./TICKET-03_dashboard.md) | `main/` | Haute | TICKET-02 | À faire |
| [TICKET-04](./TICKET-04_employes.md) | `employees/` | Haute | TICKET-02 | À faire |
| [TICKET-05](./TICKET-05_creneaux.md) | `shifts/` | Haute | TICKET-04 | À faire |
| [TICKET-06](./TICKET-06_conges_employe.md) | `absences/` Employé | Moyenne | TICKET-02 | À faire |
| [TICKET-07](./TICKET-07_conges_manager.md) | `absences/` Manager | Moyenne | TICKET-06 | À faire |
| [TICKET-08](./TICKET-08_planning_calendrier.md) | `planning/` | Haute | TICKET-05, TICKET-07 | À faire |

## Ordre de réalisation

```
TICKET-00 (Setup)
    └── TICKET-01 (Modèles BDD)
            └── TICKET-02 (Auth)
                    ├── TICKET-03 (Dashboard)
                    ├── TICKET-04 (Employés)
                    │       └── TICKET-05 (Créneaux)
                    │               └── ─────────────┐
                    └── TICKET-06 (Congés Employé)   │
                            └── TICKET-07 (Congés Manager)
                                        └── TICKET-08 (Planning) ←─┘
```

## Fonctionnalités du cahier des charges — couverture

| Code | Description | Ticket |
|---|---|---|
| F01 | Page de connexion email/mot de passe | TICKET-02 |
| F02 | Authentification bcrypt | TICKET-02 |
| F03 | Gestion de session | TICKET-02 |
| F04 | Déconnexion | TICKET-02 |
| F05 | Redirection selon rôle | TICKET-02 |
| F06 | Protection des pages | TICKET-02 |
| F07 | Liste des employés | TICKET-04 |
| F08 | Création d'un employé | TICKET-04 |
| F09 | Modification d'un employé | TICKET-04 |
| F10 | Désactivation d'un compte | TICKET-04 |
| F11 | Recherche et filtrage employés | TICKET-04 |
| F12 | Création d'un créneau | TICKET-05 |
| F13 | Modification d'un créneau | TICKET-05 |
| F14 | Suppression d'un créneau | TICKET-05 |
| F15 | Vérification des conflits | TICKET-05 |
| F16 | Duplication d'un créneau | TICKET-05 |
| F17 | Soumission demande de congé | TICKET-06 |
| F18 | Consultation statut des demandes | TICKET-06 |
| F19 | Annulation d'une demande | TICKET-06 |
| F20 | Liste des demandes (Manager) | TICKET-07 |
| F21 | Approbation / refus | TICKET-07 |
| F22 | Saisie absence imprévue | TICKET-07 |
| F23 | Absences sur le planning | TICKET-07 + TICKET-08 |
| F24 | Vue hebdomadaire | TICKET-08 |
| F25 | Vue mensuelle | TICKET-08 |
| F26 | Navigation semaines / mois | TICKET-08 |
| F27 | Filtrage par employé / poste | TICKET-08 |
| F28 | Indicateur visuel absences | TICKET-08 |
| F29 | Code couleur par poste | TICKET-08 |
