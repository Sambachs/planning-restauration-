from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError


class ShiftForm(FlaskForm):
    user_id = SelectField('Employé', coerce=int, validators=[DataRequired()])
    post_id = SelectField('Poste', coerce=int, validators=[DataRequired()])
    date_service = DateField('Date', validators=[DataRequired()])
    heure_debut = TimeField('Heure de début', validators=[DataRequired()])
    heure_fin = TimeField('Heure de fin', validators=[DataRequired()])
    note = TextAreaField('Note (optionnel)', validators=[Optional()])
    submit = SubmitField('Enregistrer')

    def validate_heure_fin(self, field):
        if self.heure_debut.data and field.data:
            if field.data <= self.heure_debut.data:
                raise ValidationError("L'heure de fin doit être après l'heure de début.")

    def set_choices(self, employes, postes):
        self.user_id.choices = [(e.id, e.nom_complet) for e in employes]
        self.post_id.choices = [(p.id, p.nom) for p in postes]


class DuplicateShiftForm(FlaskForm):
    date_debut = DateField('Du', validators=[DataRequired()])
    date_fin = DateField('Au', validators=[DataRequired()])
    submit = SubmitField('Dupliquer')

    def validate_date_fin(self, field):
        if self.date_debut.data and field.data:
            if field.data < self.date_debut.data:
                raise ValidationError("La date de fin doit être après la date de début.")
