from mpi4py import MPI
import os

# Cấu hình
TAG_META = 1
TAG_ACK = 2
TAG_DATA = 3
BUFFER_SIZE = 1024 * 1024 # 1MB buffer

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    if rank == 0:
        filename = "image_3d0794.jpg" # Đổi tên file có sẵn của bạn ở đây
        if not os.path.exists(filename):
            print(f"[Sender] Error: File {filename} not found.")
            return

        filesize = os.path.getsize(filename)
        print(f"[Sender] Starting transfer for {filename} ({filesize} bytes)...")

        # 1. Gửi Metadata (Tên file | Kích thước)
        metadata = {'name': filename, 'size': filesize}
        comm.send(metadata, dest=1, tag=TAG_META)

        # 2. Chờ xác nhận (ACK) từ Receiver
        ack = comm.recv(source=1, tag=TAG_ACK)
        if ack == "READY":
            print("[Sender] Receiver is ready. Sending data...")
            
            # 3. Gửi nội dung file
            with open(filename, 'rb') as f:
                file_data = f.read()
                comm.send(file_data, dest=1, tag=TAG_DATA)
                
            print("[Sender] File sent successfully.")

    
    elif rank == 1:
        print("[Receiver] Waiting for metadata...")
        
        # 1. Nhận Metadata
        metadata = comm.recv(source=0, tag=TAG_META)
        filename = "received_" + metadata['name']
        filesize = metadata['size']
        print(f"[Receiver] Incoming file: {filename} ({filesize} bytes)")

        # 2. Gửi xác nhận (ACK)
        comm.send("READY", dest=0, tag=TAG_ACK)

        # 3. Nhận dữ liệu file
        file_data = comm.recv(source=0, tag=TAG_DATA)
        
        # Ghi xuống đĩa
        with open(filename, 'wb') as f:
            f.write(file_data)
            
        print(f"[Receiver] File saved as {filename}.")

if __name__ == "__main__":
    main()