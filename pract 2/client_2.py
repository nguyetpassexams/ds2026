import xmlrpc.client
import os

IP = "localhost"
PORT = 8000

def main():
    proxy = xmlrpc.client.ServerProxy(f"http://{IP}:{PORT}/")

    filename = "image_3d0794.jpg" 
    
    if not os.path.exists(filename):
        print(f"[ERROR] File {filename} not found!")
        return

    print(f"[SENDING] Uploading {filename} via RPC...")
    
    # Đọc file dưới dạng Binary
    with open(filename, "rb") as handle:
        binary_data = xmlrpc.client.Binary(handle.read())
        result = proxy.upload_file(filename, binary_data)

    if result:
        print("[SUCCESS] File transfer completed.")

if __name__ == "__main__":
    main()