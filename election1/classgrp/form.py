from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired, ValidationError
from election1.models import Classgrp, Office
# from wtforms_alchemy.fields import QuerySelectField


def classgrp_query():
    return Classgrp.query.order_by(Classgrp.sortkey)


def office_query():
    return Office.query.order_by(Office.sortkey)


class ClassgrpForm(FlaskForm):

    name = StringField(label='Class or Group . . .', validators=[Length(min=2, max=30), DataRequired()])
    sortkey = IntegerField(label='Sort Key . . .', validators=[DataRequired()])
    submit = SubmitField(label='submit')

    @staticmethod
    def validate_name(form, field):
        classgrp = Classgrp.query.filter_by(name=field.data).first()
        if classgrp:
            raise ValidationError('This class or group name already exists in the database.')
    @staticmethod
    def validate_sortkey(form, field):
        classgrp = Classgrp.query.filter_by(sortkey=field.data).first()
        if classgrp:
            raise ValidationError('This sort key already exists in the database.')