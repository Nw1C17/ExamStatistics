from django.http import JsonResponse
from django.shortcuts import render

from main.forms import TemplateBuilderForm
from main.models import UserDistrict, District, Subject, School, UserTemplates, UserEducationalInstitution
from main.services import mainContext

YEARS = [
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020'),
    ('2021', '2021'),
]


def getContext(request):
    form = TemplateBuilderForm(request.POST or None)
    user = request.user
    SUBJECTS = list(Subject.objects.values_list('id', 'name'))
    DISTRICTS = []
    if UserDistrict.objects.filter(user=user).exists():  # Проверка юзера на районы
        # Если доступны все районы
        if list(UserDistrict.objects.filter(user=user).values_list('quantity', flat=True))[0]:
            DISTRICTS = list(District.objects.values_list('id', 'name'))  # Берем все районы
        else:
            a = list(UserDistrict.objects.filter(user=user).values_list('district', flat=True))[0]
            DISTRICTS = list(District.objects.filter(id=a).values_list('id', 'name'))  # Берем один район
    context = {
        'form': form,
        'subjects': SUBJECTS,
        'years': YEARS,
        'districts': DISTRICTS,
    }
    return context


def postData(request):
    data = {
        'name': request.POST.get('name'),
        'exam_type': request.POST.get('exam_type'),
        'head': request.POST.get('head'),
        'param': request.POST.getlist('param'),
        'stat_fields': request.POST.getlist('stat_fields'),
        'subjects': request.POST.getlist('subjects'),
        'years': request.POST.getlist('years'),
        'districts': request.POST.getlist('districts'),
        'educInsts': request.POST.getlist('educInsts'),
        'range': request.POST.getlist('range'),
    }
    saveData(data, request)
    return render(request, 'main/home.html', mainContext.getContext(request))
    # return JsonResponse(data, safe=False)


def saveData(data, request):
    new_temp = UserTemplates()
    new_temp.name = data['name']
    new_temp.user = request.user
    new_temp.jsonFile = data
    new_temp.save()


def requestAjax(request):
    if not request.POST.getlist('districts'):
        return JsonResponse({})
    else: #len(request.POST.getlist('districts')) != 0:
        return distAjax(request)




def distAjax(request):
    dist = request.POST.getlist('districts')
    educInsts = list(School.objects.filter(district__in=dist).values_list('school_code', 'short_name'))
    data = {'educInsts': educInsts}
    return JsonResponse(data)


    # user = request.user
    # distCheck = list(UserDistrict.objects.filter(user=user).values_list('quantity', flat=True))[0]
    # schoolCheck = list(UserEducationalInstitution.objects.filter(user=user).values_list('quantity', flat=True))[0]
    # print(distCheck, schoolCheck)
    # Если доступны все районы или все школы, то все школы этого района
    # if distCheck or schoolCheck:
    #     educInsts = list(School.objects.filter(district__in=dist).values_list('school_code', 'short_name'))
    # else:
    #     school_code = list(UserEducationalInstitution.objects.filter(user=user).values_list('school', flat=True))[0]
    #     educInsts = list(School.objects.filter(school_code=school_code).values_list('school_code', 'short_name'))