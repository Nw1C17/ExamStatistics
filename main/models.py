from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Property(models.Model):  # Организационная форма
    name = models.CharField('Название формы', max_length=255)

    class Meta:
        verbose_name_plural = 'Организационная форма'

    def __str__(self):
        return self.name


class SchoolType(models.Model):  # Тип школы
    name = models.CharField('Название типа', max_length=255)

    class Meta:
        verbose_name_plural = 'Тип школы'

    def __str__(self):
        return self.name


class SchoolKind(models.Model):  # Вид школы
    school_type = models.ForeignKey('SchoolType', on_delete=models.PROTECT)
    code = models.IntegerField('Код школы')
    name = models.CharField('Название вида', max_length=255)

    class Meta:
        verbose_name_plural = 'Вид школы'

    def __str__(self):
        return self.name


class District(models.Model):  # Районы
    code = models.IntegerField('Код района')
    name = models.CharField('Название района', max_length=255)

    class Meta:
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.name


class LocalityType(models.Model):  # Тип населенного пункта
    name = models.CharField('Название типа', max_length=255)

    class Meta:
        verbose_name_plural = 'Тип населенного пункта'

    def __str__(self):
        return self.name


class School(models.Model):  # Школы
    school_code = models.IntegerField('Код школы', primary_key=True)
    district = models.ForeignKey('District', on_delete=models.PROTECT)
    full_name = models.CharField('Полное название школы', max_length=255)
    short_name = models.CharField('Краткое название школы', max_length=255)
    adres = models.CharField('Адрес', max_length=255)
    school_kind = models.ForeignKey('SchoolKind', on_delete=models.PROTECT)
    property = models.ForeignKey('Property', on_delete=models.PROTECT)
    town_type = models.ForeignKey('LocalityType', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Школы'
        verbose_name_plural = "Школы"

    def __str__(self):
        return self.short_name


class ExamType(models.Model):  # Тип Экзамена
    name = models.CharField('Название экзамена', max_length=255)

    class Meta:
        verbose_name_plural = 'Тип экзамена'

    def __str__(self):
        return self.name


class Subject(models.Model):  # Предметы
    name = models.CharField('Название предмета', max_length=255)

    class Meta:
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class ParticipantCategory(models.Model):  # Категория участника
    name = models.CharField('Название категории', max_length=255)

    class Meta:
        verbose_name_plural = 'Категория участника'

    def __str__(self):
        return self.name


class Examination(models.Model):  # Экзамены
    exam = models.ForeignKey('ExamType', on_delete=models.PROTECT)
    year = models.IntegerField('Год')
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    min_score = models.IntegerField('Минимальный балл для зачета')
    grading_system = models.BooleanField('5 бальная система оценивания')

    class Meta:
        verbose_name_plural = 'Экзамены'

    def __str__(self):
        return self.exam.name + "/" + str(self.year) + "/" + self.subject.name


class RequirementsSpec(models.Model):  # Кодификатор требований
    section_codeRS = models.ForeignKey('RequirementsSpec', on_delete=models.PROTECT, null=True, blank=True,
                                       default=None)
    skill_codeRS = models.CharField('Код умения', max_length=10)
    checkedRS = models.CharField('Проверяемые требования', max_length=255)
    exam = models.ForeignKey('Examination', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = 'Кодификатор требований'

    def __str__(self):
        # return str(self.exam) + "/" + self.skill_codeRS
        return self.skill_codeRS


class ElementsSpec(models.Model):  # Кодификатор элементов
    section_codeRS = models.ForeignKey('ElementsSpec', on_delete=models.PROTECT, null=True, blank=True, default=None)
    element_codeES = models.CharField('Код элемента', max_length=10)
    checkedRS = models.CharField('Проверяемые требования', max_length=255)
    exam = models.ForeignKey('Examination', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = 'Кодификатор элементов'

    def __str__(self):
        # return str(self.exam) + "/" + self.element_codeES
        return self.element_codeES


class Result(models.Model):  # Резульаты
    examination = models.ForeignKey('Examination', on_delete=models.PROTECT)
    school_code = models.ForeignKey('School', on_delete=models.PROTECT)
    variant = models.IntegerField('Вариант')
    primary_score = models.IntegerField('Первичный балл')
    completion_perc = models.IntegerField('Процент выполнения')
    shortanswer = models.CharField('Краткий ответ', max_length=50)
    full_answer = models.CharField('Полный ответ ответ', max_length=50)
    point_scale100 = models.IntegerField('100 балльная шкала')
    point_scale5 = models.IntegerField('5 балльная шкала')
    short_answerPS = models.IntegerField('Первичный балл за часть с кратким ответом')
    full_answerPS = models.IntegerField('Первичный балл за часть с полным ответом')
    category = models.ForeignKey('ParticipantCategory', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return str(self.variant)


class Specification(models.Model):  # Спецификации
    checked = models.CharField('Проверяемые требования', max_length=255)
    skills = models.ManyToManyField('RequirementsSpec')
    section_code = models.ManyToManyField('ElementsSpec')
    difficulty = models.CharField('Уровень сложности', max_length=5)
    max_score = models.IntegerField('Максимальный балл')
    estimated_time = models.IntegerField('Примерное время выполнения')
    examination = models.ForeignKey('Examination', on_delete=models.PROTECT)
    task_number = models.IntegerField('Номер задания')

    class Meta:
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return str(self.examination) + "/Задание " + str(self.task_number)


class StudentAnswer(models.Model):  # Ответы ученика
    task_number = models.ManyToManyField('Specification')
    answer = models.IntegerField('Ответ')
    result = models.ForeignKey('Result', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Ответы ученика'

    def __str__(self):
        return str(self.answer)


class UserTemplates(models.Model):  # Шаблоны пользователя
    name = models.CharField('Название шаблона', max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    jsonFile = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = 'Шаблоны пользователей'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'temp_id': self.pk})


class UserEducationalInstitution(models.Model):  # Школы привязанные к пользователю
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    school = models.ForeignKey(School, max_length=255, null=True, blank=True, default=None, on_delete=models.PROTECT)
    quantity = models.BooleanField('Все учреждения', default=True)

    class Meta:
        verbose_name_plural = 'Школы привязанные к пользователю'

    def __str__(self):
        return self.user.username


class UserDistrict(models.Model):  # Районы привязанные к пользователю
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    district = models.ForeignKey(District, max_length=255, null=True, blank=True, default=None,
                                 on_delete=models.PROTECT)
    quantity = models.BooleanField('Все районы', default=True)

    class Meta:
        verbose_name_plural = 'Районы привязанные к пользователю'

    def __str__(self):
        return self.user.username
