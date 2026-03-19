# TICKET-03 — Dashboard

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-03 |
| Module | `main/` |
| Priorité | Haute |
| Statut | À faire |
| Dépendances | TICKET-02 |

## Description

Page d'accueil post-connexion. Le contenu affiché diffère selon le rôle de l'utilisateur connecté. Le Manager voit un résumé de l'état global du restaurant. L'employé voit son planning de la semaine et ses demandes de congés.

## Tâches

### 1. Route `GET /dashboard`

Logique :
- Vérifier que l'utilisateur est connecté (`@login_required`)
- Si `role == 'manager'` → préparer les données manager
- Si `role == 'employe'` → préparer les données employé
- Rendre le template correspondant

---

### 2. Vue Manager — données à afficher

- Nombre total d'employés actifs
- Nombre de créneaux créés pour la semaine en cours
- Nombre de demandes de congés en attente (`statut == 'en_attente'`)
- Liste des 5 prochains créneaux (tous employés confondus)
- Alertes : demandes de congés en attente (avec lien vers la liste)

---

### 3. Vue Employé — données à afficher

- Planning de la semaine en cours (ses créneaux uniquement)
- Ses 3 dernières demandes de congés avec leur statut (`en_attente` / `approuvé` / `refusé`)
- Lien rapide vers le formulaire de demande de congé

---

### 4. Templates

#### `templates/dashboard_manager.html`
- Cards de résumé (employés actifs, créneaux semaine, demandes en attente)
- Tableau des prochains créneaux
- Section alertes

#### `templates/dashboard_employee.html`
- Planning de la semaine sous forme de liste
- Section statut des demandes de congés
- Bouton « Faire une demande de congé »

---

## Critères de validation

- [ ] Un manager connecté voit le dashboard manager
- [ ] Un employé connecté voit le dashboard employé
- [ ] Les chiffres affichés correspondent aux données réelles de la BDD
- [ ] Un utilisateur non connecté est redirigé vers `/login`
- [ ] La navigation dans `base.html` affiche les bons liens selon le rôle
