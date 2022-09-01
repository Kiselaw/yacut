from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[URL(message='Некорректная ссылка'),
                    DataRequired(message='Укажите ссылку')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message='Длина не должна превышать 16 символов'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
