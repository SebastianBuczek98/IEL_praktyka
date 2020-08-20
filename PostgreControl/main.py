import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(user="guest", password="guest", database="IEL", host="10.10.6.217", port="5432")
print("Connected to: ", conn)

cursor = conn.cursor()
cursor.execute("SELECT VERSION();")
version = cursor.fetchone()
print("Connected into - ", version)


def insert():
    insert_loop = True
    while True:
        print('\n("z" aby wyjsc)')
        print("Podaj pomiar temperatury: ")
        try:
            ins_temp = input()
            if ins_temp == 'z':
                break
            cursor.execute('INSERT INTO PUBLIC."TABLE1"(temp) VALUES (%s);', [float(ins_temp)])
            conn.commit()
            print("Poprawnie wprowadzono pomiar do bazy\n")
            insert_loop = False
        except (Exception, psycopg2.Error) as error1:
            print("Exception: ", error1)

        if not insert_loop:
            break


def display_all():
    try:
        cursor.execute('SELECT * FROM PUBLIC."TABLE1"')
        db_data = cursor.fetchall()

        for row in db_data:
            print("ID: ", row[0])
            print("Temp: ", row[1])
            print("Date: ", row[2], "\n")

    except (Exception, psycopg2.Error) as error2:
        print("Exception: ", error2, "\n")


def rysujWykres():
    print("Okres czasu od (YYYY-MM-DD GG:MM:SS): ")
    date_start = input()                #Pobranie daty początkowej
    print("Do (YYYY-MM-DD GG:MM:SS): ")
    date_end = input()                  #Pobranie daty końcowej
    try:
        cursor.execute("SELECT * FROM PUBLIC.\"TABLE1\" WHERE \"date\" between (%s) and (%s)", [date_start, date_end])  #backslashe są konieczne aby cudzysłowy nie były rozpoznawane jako znaki specjalne dla pythona, a dla postgre
        date = cursor.fetchall()
        for row in date:            #wyświetlenie rekordow (dla sprawdzenia poprawnosci dzialania)
            print("ID: ", row[0])
            print("Temp: ", row[1])
            print("Date: ", row[2], "\n")
    except (Exception, psycopg2.Error, TypeError) as error3:
        print(error3)


def wykres():
    plt.plot([1, 2, 3, 4], [5, 6, 7, 7])
    plt.show()


menuloop = True
while menuloop:
    print("\nWybierz akcje: \n"
          "1. Insert \n"
          "2. Wyswietl baze\n"
          "3. Rysuj wykres\n"
          "0. Zakoncz dzialanie programu")
    choice = input()
    if choice == '1':
        insert()
    elif choice == '2':
        display_all()
    elif choice == '3':
        rysujWykres()
    elif choice == '4':
        wykres()
    elif choice == '0':
        menuloop = False


conn.commit()
cursor.close()
conn.close()
