# Данный файл содержит формы, которые отображаются на страницах сайта

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.models import User

# Форма входа на сайт для пользователей из детских учреждений
class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

# Форма поиска детских учреждений на главной странице для анонимных пользователей
class SearchForm(FlaskForm):
    search = StringField('Я хочу, чтобы мой ребенок занимался', validators=[DataRequired()])
    submit = SubmitField('Найти учреждение')

# Форма регистрации пользователей из детских учреждений
class SignUpForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Поворите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя не уникально, введите другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email не уникален.')

# Форма расширенного поиска детских учреждений на странице найденных учреждений для анонимных пользователей
class AdvancedSearchForm(FlaskForm):
    sport = BooleanField('ДЮСШ')
    music = BooleanField('Музыка')
    theatre  = BooleanField('Музыка')
    tto = BooleanField('Дошкольники')
    ttoten = BooleanField('Младшие школьники')
    submit = SubmitField('Найти учреждения')

# Форма добавления детского учреждения в аккаунте пользователя
class AddClubForm(FlaskForm):
    club = StringField('Название кружка', validators=[DataRequired()])
    institution = StringField('Учреждение', validators=[DataRequired()])
    teacher = StringField('Преподаватель', validators=[DataRequired()])
    category = FormField(AdvancedSearchForm)
    submit = SubmitField('Добавить кружок')

# Форма выбора города при поиске десткого учреждения на всех страницах
class CityForm(FlaskForm):
    city = SelectField(
        'Выберите Ваш город',
        choices=[('К', 'Краматорск'), ('С', 'Славянск'), ('Д', 'Дружковка')]
    )

#class CityForm(FlaskForm):
#    city_id = SelectField(u'Group', coerce=int)
#def edit_city(request, id):
#    city = city.query.get(id)
#    form = CityForm(request.POST, obj=city)
#    form.city_id.choices = [(c.id, c.name) for c in Group.query.order_by('city')]