import requests
import json

vcenter_server = '10.0.0.10'
username = 'Administrator@VSPHERE.LOCAL'
password = 'VMware123!'

def authenticate(vcenter_server, username, password):
    url = f'https://{vcenter_server}/rest/com/vmware/cis/session'
    response = requests.post(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.json()['value']
    else:
        raise Exception(f"Failed to authenticate: {response.status_code} {response.json()}")

def list_vms(vcenter_server, session_id):
    url = f'https://{vcenter_server}/rest/vcenter/vm'
    headers = {
        'vmware-api-session-id': session_id
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        vms = response.json()
        for vm in vms['value']:
            print(f"VM ID: {vm['vm']} - VM Name: {vm['name']}")
    else:
        raise Exception(f"Failed to list VMs: {response.status_code} {response.json()}")

# Add this function call in the main function before obtaining a guest ticket
try:
    # Step 1: Authenticate to vSphere API
    session_id = authenticate(vcenter_server, username, password)
    print(f"Authenticated successfully. Session ID: {session_id}")

    # Step 1.1: List VMs to verify the VM ID
    list_vms(vcenter_server, session_id)

    # Step 2: Obtain a guest authentication ticket
    ticket = obtain_ticket(vcenter_server, session_id, vm_id, guest_username, guest_password)
    print(f"Obtained guest authentication ticket: {ticket}")

    # Step 3: Transfer the file from datastore to VM
    transfer_file(vcenter_server, session_id, vm_id, ticket, datastore, datastore_path, destination_path)
    print(f"File transferred successfully to {destination_path}")

except Exception as e:
    print(f"An error occurred: {e}")
