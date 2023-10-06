from main.models import UserDistrict, UserEducationalInstitution, Result, StudentAnswer, Specification
import pandas as pd
# distCheck = list(UserDistrict.objects.filter(user=user).values_list('quantity', flat=True))[0]
# schoolCheck = list(UserEducationalInstitution.objects.filter(user=user).values_list('quantity', flat=True))[0]
# user = request.user
def getContext(request):
    data = {'stat': []}
    results = list(Result.objects.filter(examination='1').values_list('examination', 'school_code', 'point_scale100', 'point_scale5', 'id'))
    df = pd.DataFrame(results, columns=['examination', 'school_code', 'point_scale100', 'point_scale5', 'id'])
    data['stat'] = [('Кол-во учеников сдававших профильную математику ', len(df.index)),
                        ('Средний балл по профильной математике ', round(df['point_scale100'].mean(), 1)),
                        ('Кол-во учеников набравших 100 баллов ', len(df[df['point_scale100'] == 100])),
                        ('Процент учеников не набравших пороговых значений ', round(100*(len(df[df['point_scale100'] < 27]) / len(df.index)), 1))]
    data.update(getCharts())
    return data

def getCharts():
    vals = []
    winners = []
    results = Result.objects.all()
    for i in range(1, 13):
        vals.append(len(list(
            StudentAnswer.objects.filter(task_number=Specification.objects.get(id=i), answer=1).values_list('answer')))/len(results)*100)
    values = [['1'], ['2'] , ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'], ['10'], ['11'], ['12']]
    c = len(results)
    for j in results:
        if j.point_scale100 >= 36:
            winners.append(i)
    for i in range (len(values)):
        values[i].append(vals[i])
    return {'values': values, 'c': c, 'winners': len(winners)}