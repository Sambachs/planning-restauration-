# TICKET-06 — Module Congés & Absences (côté Employé)

## Informations générales

| Champ | Valeur |
|---|---|
| ID | TICKET-06 |
| Module | `absences/` — partie Employé |
| Priorité | Moyenne |
| Statut | À faire |
| Dépendances | TICKET-02 |
| Fonctionnalités | F17, F18, F19 |
| Accès | Employé (et Manager) |

## Description

Interface permettant à l'employé de soumettre, consulter et annuler ses demandes de congés. L'employé ne peut voir que ses propres demandes. Il ne peut annuler qu'une demande dont le statut est encore `en_attente`.

## Fonctionnalités couvertes

| Code | Description |
|---|---|
| F17 | Soumission d'une demande de congé (dates + motif) |
| F18 | Consultation du statut de ses demandes |
| F19 | Annulation d'une demande en attente |

## Tâches

### 1. `absences/forms.py` — Formulaire de demande de congé

#### Formulaire `AbsenceRequestForm`

| Champ | Type WTForms | Validation |
|---|---|---|
| type_absence | SelectField | Obligatoire (`conge_paye` / `sans_solde`) |
| date_debut | DateField | Obligatoire, >= aujourd'hui |
| date_fin | DateField | Obligatoire, >= date_debut |
| motif | TextAreaField | Optionnel |

---

### 2. `absences/routes.py` — Routes

#### `GET/POST /absences/request` — Soumission d'une demande (F17)
- GET : afficher le formulaire vide
- POST :
  1. Valider le formulaire
  2. Vérifier que `date_fin >= date_debut`
  3. Vérifier que `date_debut >= aujourd'hui`
  4. Créer l'absence avec `statut = 'en_attente'` et `user_id = current_user.id`
  5. Flash succès → rediriger vers `/absences/my`

#### `GET /absences/my` — Mes demandes (F18)
- Récupérer toutes les absences de `current_user`
- Trier par date de soumission (les plus récentes en premier)
- Afficher le statut avec code couleur :
  - `en_attente` → orange
  - `approuve` → vert
  - `refuse` → rouge

#### `POST /absences/<id>/cancel` — Annulation (F19)
- Vérifier que l'absence appartient bien à `current_user`
- Vérifier que le statut est `en_attente` (sinon refuser)
- Supprimer ou passer le statut à `annule`
- Flash succès → rediriger vers `/absences/my`

---

### 3. Templates

#### `templates/absences/request_form.html`
- Formulaire de demande avec sélection du type, des dates et du motif
- Validation côté client : date_fin >= date_debut
- Messages d'erreur par champ

#### `templates/absences/my_absences.html`
- Tableau de toutes les demandes de l'employé connecté
- Colonnes : Type, Période, Motif, Date de soumission, Statut, Action
- Badge coloré pour le statut
- Bouton « Annuler » uniquement visible si `statut == 'en_attente'`
- Commentaire du manager visible si `statut == 'refuse'`
- Bouton « Nouvelle demande »

---

## Critères de validation

- [ ] Une demande avec `date_debut` dans le passé est refusée
- [ ] Une demande avec `date_fin < date_debut` est refusée
- [ ] L'employé ne voit que ses propres demandes
- [ ] Un employé ne peut pas annuler une demande déjà approuvée ou refusée
- [ ] Un employé ne peut pas accéder aux demandes d'un autre employé (vérification par ID)
- [ ] Le commentaire du manager s'affiche en cas de refus
