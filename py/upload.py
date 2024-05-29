import sys
import ssl
import os
import requests
from ftplib import FTP
from pyVmomi import vim
from pyVim import connect
from pyVim.task import WaitForTask
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Suppress only the single InsecureRequestWarning from urllib3 needed for this script
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to upload file to datastore using HTTP PUT
def upload_to_datastore(file_path, upload_url, cookies):
    try:
        with open(file_path, 'rb') as file_data:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount('https://', HTTPAdapter(max_retries=retries))
            response = session.put(upload_url, data=file_data, cookies=cookies, verify=False)
            response.raise_for_status()
        print("File uploaded successfully.")
    except Exception as e:
        print(f"Failed to upload file: {e}")

# Function to download file from FTP server
def download_from_ftp(ftp_server, ftp_username, ftp_password, remote_file_path, local_file_path):
    try:
        ftp = FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
        ftp.quit()
        print(f"Downloaded {remote_file_path} to {local_file_path}")
    except Exception as e:
        print(f"Failed to download file: {e}")

# Check if the file name argument is provided
if len(sys.argv) < 2:
    print("Usage: python3 upload.py <uploaded_file_name>")
    sys.exit(1)

# Retrieve the file name from the command-line argument
uploaded_file_name = sys.argv[1]

# Retrieve the full path of the uploaded file on the FTP server
remote_file_path = f"/home/ftpserver/userfiles/{uploaded_file_name}"
local_file_path = f"/tmp/{uploaded_file_name}"

# Disable SSL certificate verification
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Connect to vCenter with custom SSL context
si = connect.SmartConnect(host="10.0.0.10",
                          user="administrator@vsphere.local",
                          pwd="VMware123!",
                          sslContext=context)

# Print the content of the vSphere service instance
print("vSphere Service Instance Content:")

# Get the content of the vCenter
content = si.RetrieveContent()

# Access Datastore
datastore_name = "DatastoreClusters"
datastore = None
datacenter_name = None
for dc in content.rootFolder.childEntity:
    if isinstance(dc, vim.Datacenter):
        datacenter_name = dc.name
        for ds in dc.datastoreFolder.childEntity:
            if isinstance(ds, vim.Datastore) and ds.name == datastore_name:
                datastore = ds
                break
    if datastore:
        break

if datastore is None:
    raise ValueError(f"Datastore '{datastore_name}' not found")

# Connect to FTP server and download the file locally
ftp_server = "10.0.0.204"
ftp_username = "ftpserver"
ftp_password = "ITF"

download_from_ftp(ftp_server, ftp_username, ftp_password, remote_file_path, local_file_path)

# Construct the upload URL for the HTTP PUT request
upload_url = f"https://{si._stub.host}/folder/userfiles/{uploaded_file_name}?dcPath={datacenter_name}&dsName={datastore_name}"

# Get the session cookie for authentication
session_cookie = si._stub.cookie
cookies = {'vmware_soap_session': session_cookie.split('"')[1]}

# Upload the file to the datastore
print("Uploading file:", uploaded_file_name)
upload_to_datastore(local_file_path, upload_url, cookies)

# Disconnect from vCenter
connect.Disconnect(si)
