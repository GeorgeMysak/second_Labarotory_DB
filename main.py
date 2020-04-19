import cx_Oracle

username = 'SYSTEM'
password = 'SYSTEM'
database = 'localhost'

print('connection start')

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

#Запит 1
print("Запит №1: вивести кількість рев'ю з оціною готелю 5 і більше \n")
query1 = """
SELECT REVIEWER_SCORE, REVIEWER_NATIONALITY, HOTEL_NAME
FROM REVIEWERS, HOTEL
WHERE REVIEWER_SCORE > 5
"""
cursor.execute(query1)
record1 = cursor.fetchone()

for row in record1:
    print(row)

#Запит 2
print("\nЗапит №2: вивести % різниці оцінки певної групи рев'юверів від загальної.\n")
query2 = """

SELECT HOTEL_NAME, AVERAGE_SCORE, REVIEWER_SCORE, ROUND(1 - REVIEWER_SCORE/AVERAGE_SCORE,2)*100||'%' as PrecentOfAVERAGE
FROM REVIEWERS, HOTEL,REVIEWS
"""
cursor.execute(query2)
record2 = cursor.fetchone()

for row in record2:
    print (row)


#Запит 3
print("\nЗапит №3: вивести динаміку збільшення оцінки по даті.\n")
query3 = """
SELECT REVIEWER_SCORE, EXTRACT(MONTH FROM REVIEW_DATE)
FROM REVIEWERS, REVIEWS
"""
cursor.execute(query3)
record3 = cursor.fetchone()

for row in record3:
    print (row)

cursor.close()
connection.close()