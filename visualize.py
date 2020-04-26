import cx_Oracle
import chart_studio
import re
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dash

chart_studio.tools.set_credentials_file(username='YMysak', api_key='jGU7zEFYXyP9VYXv71Qo')

username = 'SYSTEM'
password = 'SYSTEM'
database = 'localhost/xe'
print('connection start')

def fileId_from_url(url):

    raw_fileId = re.findall("~[0-z.]+/[0-9]+", url)[0][1:]
    return raw_fileId.replace('/', ':')


connection = cx_Oracle.connect(username,password, database)
cursor = connection.cursor()

""" create plot 1 Запит №1: вивести назву готелю і кількість рев'ю з оціною готелю 5 і більше """
query1 = '''
SELECT DISTINCT HOTEL_NAME, COUNT(REVIEWER_SCORE)
FROM REVIEWERS, HOTEL
WHERE REVIEWER_SCORE > 5
GROUP BY hotel.hotel_name
'''

hotel_name = []
RevScor_count = []

cursor.execute(query1)
for row in cursor.fetchall():

    hotel_name.append(row[0])

    RevScor_count.append(row[1])

bar = go.Bar(x=hotel_name, y=RevScor_count)

bar = py.plot([bar], auto_open=True, file_name="Plot1")

""" create plot 1 Запит №2: вивести відсоток рев'юверів певної національності від загальної кількості рев'юверів  """
query2 = '''
SELECT DISTINCT(REVIEWER_NATIONALITY),ROUND(COUNT(REVIEWER_NATIONALITY)/(SELECT COUNT(*) FROM REVIEWERS ),2)*100||'%' as PrecentOfNEGATIVE
FROM REVIEWERS
GROUP BY REVIEWER_NATIONALITY
ORDER BY PrecentOfNEGATIVE
'''
hotel_name = []
persent = []

cursor.execute(query2)
for row in cursor.fetchall():

    hotel_name.append(row[0])

    persent.append(row[1])

pie = go.Pie(labels=hotel_name, values=persent)

pie = py.plot([pie], auto_open=True, file_name="Plot2",)


my_dboard = dash.Dashboard()

bar_id = fileId_from_url(bar)

pie_id = fileId_from_url(pie)


box_1 = {

    'type': 'box',

    'boxType': 'plot',

    'fileId': bar_id,
    'title': 'task1'


}
box_2 = {

    'type': 'box',

    'boxType': 'plot',

    'fileId': pie_id,
    'title': 'task2'



}

my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)

py.dashboard_ops.upload(my_dboard, 'db_lab2')
cursor.close()
connection.close()