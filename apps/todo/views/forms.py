from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])


class TodoForm(Form):
    title = StringField('title', [
        validators.required(),
        validators.Length(min=4, max=100)
    ])

    text = StringField('text', [
        validators.required(),
        validators.Length(min=4, max=300)
    ])