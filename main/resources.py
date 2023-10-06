from import_export import resources
from import_export import fields
from main.models import *
from django import db
from import_export.instance_loaders import CachedInstanceLoader


class KindResource(resources.ModelResource):
    class Meta:
        model = SchoolKind


class TypeResource(resources.ModelResource):
    class Meta:
        model = SchoolType


class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        exclude = ['id']
        import_id_fields = ['school_code']
        fields = ('school_code', 'district', 'full_name', 'short_name', 'adres', 'school_kind', 'property', 'town_type')


class TypeProperty(resources.ModelResource):
    class Meta:
        model = Property


class District(resources.ModelResource):
    class Meta:
        model = SchoolType


class Localitytype(resources.ModelResource):
    class Meta:
        model = LocalityType


class TypeExam(resources.ModelResource):
    class Meta:
        model = ExamType


class TypeSubject(resources.ModelResource):
    class Meta:
        model = Subject


class TypePaticipantCategory(resources.ModelResource):
    class Meta:
        model = ParticipantCategory


class TypeExamination(resources.ModelResource):
    class Meta:
        model = Examination


class TypeRequirments(resources.ModelResource):
    class Meta:
        model = RequirementsSpec


class TypeElemntSpec(resources.ModelResource):
    class Meta:
        model = ElementsSpec


class TypeResult(resources.ModelResource):
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        # for i1 in dataset:
        #     dt = list(str(dataset).replace('(', '').replace(')', ''))
        #     for j3 in range(len(dt)):
        #         dt[j3] = int(dt[j3])
        #         w1 = StudentAnswer(answer=dt[j3], result_id=Result.objects.get(id=dataset.id))
        #         w1.save()
        for i in Result.objects.all():
            rt = list(i.shortanswer)
            ln = list(str(i.full_answer).replace('(', '').replace(')', ''))
            k = 0
            s = 12
            for j1 in range(len(rt)):
                k += 1
                if (rt[j1] == '+'):
                    rt[j1] = 1
                elif rt[j1] == '-':
                    rt[j1] = 0
                rt[j1] = int(rt[j1])
                w1 = StudentAnswer(answer=rt[j1], result=Result.objects.get(id=i.id))
                target = Specification.objects.get(id=k)
                # w1 = ParticipantCategory(name="ляляля")
                w1.save()
                w1.task_number.add(k)
                w1.save()

            ln1 = ln[::2]
            for j2 in range(len(ln1)):
                s += 1
                ln1[j2] = int(ln1[j2])
                w1 = StudentAnswer(answer=ln1[j2], result=Result.objects.get(id=i.id))
                # w1 = ParticipantCategory(name="ляляля")
                target = Specification.objects.get(id=s)
                w1.save()
                w1.task_number.add(target)
                w1.save()

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     db.reset_queries()
    class Meta:
        model = Result
        skip_unchanged = True
        instance_loader_class = CachedInstanceLoader
        force_init_instance = True
        skip_diff = True
        use_bulk = True


class SpecificationResource(resources.ModelResource):
    class Meta:
        model = Specification


class TypeAnswer(resources.ModelResource):
    class Meta:
        model = StudentAnswer
