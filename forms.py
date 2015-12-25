# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class AddRelationForm(Form):
    subject = StringField(validators=[Required()])
    predicate = StringField(validators=[Required()])
    object = StringField(validators=[Required()])
    submit = SubmitField('保存')
