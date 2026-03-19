# TICKET-05 — Module Créneaux Horaires

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-05 |
| Module | `shifts/` |
| Priorité | Haute |
| Statut | À faire |
| Dépendances | TICKET-04 |
| Fonctionnalités | F12, F13, F14, F15, F16 |
| Accès | Manager uniquement |

## Description

Gestion des créneaux de travail affectés aux employés. Chaque créneau est lié à un employé, une date, une plage horaire et un poste. La détection de conflits est obligatoire côté serveur. La duplication permet de répéter rapidement un créneau sur plusieurs jours.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F12 | Création d'un créneau pour un employé à une date donnée |
| F13 | Modification d'un créneau existant |
| F14 | Suppression d'un créneau |
| F15 | Vérification automatique des conflits (double affectation) |
| F16 | Duplication d'un créneau sur plusieurs jours |

## Tâches

### 1. `shifts/forms.py` — Formulaires

#### Formulaire `ShiftForm` (création + édition)

| Champ | Type WTForms | Validation |
|---|---|---|
| user_id | SelectField | Obligatoire (liste des employés actifs) |
| post_id | SelectField | Obligatoire (liste des postes) |
| date_service | DateField | Obligatoire |
| heure_debut | TimeField | Obligatoire |
| heure_fin | TimeField | Obligatoire, doit être > heure_debut |
| note | TextAreaField | Optionnel |

#### Formulaire `DuplicateShiftForm`

| Champ | Type WTForms | Validation |
|---|---|---|
| date_debut | DateField | Obligatoire — début de la plage |
| date_fin | DateField | Obligatoire — fin de la plage |
| jours | MultipleSelectField | Optionnel — filtrer sur certains jours de la semaine |

---

### 2. `shifts/routes.py` — Routes

#### `GET/POST /shifts/new` — Création (F12)
- GET : formulaire vide (peut préremplir `user_id` et `date` via paramètres URL)
- POST :
  1. Valider le formulaire
  2. Vérifier `heure_fin > heure_debut`
  3. Appeler `check_conflict()` — bloquer si conflit détecté
  4. Sauvegarder le créneau avec `created_by = current_user.id`
  5. Flash succès → rediriger vers `/planning/week`

#### `GET/POST /shifts/<id>/edit` — Modification (F13)
- GET : formulaire prérempli
- POST :
  1. Valider le formulaire
  2. Revérifier les conflits (en excluant le créneau en cours d'édition)
  3. Sauvegarder
  4. Flash succès → rediriger vers `/planning/week`

#### `POST /shifts/<id>/delete` — Suppression (F14)
- Vérifier que le créneau existe
- Supprimer de la BDD
- Flash succès → rediriger vers la page précédente

#### `POST /shifts/check-conflict` — Vérification AJAX (F15)
- Accepte : `user_id`, `date_service`, `heure_debut`, `heure_fin`, `exclude_id` (optionnel)
- Retourne JSON :
  ```json
  { "conflict": true/false, "message": "..." }
  ```
- Logique : rechercher dans `shifts` un créneau du même employé, même date, dont les plages se chevauchent

#### `POST /shifts/<id>/duplicate` — Duplication (F16)
- Accepte : `date_debut`, `date_fin`, `jours` (optionnel)
- Pour chaque jour dans la plage :
  1. Vérifier l'absence de conflit
  2. Créer un créneau identique à la date cible (ignorer silencieusement les jours en conflit ou alerter)
- Flash avec résumé : « X créneaux créés, Y ignorés (conflits) »

---

### 3. Fonction utilitaire `check_conflict()`

```
check_conflict(user_id, date_service, heure_debut, heure_fin, exclude_shift_id=None)
→ retourne True si conflit, False sinon
```

Condition de chevauchement :
- Même `user_id` et même `date_service`
- Les plages horaires se chevauchent : `heure_debut < autre.heure_fin AND heure_fin > autre.heure_debut`

---

### 4. Templates

#### `templates/shifts/form.html`
- Formulaire de création/édition
- Vérification de conflit en temps réel via AJAX sur les champs `user_id`, `date_service`, `heure_debut`, `heure_fin`
- Indicateur visuel (rouge/vert) du résultat de la vérification

#### `templates/shifts/confirm_delete.html`
- Page de confirmation avant suppression
- Rappel des informations du créneau (employé, date, horaire)
- Boutons : Confirmer / Annuler

#### `templates/shifts/duplicate_form.html`
- Formulaire de duplication avec sélection de la plage de dates

---

## Critères de validation

- [ ] Un créneau avec `heure_fin <= heure_debut` est refusé
- [ ] Deux créneaux qui se chevauchent pour le même employé le même jour sont refusés
- [ ] La vérification AJAX retourne une réponse JSON correcte
- [ ] La suppression d'un créneau le retire définitivement de la BDD
- [ ] La duplication crée les créneaux correctement et signale les conflits ignorés
- [ ] `created_by` est bien renseigné avec l'ID du manager connecté
- [ ] Toutes les routes sont inaccessibles à un employé (erreur 403)
