import psycopg2
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
    print("Wpisz okres: ")
    

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
    elif choice == '0':
        menuloop = False


conn.commit()
cursor.close()
conn.close()
