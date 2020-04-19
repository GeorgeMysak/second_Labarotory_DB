import cx_Oracle

import chart_studio.plotly as py

import plotly.graph_objs as go

import re

import chart_studio.dashboard_objs as dashboard

username = 'SYSTEM'
password = 'SYSTEM'
database = 'localhost'

print('connection start')


def fileId_from_url(url):
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
    return raw_fileId.replace('/', ':')


conn = cx_Oracle.connect(username, password, database)
cursor = conn.cursor()

""" create plot 1 Запит №1: вивести кількість рев'ю з оціною готелю 5 і більше """

firstQuery = """SELECT DISTINCT  REVIEWER_SCORE, HOTEL_NAME
FROM REVIEWERS, HOTEL
WHERE REVIEWER_SCORE > 5"""





cursor.execute(firstQuery)

HOTEL_NAME = []
REVIEWER_SCORE = []

for row in cursor:
    print(row)
    HOTEL_NAME += [row[0]]
    REVIEWER_SCORE += [row[1]]

data = [go.Bar(
    x=HOTEL_NAME,
    y=REVIEWER_SCORE
)]

layout = go.Layout(
    title='HOTEL_NAME',
    xaxis=dict(
        title='HOTEL_NAME',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='REVIEWER_SCORE',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data=data, layout=layout)

score_count = py.plot(fig, filename='HOTEL_NAME-REVIEWER_SCORE')

""" create plot 2 Запит №2: вивести % різниці оцінки певної групи рев'юверів від загальної. """
secondQuery = """SELECT HOTEL_NAME, AVERAGE_SCORE, REVIEWER_SCORE, ROUND(1 - REVIEWER_SCORE/AVERAGE_SCORE,2)*100||'%' as PrecentOfAVERAGE
FROM REVIEWERS, HOTEL,REVIEWS
"""
cursor.execute(secondQuery)

REVIEWER_NATIONALITY = []
percent_of_aveScore = []

for row in cursor:
    REVIEWER_NATIONALITY += [row[0]]
    percent_of_aveScore += [row[1]]

pie = go.Pie(labels=REVIEWER_NATIONALITY, values=percent_of_aveScore)
NATIONALITY = py.plot([pie], filename ='NATIONALITY-dep_on-score')

""" create plot 3 Запит №3: вивести динаміку збільшення оцінки по даті """
thirdQuery = """SELECT REVIEWER_NATIONALITY, ROUND(1 - REVIEWER_SCORE/AVERAGE_SCORE,2)*100||'%' as PrecentOfAVERAGE
FROM REVIEWERS, HOTEL,REVIEWS
"""

"""--------CREATE DASHBOARD------------------ """

my_dboard = dashboard.Dashboard()

score_count = fileId_from_url(score_count)
NATIONALITY = fileId_from_url(NATIONALITY)
box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': score_count,
    'title': 'Ревю з оцінкою> 5 та готель'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': NATIONALITY,
    'title': 'відсоток від загальної оцінки та ревювер'
}
my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)

py.dashboard_ops.upload(my_dboard, 'My First Dashboard ')