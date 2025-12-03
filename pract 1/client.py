import socket
import os

SERVER_NAME = "localhost" 
PORT = 65432
FORMAT = "utf-8"
SIZE = 1024

def main():
    server_ip = socket.gethostbyname(SERVER_NAME)
    addr = (server_ip, PORT)
    
    print(f"[INFO] Resolved {SERVER_NAME} to {server_ip}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect(addr)

    file_path = "data.txt" 
    filename = file_path
    filesize = os.path.getsize(file_path)

    data = f"{filename}|{filesize}"
    client.send(data.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(SIZE)
            if not chunk:
                break
            client.send(chunk)

    print("File sent successfully.")
    client.close()

if __name__ == "__main__":
    main()