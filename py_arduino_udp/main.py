from socket import *
import psycopg2
import time


conn = psycopg2.connect(user="sensor", password="sensor", database="IEL", host="10.10.6.204", port="5432")
print("Connected to: ", conn)
cursor = conn.cursor()

address = ('192.168.107.7', 8888)  # define server IP and port
client_socket = socket(AF_INET, SOCK_DGRAM)  # Set up the Socket
client_socket.settimeout(5)  # Only wait x second for a response

while True:
    data = '1'.encode("utf-8")  #Set data request to Temperature
    client_socket.sendto(data, address)  #Send the data request

    try:

        rec_data, addr = client_socket.recvfrom(59676)  # Read response from arduino
        rec_data = rec_data.decode("utf-8")
        print("The Measured Temperature ONE is ", rec_data)  # Print the result
        print(rec_data)
        rec_data = rec_data.replace('\x00', '')
        rec_data = rec_data.replace('\00', '')
        rec_data = rec_data.replace('\0', '')
        print(rec_data)
        cursor.execute('INSERT INTO PUBLIC."TABLE1"(temp) VALUES (%s)', [rec_data])
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Exception: ", error)
        pass

    time.sleep(5)  # delay before sending next command

    print("")
