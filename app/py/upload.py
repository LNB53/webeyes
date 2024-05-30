import sys
import os
import paramiko
import traceback

# Function to download file from FTP server
def download_from_ftp(ftp_server, ftp_username, ftp_password, remote_file_path, local_file_path):
    try:
        transport = paramiko.Transport(ftp_server)
        transport.connect(username=ftp_username, password=ftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_file_path, local_file_path)
        sftp.close()
        transport.close()
        print(f"Downloaded {remote_file_path} to {local_file_path}")
    except Exception as e:
        print(f"Failed to download file: {e}")

# Function to upload file to another VM using SSH
def upload_to_vm(vm_host, vm_username, vm_password, local_file_path):
    try:
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"Local file {local_file_path} does not exist.")

        remote_file_path = f"/home/user/app/{os.path.basename(local_file_path)}"
        transport = paramiko.Transport((vm_host, 22))
        transport.connect(username=vm_username, password=vm_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
        print(f"Uploaded {local_file_path} to {remote_file_path} on {vm_host}")
    except Exception as e:
        print(f"Failed to upload file: {e}")
        traceback.print_exc()  # Print traceback for more information

# Check if the file name argument is provided
if len(sys.argv) < 2:
    print("Usage: python3 upload.py <uploaded_file_name>")
    sys.exit(1)

# Retrieve the file name from the command-line argument
uploaded_file_name = sys.argv[1]

# Retrieve the full path of the uploaded file on the FTP server
remote_file_path = f"/home/ftpserver/userfiles/{uploaded_file_name}"
local_file_path = f"/tmp/{uploaded_file_name}"

# Connect to FTP server and download the file locally
ftp_server = "10.0.0.204"
ftp_username = "ftpserver"
ftp_password = "ITF"

download_from_ftp(ftp_server, ftp_username, ftp_password, remote_file_path, local_file_path)

# Connect to the remote VM and upload the file
vm_host = "10.0.0.40"
vm_username = "user"
vm_password = "ITF"

upload_to_vm(vm_host, vm_username, vm_password, local_file_path)
