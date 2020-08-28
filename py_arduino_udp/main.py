from socket import *
import psycopg2
import time


conn = psycopg2.connect(user="sensor", password="sensor", database="IEL", host="10.10.6.204", port="5432")
print("Connected to: ", conn)
cursor = conn.cursor()

address = ('192.168.107.7', 8888)  # define server IP and port
client_socket = socket(AF_INET, SOCK_DGRAM)  # Set up the Socket
client_socket.settimeout(5)  # Only wait x second for a response
exitval = 1

while True:

    try:
        data1 = '1'.encode("utf-8")  # Set data request to Temperature
        data2 = '2'.encode("utf-8")  # Set data request to Temperature
        client_socket.sendto(data2, address)  # Send the data request
        rec_data2, addr = client_socket.recvfrom(59676)  # Read response from arduino
        rec_data2 = rec_data2.decode("utf-8")
        print("The Measured Temperature S2 is ", rec_data2)  # Print the result
        rec_data2 = rec_data2.replace('\x00', '')
        rec_data2 = rec_data2.replace('\00', '')
        rec_data2 = rec_data2.replace('\0', '')
        time.sleep(5)
        client_socket.sendto(data1, address)
        rec_data1, addr2 = client_socket.recvfrom(59677)
        rec_data1 = rec_data1.decode("utf-8")
        rec_data1 = rec_data1.replace('\x00', '')
        rec_data1 = rec_data1.replace('\00', '')
        rec_data1 = rec_data1.replace('\0', '')
        print("The Measured Temperature S1 is ", rec_data1)
        a1 = float(rec_data1)
        if float(rec_data2) > 100:
            tempx = a1
            a1 = float(rec_data2)
            rec_data2 = str(tempx)
        a1 = a1/100
        a1 = str(a1)
        print("The corrected temperature S1 & S2 is: ", a1 ," & ", rec_data2)  # Print the result
        if(float(a1)>1 and float(a1)<100 and float(rec_data2)>1 and float(rec_data2)<100):
            cursor.execute('INSERT INTO PUBLIC."TABLE1"(temp1, temp2) VALUES (%s, %s)', [a1, rec_data2])
            conn.commit()
            print("Sent!")
        else:
            time.sleep(10)
        del rec_data2, rec_data1, a1
        print()

    except (Exception, psycopg2.Error) as error:
        print("Exception: ", error)
        exitval = 0
        pass

    time.sleep(10)  # delay before sending next command

    print("")


