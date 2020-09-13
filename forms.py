from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    name = StringField('Nickname', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    create = SubmitField('Create')
    join = SubmitField('Join')

class ChatBox(FlaskForm):
    msg = StringField('Message')
    send = SubmitField('Send')