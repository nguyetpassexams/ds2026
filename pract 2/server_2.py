from xmlrpc.server import SimpleXMLRPCServer
import os

IP = "localhost"
PORT = 8000

def save_file(filename, binary_data):
    print(f"[UPLOAD] Receiving file: {filename}")
    
    with open(f"uploaded_{filename}", "wb") as f:
        f.write(binary_data.data)
        
    print(f"[FINISHED] Saved {filename} successfully.")
    return True  # Trả về kết quả cho Client

def main():
    print(f"[STARTING] RPC Server running on {IP}:{PORT}...")
    server = SimpleXMLRPCServer((IP, PORT), allow_none=True)
    
    # Đăng ký hàm để Client có thể gọi
    server.register_function(save_file, "upload_file")
    
    # Chạy server mãi mãi
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    main()