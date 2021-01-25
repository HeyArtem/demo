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


def f_snippet(search):
    '''Навыки на одной странице'''
    snippet = [] # здесь сохраняю навыки от соискателя
    params = {'text': f'{search}'}
    vacancies = requests.get(url, params=params).json()
    for item in vacancies['items']:
        if item['snippet']['requirement']:
            snippet.append(item['snippet']['requirement'])
    return snippet


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

        return render_template("search.html", search=search, start=request.form['search'], snippet=f_snippet(request.form['search']))


@app.route("/contacts")
def contacts():
    '''Страница с контактами'''
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run()



