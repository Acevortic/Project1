import socket
import sys


def main():
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ('', int(sys.argv[1]))  # Bind to all available interfaces

    try:
        welcome_socket.bind(server_addr)
        print("Listening")
    except socket.error as err:
        print(f"Error: {err}")
        sys.exit()

    welcome_socket.listen(5)  # Listen with a queue of 5 connection requests

    new_socket, client_addr = welcome_socket.accept()

    try:
        # Receive data from the client
        # data = new_socket.recv(4)  # Receive 4 bytes (32 bits) of data from the client
        # num = int.from_bytes(data, byteorder='big')  # Convert bytes to integer
        # print("Received integer:", num)

        data = new_socket.recv(4)  # Receive the client's operation
        operation = int.from_bytes(data, byteorder='big')

        while operation != 6:

            if operation == 1:
                response_msg = "Operation received successfully".encode()  # Encode the message as bytes
                new_socket.sendall(response_msg)  # Send the message back to the client

                data = new_socket.recv(4)
                ID = int.from_bytes(data, byteorder='big')

                firstName = ''
                while True:
                    chunk = new_socket.recv(1).decode('utf-8')
                    if chunk == '\n':
                        break
                    firstName += chunk  # Reads too much data from the client. -> Lastname and data are not written to.

                lastName = ''
                while True:
                    chunk = new_socket.recv(1).decode('utf-8')
                    if chunk == '\n':
                        break
                    lastName += chunk

                data = new_socket.recv(4)
                score = int.from_bytes(data, byteorder='big')
                f = open('database.txt', 'r+')
                f.write("ID: " + str(ID) + ' ')
                f.write("First name: " + firstName + ' ')
                f.write("Last name: " + lastName + ' ')
                f.write("score: " + str(score) + "\n")
                response_msg = "Data stored successfully".encode()  # Encode the message as bytes
                new_socket.sendall(response_msg)  # Send the message back to the client

            elif operation == 2:
                data = new_socket.recv(4).decode('utf-8')
                searchID = data

                with open('database.txt') as f:
                    if searchID in f.read():
                        found_response = "ID found successfully.".encode()
                        new_socket.sendall(found_response)

            elif operation == 6:
                break


        # Process the received data
        # print(f"Integer received: {num}") #Debug output ensuring the right data was received
        # print(f"ID received: {ID}")
        # print(f"First Name: {firstName}")
        # print(f"Last Name: {lastName}")
        # print(f"Score: {score}")

        # Send a response back to the client
        response_msg = "Data received successfully".encode()  # Encode the message as bytes
        new_socket.sendall(response_msg)  # Send the message back to the client

    except socket.error as err:
        print(f"Socket error: {err}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <port>")
        sys.exit(1)
    main()
