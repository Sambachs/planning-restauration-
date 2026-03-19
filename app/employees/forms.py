from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length


CONTRATS = [('CDI', 'CDI'), ('CDD', 'CDD'), ('Extra', 'Extra'), ('Apprenti', 'Apprenti')]
ROLES = [('employe', 'Employé'), ('manager', 'Manager')]


class EmployeeForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(max=50)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Mot de passe', validators=[Optional(), Length(min=6)])
    telephone = TelField('Téléphone', validators=[Optional(), Length(max=20)])
    post_id = SelectField('Poste', coerce=int, validators=[Optional()])
    contrat = SelectField('Type de contrat', choices=CONTRATS, validators=[DataRequired()])
    date_embauche = DateField('Date d\'embauche', validators=[DataRequired()])
    role = SelectField('Rôle', choices=ROLES, validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

    def set_post_choices(self, postes):
        self.post_id.choices = [(0, '— Sélectionner un poste —')] + [(p.id, p.nom) for p in postes]
