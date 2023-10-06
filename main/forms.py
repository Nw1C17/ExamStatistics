from django import forms
from django.contrib.auth import get_user_model

from main.models import ExamType

User = get_user_model()


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    # Использование виджетов на поля
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Повторите пароль'
        self.fields['email'].label = 'Электронная почта'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый адрес уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} уже занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']



PARAMETERS = [
    ('district', 'Району'),
    ('school', 'Образовательному учереждению'),
    ('subject', 'Предмету'),
]
HEADS = [('1', 'Год'), ('2', 'Предмет')]
STAT_FIELDS = [
    ('sum', 'Всего участников'),
    ('avg', 'Средний балл'),
    ('score_5', 'Оценки (5 бальная система)'),
    ('score_100', 'Оценки (100 бальная система)'),
]

EXAM_TYPES = [
    ('1', 'ЕГЭ'),
    ('2', 'ОГЭ')
]
class TemplateBuilderForm(forms.Form):
    name = forms.CharField(max_length=255, label='Название шаблона')
    exam_type = forms.ChoiceField(widget=forms.RadioSelect, choices=EXAM_TYPES, label='Выбор экзамена')
    head = forms.ChoiceField(widget=forms.RadioSelect, choices=HEADS, label='Шапка')
    param = forms.MultipleChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=PARAMETERS,
        label='Статистика по:'
    )
    stat_fields = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=STAT_FIELDS,
        label='Вычислить:'
    )

