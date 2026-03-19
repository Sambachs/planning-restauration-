from datetime import date
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError

TYPES_CONGE = [
    ('conge_paye', 'Congé payé'),
    ('sans_solde', 'Congé sans solde'),
]

TYPES_ABSENCE_MANAGER = [
    ('maladie',    'Absence maladie'),
    ('injustifie', 'Absence injustifiée'),
]


class AbsenceRequestForm(FlaskForm):
    type_absence = SelectField('Type de congé', choices=TYPES_CONGE, validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    motif = TextAreaField('Motif (optionnel)', validators=[Optional()])
    submit = SubmitField('Soumettre la demande')

    def validate_date_debut(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('La date de début ne peut pas être dans le passé.')

    def validate_date_fin(self, field):
        if self.date_debut.data and field.data:
            if field.data < self.date_debut.data:
                raise ValidationError('La date de fin doit être après la date de début.')


class ManualAbsenceForm(FlaskForm):
    user_id = SelectField('Employé', coerce=int, validators=[DataRequired()])
    type_absence = SelectField('Type d\'absence', choices=TYPES_ABSENCE_MANAGER, validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    motif = TextAreaField('Motif (optionnel)', validators=[Optional()])
    submit = SubmitField('Enregistrer l\'absence')

    def set_employe_choices(self, employes):
        self.user_id.choices = [(e.id, e.nom_complet) for e in employes]

    def validate_date_fin(self, field):
        if self.date_debut.data and field.data:
            if field.data < self.date_debut.data:
                raise ValidationError('La date de fin doit être après la date de début.')


class RejectAbsenceForm(FlaskForm):
    commentaire_manager = TextAreaField('Commentaire (optionnel)', validators=[Optional()])
    submit = SubmitField('Confirmer le refus')
