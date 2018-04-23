# Данный файл содержит формы, которые отображаются на страницах сайта

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, PasswordField, BooleanField, SubmitField, SelectField, FormField, FieldList, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.models import User
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet('images', IMAGES)

# Форма загрузки изображения
class UploadForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])

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
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя не уникально, введите другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email не уникален.')

# Базовая форма категорий
class CategoriesForm(FlaskForm):
    sport = BooleanField('ДЮСШ')
    music = BooleanField('Музыка')
    theatre  = BooleanField('Театр')

# Базовая форма возрастов
class AgesForm(FlaskForm):
    fromto5 = BooleanField('До 5 лет')
    from6to9 = BooleanField('От 6 до 9 лет')
    from10to14 = BooleanField('От 10 до 14 лет')
    from15to18 = BooleanField('От 15 до 18 лет')

# Форма расширенного поиска детских учреждений на странице найденных учреждений для анонимных пользователей
class AdvancedSearchForm(FlaskForm):
    categories = FormField(CategoriesForm)
    ages = FormField(AgesForm)
    submit = SubmitField('Найти учреждения')

class OfficeHours(FlaskForm):
    Monday = StringField('Понедельник', validators=[DataRequired()])
    Tuesday = StringField('Вторник', validators=[DataRequired()])
    Wednesday = StringField('Среда', validators=[DataRequired()])
    Thursday = StringField('Четверг', validators=[DataRequired()])
    Friday = StringField('Пятница', validators=[DataRequired()])
    Saturday = StringField('Суббота', validators=[DataRequired()])
    Sunday = StringField('Воскресенье', validators=[DataRequired()])

# Форма добавления детского учреждения в аккаунте пользователя
class AddClubForm(FlaskForm):
    name = StringField('Название кружка', validators=[DataRequired()])
    institution = StringField('Учреждение', validators=[DataRequired()])
    snippet = StringField('Краткое описание кружка', validators=[DataRequired()])
    description = StringField('Полное описание кружка', validators=[DataRequired()])
    leader = StringField('Преподаватель', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    web = StringField('WEB-страница')
    email = StringField('Электронная почта')
    social = StringField('Страница в социальной сети')
    street = StringField('Улица', validators=[DataRequired()])
    building = StringField('Номер строения', validators=[DataRequired()])
    room = StringField('Кабинет')
    #hours = FieldList(FormField(OfficeHours), min_entries=1, max_entries=1, label = 'Время работы')
    #url_logo = FormField(UploadForm)
    ages = FormField(AgesForm, label = 'Возраст')
    categories = FormField(CategoriesForm, label = 'Категория')
    tags = StringField('Тэги', validators=[DataRequired()])
    #photos = FormField(UploadPhotoForm)
    submit = SubmitField('Добавить кружок')

# Форма выбора города при поиске десткого учреждения на всех страницах
class CityForm(FlaskForm):
    city = SelectField(
        'Выберите Ваш город',
        choices=[('К', 'Краматорск'), ('С', 'Славянск'), ('Д', 'Дружковка')]
    )