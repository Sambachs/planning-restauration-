# TICKET-07 — Module Congés & Absences (côté Manager)

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-07 |
| Module | `absences/` — partie Manager |
| Priorité | Moyenne |
| Statut | À faire |
| Dépendances | TICKET-06 |
| Fonctionnalités | F20, F21, F22, F23 |
| Accès | Manager uniquement |

## Description

Interface manager pour traiter les demandes de congés soumises par les employés, et saisir manuellement des absences imprévues (maladie, absence injustifiée). Les absences approuvées sont visibles sur le planning.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F20 | Consultation de toutes les demandes de congés en attente |
| F21 | Approbation ou refus d'une demande (avec commentaire optionnel) |
| F22 | Saisie manuelle d'une absence imprévue |
| F23 | Visualisation des absences sur le planning (jours bloqués) |

## Types d'absences et statuts

| Type | Initiateur | Statuts possibles |
|---|---|---|
| `conge_paye` | Employé | en_attente, approuve, refuse |
| `sans_solde` | Employé | en_attente, approuve, refuse |
| `maladie` | Manager | confirme |
| `injustifie` | Manager | confirme |

## Tâches

### 1. `absences/forms.py` — Formulaire absence manuelle

#### Formulaire `ManualAbsenceForm`

| Champ | Type WTForms | Validation |
|---|---|---|
| user_id | SelectField | Obligatoire (liste des employés actifs) |
| type_absence | SelectField | Obligatoire (`maladie` / `injustifie`) |
| date_debut | DateField | Obligatoire |
| date_fin | DateField | Obligatoire, >= date_debut |
| motif | TextAreaField | Optionnel |

#### Formulaire `RejectAbsenceForm`

| Champ | Type WTForms | Validation |
|---|---|---|
| commentaire_manager | TextAreaField | Optionnel |

---

### 2. `absences/routes.py` — Routes Manager

#### `GET /absences/` — Liste toutes les demandes (F20)
- Récupérer toutes les absences, filtrables via paramètres URL :
  - `?statut=en_attente|approuve|refuse|tous`
  - `?employe=<user_id>`
- Par défaut : afficher `en_attente` en premier
- Afficher le nom de l'employé, la période, le type, le statut

#### `POST /absences/<id>/approve` — Approbation (F21)
- Vérifier que le statut est `en_attente`
- Passer `statut = 'approuve'`
- Renseigner `traite_par = current_user.id`
- Flash succès → rediriger vers la liste

#### `POST /absences/<id>/reject` — Refus (F21)
- Vérifier que le statut est `en_attente`
- Accepter un `commentaire_manager` optionnel
- Passer `statut = 'refuse'`
- Renseigner `traite_par = current_user.id`
- Flash succès → rediriger vers la liste

#### `GET/POST /absences/add` — Absence manuelle (F22)
- GET : formulaire vide
- POST :
  1. Valider le formulaire
  2. Créer l'absence avec `statut = 'confirme'` et `traite_par = current_user.id`
  3. Flash succès → rediriger vers la liste

---

### 3. Données pour le planning (F23)

Préparer une requête utilitaire récupérant les absences approuvées/confirmées sur une période donnée :
```
get_approved_absences(date_debut, date_fin) → liste d'absences
```
Cette fonction sera utilisée dans TICKET-08 pour afficher les jours bloqués sur le calendrier.

---

### 4. Templates

#### `templates/absences/list.html`
- Onglets ou filtres : Toutes / En attente / Approuvées / Refusées
- Tableau : Employé, Type, Période, Soumis le, Statut, Actions
- Boutons : Approuver / Refuser (avec modal de commentaire pour le refus)
- Lien vers « Saisir une absence »

#### `templates/absences/add_form.html`
- Formulaire de saisie directe d'absence
- Sélection de l'employé et du type (maladie / injustifiée)

---

## Critères de validation

- [ ] La liste affiche toutes les demandes avec filtrage fonctionnel
- [ ] L'approbation change le statut en `approuve` et renseigne `traite_par`
- [ ] Le refus accepte un commentaire optionnel et change le statut en `refuse`
- [ ] Une demande déjà traitée (approuvée ou refusée) ne peut plus être modifiée
- [ ] Les absences manuelles sont créées avec `statut = 'confirme'` directement
- [ ] La fonction `get_approved_absences()` retourne les bons résultats pour une période
- [ ] Toutes les routes sont inaccessibles à un employé (erreur 403)
