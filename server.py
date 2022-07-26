import random
import socket
from http import HTTPStatus


def rand_port():
    return random.randint(20000, 30000)


def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = rand_port()
        server.bind(("127.0.0.1", port))
        server.listen()
        print("port is ", port)
        while True:
            client, address = server.accept()
            data = client.recv(1024).decode("utf-8")

            url = data.splitlines()[0].split(" ")[1]
            send_status = "200"
            method = data.splitlines()[0].split(" ")[0]
            if method == "GET" and "status" in url:
                send_status = url.split("=")[1]
            try:
                text_status = [
                    i.name for i in list(HTTPStatus) if i.value == int(send_status)
                ][0]
                headers = ""
                for i in data.splitlines()[1:]:
                    headers += i + "<br>" + "\n"
                body = (
                    f"<div>Request Method: {method}<br>Request Source: {address}<br>Response Status: {send_status} "
                    f"{text_status}<br>{headers}</div>"
                )

                client.send(
                    f"HTTP/1.1 {send_status} {text_status}\n Content-Type: text/html\n\n{body}".encode(
                        "utf-8"
                    )
                )
            except IndexError:
                client.send(
                    "HTTP/1.1 200 OK\n Content-Type: text/html\n\nInvalid status code".encode(
                        "utf-8"
                    )
                )
            client.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()


start_server()
