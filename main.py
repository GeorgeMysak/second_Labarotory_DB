import cx_Oracle

username = 'SYSTEM'
password = 'SYSTEM'
database = 'localhost'

print('connection start')

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

#Запит 1
print("Запит №1: вивести назву готелю і кількість рев'ю з оціною готелю 5 і більше \n")
query1 = """SELECT DISTINCT HOTEL_NAME, COUNT(REVIEWER_SCORE)
FROM REVIEWERS, HOTEL
WHERE REVIEWER_SCORE > 5
GROUP BY hotel.hotel_name"""
cursor.execute(query1)
record1 = cursor.fetchone()

for row in record1:
    print(row)

#Запит 2
print("\nЗапит №2: вивести відсоток рев'юверів певної національності від загальної кількості рев'юверів .\n")
query2 = """SELECT DISTINCT(REVIEWER_NATIONALITY),ROUND(COUNT(REVIEWER_NATIONALITY)/(SELECT COUNT(*) FROM REVIEWERS ),2)*100||'%' as PrecentOfNEGATIVE
FROM REVIEWERS
GROUP BY REVIEWER_NATIONALITY
ORDER BY PrecentOfNEGATIVE
"""
cursor.execute(query2)
record2 = cursor.fetchone()

for row in record2:
    print (row)


#Запит 3
print("\nЗапит №3: вивести динаміку  оцінки по даті.\n")
query3 = """SELECT  REVIEW_DATE,  REVIEWER_SCORE 
FROM REVIEWERS, REVIEWS
order by REVIEW_DATE
"""
cursor.execute(query3)
record3 = cursor.fetchone()

for row in record3:
    print (row)

cursor.close()
connection.close()