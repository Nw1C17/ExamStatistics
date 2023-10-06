import pandas as pd
import math

from main.models import School, Result, Subject, Examination, UserTemplates


def getExamCode(data):
    # if data['head'] == '2':
    exam = list(Examination.objects.filter(exam=data['exam_type'], subject__in=data['subjects'], year='2021').values_list()) #Залочено на 2021 год
    exam_code = [exam[i][0] for i in range(len(exam))]
    # if data['head'] == '1':
    #     exam = list(Examination.objects.filter(year='2021').values_list()) #Залочено на 2021 год
    #     exam_code = [exam[i][0] for i in range(len(exam))]
    return exam_code

def getHead(data):
    if data['head'] == '2':
        sub = list(Subject.objects.filter(id__in=data['subjects']).values_list('name'))
        sub = [sub[i][0] for i in range(len(sub))]
        return sub
    if data['head'] == '1' and data['param'] != 'subjects':
        return ['2021']
    if data['head'] == '1' and data['param'] == 'subjects':
        return ['2021 Математика']


def getStatSubcject(first_param, exam_code, data, DataTable, school_code, df):
    stat = []
    for sc in first_param:
        stat.append((sc[0], []))
    for k in range(len(exam_code)):
        if 'sum' in data['stat_fields']:
            if 'Всего участников' not in DataTable['stat_fields']:
                DataTable['stat_fields'].append('Всего участников')
            sm = []
            for i in range(len(school_code)):
                dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                sm.append(len(dfRes.index)) #Добавляем кол-во записей
            try:
                for i in range(len(sm)):
                    stat[i][1][k] = stat[i][1][0] + (sm[i],)
            except:
                for i in range(len(sm)):
                    stat[i][1].append((sm[i],))

        if 'avg' in data['stat_fields']:
            if 'Средний балл' not in DataTable['stat_fields']:
                DataTable['stat_fields'].append('Средний балл')
            sm = []
            for i in range(len(school_code)):
                dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                val = dfRes['point_scale100'].mean()
                sm.append(0 if math.isnan(val) else round(val, 1))
            try:
                for i in range(len(sm)):
                    stat[i][1][k] = stat[i][1][0] + (sm[i],)
            except:
                for i in range(len(sm)):
                    stat[i][1].append((sm[i],))

        if 'score_5' in data['stat_fields']:
            if '2' not in DataTable['slice_fields']:
                DataTable['slice_fields'] = ['2', '3', '4', '5']
            for n in range(2, 6):
                sm, per = [], []
                for i in range(len(school_code)):
                    dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                    smRes = dfRes[dfRes['point_scale5'] == n]
                    # perRes = (len(dfRes.index)/len(smRes.index))*100 if len(smRes.index) != 0 else 0
                    perRes = round((len(smRes.index)/len(dfRes.index))*100, 1) if len(smRes.index) != 0 else 0
                    sm.append(len(smRes.index))
                    per.append(perRes)
                try:
                    for i in range(len(sm)):
                        stat[i][1][k] = stat[i][1][0] + (sm[i],per[i],)
                except:
                    for i in range(len(sm)):
                        stat[i][1].append((sm[i], per[i],))

        if 'score_100' in data['stat_fields']:
            rng = data['range']
            for j in range(1, len(rng), 2):
                s = "от " + str(rng[j-1]) + " до " + str(rng[j]) + " баллов"
                if s not in DataTable['stat_fields']:
                    DataTable['slice_fields'].append(s)

                sm, per = [], []
                for i in range(len(school_code)):
                    dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                    smRes = dfRes[(dfRes['point_scale100'] >= int(rng[j-1])) & (dfRes['point_scale100'] <= int(rng[j]))]
                    perRes = round((len(smRes.index)/len(dfRes.index))*100, 1   ) if len(smRes.index) != 0 else 0
                    sm.append(len(smRes.index))
                    per.append(perRes)
                try:
                    for i in range(len(sm)):
                        stat[i][1][k] = stat[i][1][0] + (sm[i],per[i],)
                except:
                    for i in range(len(sm)):
                        stat[i][1].append((sm[i], per[i],))
    return stat


