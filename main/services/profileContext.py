from django.http import JsonResponse

from main.models import UserTemplates, UserEducationalInstitution, UserDistrict, District, School


def getContext(request):
    temp = list(UserTemplates.objects.filter(user=request.user).values_list('id', 'name'))
    ue = list(UserEducationalInstitution.objects.filter(user=request.user).values_list('school', 'quantity'))[0]
    ud = list(UserDistrict.objects.filter(user=request.user).values_list('district', 'quantity'))[0]
    d = list(District.objects.filter(code=ud[0]).values_list('name'))[0]
    e = list(School.objects.filter(school_code=ue[0]).values_list('short_name'))[0]
    ue = 'Все' if ue[1] else e[0]
    ud = 'Все' if ud[1] else d[0]
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'templates': temp,
        'ud': ud,
        'ue': ue
    }
    return context

def requestAjax(request):
    id = request.POST.get('id')
    UserTemplates.objects.filter(user=request.user, id=id).delete()
    temp = list(UserTemplates.objects.filter(user=request.user).values_list('id', 'name'))
    return JsonResponse({'templates': temp})