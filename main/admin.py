from django.contrib import admin

from main.models import *
from import_export.admin import ImportExportModelAdmin
from main.resources import TypeResource, SchoolResource, TypeResult
from django import db

@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(ImportExportModelAdmin):
    pass


@admin.register(LocalityType)
class LocalityAdmin(ImportExportModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource

@admin.register(ExamType)
class ExamTypeAdmin(ImportExportModelAdmin):
    pass

@admin.register(Examination)
class ExaminationAdmin(ImportExportModelAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    pass

@admin.register(ParticipantCategory)
class ParticipantType(ImportExportModelAdmin):
    pass
@admin.register(RequirementsSpec)
class RequirmentsAdmin(ImportExportModelAdmin):
    pass


@admin.register(ElementsSpec)
class ElementsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    resource_class = TypeResult
    skip_admin_log = True


@admin.register(Specification)
class SpecAdmin(ImportExportModelAdmin):
    pass


@admin.register(StudentAnswer)
class AnswerAdmin(ImportExportModelAdmin):
    pass


@admin.register(SchoolKind)
class KindAdmin(ImportExportModelAdmin):
    pass


@admin.register(SchoolType)
class TypeAdmin(ImportExportModelAdmin):
    resource_class = TypeResource


admin.site.register(UserTemplates)
admin.site.register(UserEducationalInstitution)
admin.site.register(UserDistrict)
