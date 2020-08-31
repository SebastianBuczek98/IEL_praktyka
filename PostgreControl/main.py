import psycopg2
import matplotlib.pyplot as plt
import datetime
from matplotlib import dates
import numpy


conn = psycopg2.connect(user="guest", password="guest", database="IEL", host="10.10.6.204", port="5432")
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
            cursor.execute('INSERT INTO PUBLIC."TABLE1"(temp1, temp2) VALUES (%s, %s);', [float(ins_temp), float(ins_temp)])
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
            print("Temp1: ", row[1])
            print("Temp2: ", row[2])
            print("Date: ", row[3], "\n")

    except (Exception, psycopg2.Error) as error2:
        print("Exception: ", error2, "\n")


def rysujWykres():
    plotprint = "Temperatura"

    print("Wybierz czujnik: \n"
          "1. Dokladnosc pomiaru .01\n"
          "2. Dokladnosc pomiaru 1\n"
          "3. Obydwa czujniki\n")
    wybor_czujnika = input()
    print("Okres czasu od (YYYY-MM-DD GG:MM:SS): ")
    date_start = input()                #Pobranie daty początkowej
    #date_start = '2020-08-12'
    print("Do (YYYY-MM-DD GG:MM:SS): ")
    date_end = input()                  #Pobranie daty końcowej
    #date_end = '2020-08-13'
    try:
        if wybor_czujnika == '1':
            cursor.execute("SELECT \"date\", \"temp1\" FROM PUBLIC.\"TABLE1\" WHERE \"date\" between (%s) and (%s)", [date_start, date_end])  #backslashe są konieczne aby cudzysłowy nie były rozpoznawane jako znaki specjalne dla pythona, a dla postgre
            plotprint = "Temperatura (Czujnik 1)"
        if wybor_czujnika == '2':
            cursor.execute("SELECT \"date\", \"temp2\" FROM PUBLIC.\"TABLE1\" WHERE \"date\" between (%s) and (%s)", [date_start, date_end])  #backslashe są konieczne aby cudzysłowy nie były rozpoznawane jako znaki specjalne dla pythona, a dla postgre
            plotprint = "Temperatura (Czujnik 2)"
        if wybor_czujnika == '3':
            cursor.execute("SELECT \"date\", \"temp1\", \"temp2\" FROM PUBLIC.\"TABLE1\" WHERE \"date\" between (%s) and (%s)", [date_start, date_end])
        date = cursor.fetchall()
        for row in date:            #wyświetlenie rekordow (dla sprawdzenia poprawnosci dzialania)
            print("Date: ", row[0])
            print("Temp1: ", row[1], "\n")
            print("Temp2: ", row[2], "\n")
        datetoplot, value1, value2 = zip(*date)
        datetoplot2 = dates.date2num(datetoplot)

        plt.plot_date(datetoplot2, value1)
        plt.plot_date(datetoplot2, value2)
        plt.xticks(rotation='vertical')
        plt.setp(plt.xticks()[1], rotation=70)
        plt.plot_date(datetoplot, value1, fmt="r-", label='Czujnik 1')
        plt.plot_date(datetoplot, value2, fmt="g-", label='Czujnik 2')
        #plt.gcf().subplots_adjust(bottom=0.15)
        plt.xlabel("Czas")
        plt.ylabel(plotprint)
        plt.autoscale()
        plt.legend()
        plt.show()
    except (Exception, psycopg2.Error, TypeError) as error3:
        print(error3)


def wykres():
    plt.plot([1, 2, 3, 4], [5, 3, 7, 7])
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