def getStatYear(first_param, exam_code, data, DataTable, school_code, df):
    stat = []
    for sc in first_param:
        stat.append((sc[0], []))
    for k in range(len(exam_code)):
        if 'sum' in data['stat_fields']:
            if 'Всего участников' not in DataTable['stat_fields']:
                DataTable['stat_fields'].append('Всего участников')
            sm = []
            for i in range(len(school_code)):
                dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                sm.append(len(dfRes.index)) #Добавляем кол-во записей
            try:
                for i in range(len(sm)):
                    stat[i][1][k] = stat[i][1][0] + (sm[i],)
            except:
                for i in range(len(sm)):
                    stat[i][1].append((sm[i],))

        if 'avg' in data['stat_fields']:
            if 'Средний балл' not in DataTable['stat_fields']:
                DataTable['stat_fields'].append('Средний балл')
            sm = []
            for i in range(len(school_code)):
                dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                val = dfRes['point_scale100'].mean()
                sm.append(0 if math.isnan(val) else round(val, 1))
            try:
                for i in range(len(sm)):
                    stat[i][1][k] = stat[i][1][0] + (sm[i],)
            except:
                for i in range(len(sm)):
                    stat[i][1].append((sm[i],))

        if 'score_5' in data['stat_fields']:
            if '2' not in DataTable['slice_fields']:
                DataTable['slice_fields'] = ['2', '3', '4', '5']
            for n in range(2, 6):
                sm, per = [], []
                for i in range(len(school_code)):
                    dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                    smRes = dfRes[dfRes['point_scale5'] == n]
                    # perRes = (len(dfRes.index)/len(smRes.index))*100 if len(smRes.index) != 0 else 0
                    perRes = round((len(smRes.index)/len(dfRes.index))*100, 1) if len(smRes.index) != 0 else 0
                    sm.append(len(smRes.index))
                    per.append(perRes)
                try:
                    for i in range(len(sm)):
                        stat[i][1][k] = stat[i][1][0] + (sm[i],per[i],)
                except:
                    for i in range(len(sm)):
                        stat[i][1].append((sm[i], per[i],))

        if 'score_100' in data['stat_fields']:
            rng = data['range']
            for j in range(1, len(rng), 2):
                s = "от " + str(rng[j-1]) + " до " + str(rng[j]) + " баллов"
                if s not in DataTable['stat_fields']:
                    DataTable['slice_fields'].append(s)

                sm, per = [], []
                for i in range(len(school_code)):
                    dfRes = df[(df['examination'] == exam_code[k]) & (df['school_code'] == school_code[i])] #Фильтруем результаты
                    smRes = dfRes[(dfRes['point_scale100'] >= int(rng[j-1])) & (dfRes['point_scale100'] <= int(rng[j]))]
                    perRes = round((len(smRes.index)/len(dfRes.index))*100, 1   ) if len(smRes.index) != 0 else 0
                    sm.append(len(smRes.index))
                    per.append(perRes)
                try:
                    for i in range(len(sm)):
                        stat[i][1][k] = stat[i][1][0] + (sm[i],per[i],)
                except:
                    for i in range(len(sm)):
                        stat[i][1].append((sm[i], per[i],))
    return stat


def getContext(request, kwargs):
    DataTable = {}
    DataTable['stat_fields'] = []
    DataTable['slice_fields'] = []
    #Достаем шаблон пользователя
    data = list(UserTemplates.objects.filter(id=kwargs['temp_id']).values_list('jsonFile', flat=True))[0]
    #Выбераем экзамен
    exam_code = getExamCode(data)
    DataTable['head'] = getHead(data)
    print(exam_code)

    #Выбераем школы
    first_param, school_code = [], []
    if 'school' in data['param']:
        first_param = list(School.objects.filter(school_code__in=data['educInsts']).values_list('short_name'))
        school_code = list(School.objects.filter(school_code__in=data['educInsts']).values_list('school_code'))
        DataTable['param'] = "Образовательное учреждение"
    elif 'district' in data['param']:
        first_param = list(School.objects.filter(district__in=data['districts']).values_list('short_name'))
        school_code = list(School.objects.filter(district__in=data['districts']).values_list('school_code'))
        DataTable['param'] = "Образовательное учреждение"
    elif 'subject' in data['param']:
        first_param = list(Subject.objects.filter(id__in=data['subjects']).values_list('name'))
        school_code = list(School.objects.all().values_list('school_code'))
        DataTable['param'] = "Образовательное учреждение"
    school_code = [school_code[i][0] for i in range(len(school_code))]

    #Достаем результаты по экзамену и школе/району/предмету
    results = list(Result.objects.filter(examination__in=exam_code, school_code__in=school_code).values_list('examination',
                                                                                                             'school_code',
                                                                                                             'point_scale100',
                                                                                                             'point_scale5'))
    df = pd.DataFrame(results, columns=['examination', 'school_code', 'point_scale100', 'point_scale5'])

    stat = []
    if data['head'] == '2':
        stat = getStatSubcject(first_param, exam_code, data, DataTable, school_code, df)
    if data['head'] == '1':
        stat = getStatYear(first_param, exam_code, data, DataTable, school_code, df)
    #Вычесляем данные



    DataTable['tempName'] = data['name']
    DataTable['numberColumns'] = len(DataTable['head']) * (len(DataTable['stat_fields']) + (len(DataTable['slice_fields'])*2)) + 1 #Для ровной обводки таблицы
    DataTable['numberColumnsHead'] = len(DataTable['stat_fields']) + len(DataTable['slice_fields'])*2 #Для ровной обводки таблицы
    DataTable['stat'] = stat
    print(DataTable)
    print(data)
    return DataTable