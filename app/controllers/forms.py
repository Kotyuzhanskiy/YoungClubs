# Данный файл содержит формы, которые отображаются на страницах сайта

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, PasswordField, BooleanField, SubmitField, SelectField, FormField, FieldList, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, URL
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
    search = StringField('Моему ребенку интересны',
    description = '''укажите область интересов Вашего ребенка''',
    validators=[DataRequired()])
    submit = SubmitField('Найти кружки')

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
    fromto5 = BooleanField(label='До 5 лет')
    from6to9 = BooleanField(label='От 6 до 9 лет')
    from10to14 = BooleanField(label='От 10 до 14 лет')
    from15to18 = BooleanField(label='От 15 до 18 лет')

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
    name = StringField('Название кружка',
        description = 'Укажите название для Вашего кружка',
        validators=[DataRequired()]
        )
    institution = StringField('Учреждение',
        description = '''Укажите учреждение, к которому принадлежит кружок.
        Если кружок самостоятельный, оставьте это поле пустым'''
        )
    snippet = StringField('Краткое описание кружка',
        description = '''Коротко опишите то, чем занимается кружок,
        уделите внимание самым интересным направлениям кружка.
        Эта информация появляется на странице поиска кружков,
        что позволяет родителям делать выбор из предварительно найденного списка кружков.
        Вы можете использовать не более 500 символов.''',
        validators=[DataRequired(), Length(max=500)]
        )
    description = StringField('Полное описание кружка',
        description = '''Опишите все направления деятельности Вашего кружка,
        почему ребенку будет интересно заниматься именно в Вашем кружке. Какие выгоды получит
        ребенок от занятий в кружке.
        Расскажите о:\n
        результатах и достижениях кружка (например, о победах в конкурсе);\n
        о преподавателях кружка, об их опыте, знаниях, отзывах;\n
        о специализированном оснащении (если оно используется в работе).\n
        Вы можете использовать не более 10 000 символов.''',
        validators=[DataRequired(), Length(max=10000)]
        )
    leader = StringField('Преподаватель',
        description = '''Полностью укажите фамилию, отчество, преподавателя
        (или преподавателей через запятую).''',
        validators=[DataRequired(), Length(max=150)]
        )
    price = StringField('Цена',
        description = '''Укажите стоимость посещения ребеноком кружка.
        Если занятия не оплачиваются, укажите "бесплатно".''',
        validators=[DataRequired(), Length(max=50)]
        )
    phone = StringField('Телефон',
        description = '''Укажите телефон, по которому родители могут
        позвонить дляя уточнения интересующих их вопросов.''',
        validators=[DataRequired(), Length(max=30)]
        )
    web = StringField('WEB-страница',
        description = '''Укажите (если есть) сайт в интернете, где родители могут
        получить дополнительную информацию о работе Вашего кружка.
        В этом поле обязательно http(s)://'''
        )
    email = StringField('Электронная почта',
        description = '''Укажите (если есть) электронную почту для связи с Вашим кружком.'''
        )
    social = StringField('Страница в социальной сети',
        description = '''Укажите (если есть) страницу в сициальной сети, где родители могут
        подробнее познакомиться с жизнью Вашего кружка.
        В этом поле обязательно http(s)://'''
        )
    street = StringField('Улица',
        description = '''Укажите улицу, на которой расположен кружок''',
        validators=[DataRequired()]
        )
    building = StringField('Номер строения',
        description = '''Укажите номер дома, где которой расположен кружок''',
        validators=[DataRequired()]
        )
    room = StringField('Кабинет',
        description = '''Укажите номер кабинета (комнаты или др.), где которой расположен кружок.
        Если кружок расположен не в отдбеном кабеине, Вы можете оставить это поле пустым'''
        )
    ages_from = IntegerField('Возраст от',
        description = '''Укажите, с какого возраста дети могут посещать Ваш кружок''',
        validators=[DataRequired()]
        )
    ages_to = IntegerField('Возраст до',
        description = '''Укажите, до какого возраста дети могут посещать Ваш кружок''',
        validators=[DataRequired()]
        )
    categories = FormField(CategoriesForm,
        description = '''Укажите категорию, с которой связана деятельность кружка''',
        label = 'Категория'
        )
    tags = StringField('Тэги',
        description = '''Внесите список ключевых слов, с которыми связана деятельность кружка.
        Это важное поле, потому как оно напрямую влияет на выдачу в поисковом запросе на главной странице.
        Поэтому постарайтесь учесть и указать все возможные варианты, которые могут быть использованы родителями
        при поиске. Например, для танцевального клуба, также укажите список танцев, которыми может заниматься
        в Вашем кружке.
        Ключевые слова необходимо вносить маленькими буквами, в именительном падеже, разделяя их запятыми''',
        validators=[DataRequired()]
        )
    #Submit = SubmitField('Добавить кружок')
    #hours = FieldList(FormField(OfficeHours), min_entries=1, max_entries=1, label = 'Время работы')
    #url_logo = FormField(UploadForm)
    #photos = FormField(UploadPhotoForm)

# Форма выбора города при поиске десткого учреждения на всех страницах
class CityForm(FlaskForm):
    city = SelectField(
        'Выберите Ваш город',
        choices=[('К', 'Краматорск'), ('С', 'Славянск'), ('Д', 'Дружковка')]
    )