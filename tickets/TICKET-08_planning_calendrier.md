# TICKET-08 — Module Planning (Vue Calendrier)

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-08 |
| Module | `planning/` |
| Priorité | Haute |
| Statut | À faire |
| Dépendances | TICKET-05, TICKET-07 |
| Fonctionnalités | F24, F25, F26, F27, F28, F29 |
| Accès | Tous les utilisateurs connectés |

## Description

Vue calendrier du planning. Le Manager voit tous les employés et peut filtrer. L'employé ne voit que son propre planning. Les absences approuvées apparaissent visuellement comme des jours bloqués. Les créneaux sont colorés par poste.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F24 | Vue planning hebdomadaire (lundi → dimanche) |
| F25 | Vue planning mensuelle (résumé des jours travaillés) |
| F26 | Navigation entre semaines et mois (précédent / suivant) |
| F27 | Filtrage par employé ou par poste (Manager uniquement) |
| F28 | Indicateur visuel des absences et congés approuvés |
| F29 | Code couleur par poste |

## Tâches

### 1. `planning/routes.py` — Routes

#### `GET /planning/week` — Vue hebdomadaire (F24, F26, F27, F28, F29)

Paramètres URL acceptés :
- `?date=YYYY-MM-DD` — afficher la semaine contenant cette date (défaut : semaine courante)
- `?employe=<user_id>` — filtrer sur un employé (Manager uniquement)
- `?poste=<post_id>` — filtrer sur un poste (Manager uniquement)

Logique :
1. Calculer le lundi et le dimanche de la semaine cible
2. Récupérer les créneaux de la période (filtrés selon le rôle)
3. Récupérer les absences approuvées/confirmées de la période
4. Calculer les URLs de navigation : semaine précédente / semaine suivante
5. Passer la liste des employés et postes pour les menus de filtre (Manager)

Structure des données passées au template :
```python
{
  "semaine": [lundi, mardi, ..., dimanche],  # 7 objets date
  "creneaux_par_jour": { date: [shift, ...] },
  "absences_par_employe": { user_id: [absence, ...] },
  "employes": [...],  # pour le filtre Manager
  "postes": [...]     # pour le filtre Manager
}
```

#### `GET /planning/month` — Vue mensuelle (F25, F26, F27, F28)

Paramètres URL :
- `?mois=YYYY-MM` — afficher ce mois (défaut : mois courant)
- `?employe=<user_id>` — filtrer (Manager uniquement)

Logique :
1. Calculer tous les jours du mois
2. Pour chaque jour, compter le nombre de créneaux par employé
3. Récupérer les absences du mois
4. Calculer les URLs précédent/suivant

#### `GET /planning/data` — Données JSON (AJAX)

Paramètres : `date_debut`, `date_fin`, `employe_id` (optionnel), `post_id` (optionnel)

Retourne :
```json
{
  "shifts": [
    {
      "id": 1,
      "employe": "Dupont Jean",
      "poste": "Serveur",
      "couleur": "#2196F3",
      "date": "2026-03-20",
      "heure_debut": "11:00",
      "heure_fin": "15:30",
      "note": "..."
    }
  ],
  "absences": [
    {
      "employe": "Martin Sophie",
      "type": "conge_paye",
      "date_debut": "2026-03-22",
      "date_fin": "2026-03-26"
    }
  ]
}
```

---

### 2. Code couleur par poste (F29)

Les couleurs sont stockées dans la table `posts` (champ `couleur` HEX).
Elles sont passées au template et appliquées via style inline ou classe CSS dynamique.

Exemple d'utilisation en Jinja2 :
```html
<span style="background-color: {{ shift.post.couleur }}">
  {{ shift.post.nom }}
</span>
```

---

### 3. Templates

#### `templates/planning/week.html`
- Grille 7 colonnes (lundi → dimanche)
- En-têtes : jour de la semaine + date
- Chaque cellule : liste des créneaux du jour (triés par heure)
  - Badge coloré par poste
  - Nom de l'employé + horaire
  - Indicateur d'absence (fond différent / icône)
- Boutons navigation : `← Semaine précédente` / `Semaine suivante →`
- Formulaire de filtre (Manager uniquement) : employé + poste
- Bouton « Ajouter un créneau » (Manager uniquement)

#### `templates/planning/month.html`
- Grille calendrier mensuelle (7 colonnes, semaines en lignes)
- Dans chaque case : points ou résumé des créneaux
- Jours avec absence : fond coloré distinctif
- Navigation mois précédent / mois suivant
- Filtre par employé (Manager uniquement)

---

### 4. `static/js/planning.js`

Fonctions JavaScript :
- Chargement dynamique des données via `fetch('/planning/data?...')`
- Mise à jour de la vue sans rechargement complet (optionnel, si implémenté)
- Gestion de la navigation clavier (flèches gauche/droite pour changer de semaine)

---

## Critères de validation

- [ ] La vue semaine affiche les 7 jours avec les créneaux corrects
- [ ] La navigation précédent/suivant change la semaine ou le mois affiché
- [ ] Un employé ne voit que ses propres créneaux
- [ ] Le Manager voit tous les créneaux et peut filtrer
- [ ] Les absences approuvées apparaissent visuellement sur le calendrier
- [ ] Chaque créneau est affiché avec la couleur de son poste
- [ ] La route `/planning/data` retourne du JSON valide
- [ ] La vue mois affiche le bon nombre de jours et le bon positionnement
