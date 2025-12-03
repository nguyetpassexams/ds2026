import socket
import os

# Cấu hình
HOST = "127.0.0.1"
PORT = 65432
FORMAT = "utf-8"
SIZE = 1024

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))
    
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        data = conn.recv(SIZE).decode(FORMAT)
        if not data:
            conn.close()
            continue
            
        filename, filesize = data.split("|")
        filename = os.path.basename(filename)
        filesize = int(filesize)
        
        print(f"[RECV] Receiving {filename} ({filesize} bytes)")

        conn.send("ACK".encode(FORMAT))

        with open(f"recv_{filename}", "wb") as f:
            bytes_read = 0
            while bytes_read < filesize:
                chunk = conn.recv(SIZE) 
                if not chunk:
                    break
                f.write(chunk)
                bytes_read += len(chunk)
                
        print(f"[COMPLETED] File received successfully.")
        conn.close()

if __name__ == "__main__":
    main()