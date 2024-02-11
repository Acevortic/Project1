import socket
import sys


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (sys.argv[1], int(sys.argv[2]))

    def add(ID, firstName, lastName, score):
        client_socket.sendall(ID.to_bytes(4, byteorder='big'))
        client_socket.sendall((firstName + '\n').encode('utf-8'))
        client_socket.sendall((lastName + '\n').encode('utf-8'))
        client_socket.sendall(score.to_bytes(4, byteorder='big'))

    try:
        client_socket.connect(server_addr)
    except socket.error as err:
        print(f"Connection error: {err}")
        sys.exit()

    # num = int(input("Enter an integer: "))
    # cnum = num.to_bytes(4, byteorder='big')  # Convert integer to bytes in network byte order

    def reconnect():
        global client_socket
        client_socket.close()  # Close the existing socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Reinitialize the socket
        client_socket.connect(server_addr)  # Reconnect to the server

    while True:
        user_input = input("Enter 1 to add to database, 2 to search an ID in the database, 3 to display above score, "
                           "4 to display all, 5 to delete an ID, and 6 to exit: ")  # int input here causes infinite loop

        if user_input == '6':
            print("Goodbye! ")
            break
        elif user_input == '1':
            # Make this a function later
            ID = int(input("Enter ID number: "))
            firstName = input("Enter firstName: ")
            lastName = input("Enter lastName: ")
            score = int(input("Enter score: "))

            try:
                add(ID, firstName, lastName, score)
            except ConnectionResetError:
                print("Eros fucked up. Reconnecting... ")
                reconnect()

        elif user_input == '2':
            try:
                searchID = int(input("Enter the ID number you want to search: "))
                client_socket.sendall(str(searchID).encode('utf-8'))
            except ConnectionResetError:
                print("Eros fucked up the connection. Reconnecting... ")
                reconnect()

        msg = client_socket.recv(30).decode()  # Receive a reply message from the server
        print(msg)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <hostname> <port>")
        sys.exit(1)
    main()
