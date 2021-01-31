from flask import Flask
from flask import request
import requests
from flask import render_template

app = Flask(__name__)

url = 'https://api.hh.ru/vacancies'

def f_vacancies(page, search):
    '''Зарплата на одной странице'''
    salary = []
    params = {'text': f'{search}', 'page': page}
    vacancies = requests.get(url, params=params).json()
    for item in vacancies['items']:
        start, stop = 0, 0
        if item['salary'] and item['salary']['currency'] == 'RUR':
            if item['salary']['from'] and item['salary']['to']:
                start = int(item['salary']['from'])
                stop = int(item['salary']['to'])
            elif item['salary']['from'] and not item['salary']['to']:
                start = int(item['salary']['from'])
                stop = start
            elif not item['salary']['from'] and item['salary']['to']:
                stop = int(item['salary']['to'])
                start = stop
        if (start + stop) / 2 > 0:
            salary.append((start + stop) / 2)
    return salary


def average_salary(search):
    '''Средняя зарпалата'''
    data = search.split()
    search = ' AND '.join(data)
    params = {'text': f'{search}'}
    pages = requests.get(url, params=params).json()['pages']
    vacancies = []
    for page in range(pages):
        vacancies.extend(f_vacancies(page, search))
    if len(vacancies):
        return sum(vacancies) / len(vacancies)
    else:
        return 'Нет данных!'


def one_page_snippet(page, search):
    '''Навыки на одной странице'''
    snippet = [] # здесь сохраняю навыки от соискателя
    params = {'text': f'{search}', 'page': page}
    vacancies = requests.get(url, params=params).json()
    for item in vacancies['items']:
        if item['snippet']['requirement']:
            snippet.append(item['snippet']['requirement'])
    return snippet


def f_snippet(search):
    req = []  # список слов
    data = search.split()
    search = ' AND '.join(data)
    params = {'text': f'{search}'}
    pages = requests.get(url, params=params).json()['pages']
    for page in range(pages):
        for char in one_page_snippet(page, search):
            req.extend(char.split())
    # грубая обработка
    sym = [',', '.', ';', ':', '<highlighttext>', '</highlighttext>', '/', ')', '(', 'e.g.']
    for i in range(len(req)):
        for s in sym:
            if s in req[i].lower():
                req[i] = req[i].replace(s, '')
    req_resault = [item.lower() for item in req if item]
    # чистая обработка
    sym = ['и', 'знание', 'с', 'на', 'работы', 'в', 'and', 'автоматизации', 'разработки', 'или', 'программирования',
           'данных', 'понимание', 'умение', 'от', '-', 'знания', 'лет', 'навыки', 'языков', 'владение', 'будет',
           'написания', 'уверенное', 'уровне', 'для', 'по', 'принципов', 'из', 'плюсом', 'желательно', 'работать',
           'высшее', '3', 'языка', 'r', 'не', 'скриптов', 'experience', 'систем', 'как', 'желание', 'года', 'базовые',
           'in', 'анализа', 'of', 'to', 'приветствуется', 'основ']
    for i in range(len(req_resault)):
        for s in sym:
            if s == req_resault[i].lower():
                req_resault[i] = req_resault[i].replace(s, '')
    req_resault = [item.lower() for item in req_resault if item]
    # частотный словарь
    my_dict = {}
    for k in req_resault:
        my_dict[k] = req_resault.count(k)
    # сортировка навыков
    resault = list(my_dict.items())
    resault.sort(key=lambda x: x[1], reverse=True)
    # оставляем наиболее частые навыки
    number = 20
    summ = sum([i[1] for i in resault[:number]])
    dict_list = []
    for item in resault[:number]:
        dict_list.append([item[0], f'{round(100 * item[1] / summ, 2)}%'])
    return dict_list


@app.route("/")
def hello():
    '''Главная страница с описанием сервиса'''
    return render_template("index.html")


@app.route("/form", methods=['GET', 'POST'])
def form():
    '''Страница с формой запроса'''
    if request.method == 'GET':
        return render_template('form.html')
    else:
        search = round(average_salary(request.form['search']), 2)
        snippet = f_snippet(request.form['search'])
        return render_template("search.html", salary=search, search=request.form['search'], snippet=snippet)


@app.route("/contacts")
def contacts():
    '''Страница с контактами'''
    contacts = ['email@email.ru', '8-1231316546', 'Челябинск, улица, дом']
    return render_template("contacts.html", cont=contacts)


if __name__ == '__main__':
    app.run()



