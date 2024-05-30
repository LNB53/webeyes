from pyVim import connect
from pyVmomi import vim
import ssl

def transfer_file_to_vm(host, user, password, vm_name, datastore_path, destination_path):
    service_instance = None
    try:
        # Connect to vSphere
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=password, sslContext=context)

        # Retrieve the VM object
        content = service_instance.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        vm = None
        for managed_object_ref in container.view:
            if managed_object_ref.name == vm_name:
                vm = managed_object_ref
                break
        container.Destroy()

        if vm is None:
            raise Exception("Virtual machine with name '{}' not found".format(vm_name))

        # Retrieve the datacenter object
        datacenter = None
        parent = vm.parent
        while True:
            if isinstance(parent, vim.Datacenter):
                datacenter = parent
                break
            elif parent is None:
                raise Exception("Datacenter not found for the VM")
            else:
                parent = parent.parent

        # Retrieve the datastore object
        datastore = None
        for entity in datacenter.datastoreFolder.childEntity:
            if isinstance(entity, vim.Datastore) and entity.name == datastore_path.split('/')[0]:
                datastore = entity
                break

        if datastore is None:
            raise Exception("Datastore '{}' not found".format(datastore_path.split('/')[0]))

        # Get the datastore browser
        browser = datastore.browser

        # Find the file on the datastore
        file_path = datastore_path.split('/')[1]
        search_spec = vim.HostDatastoreBrowserSearchSpec()
        search_spec.matchPattern = [file_path]
        search_task = browser.SearchDatastoreSubFolders_Task(datastore_path, search_spec)

        if search_task is None:
            raise Exception("Failed to initiate search task")

        while True:
            search_task_info = search_task.info
            if search_task_info.state == vim.TaskInfo.State.success:
                search_result = search_task_info.result
                break
            elif search_task_info.state == vim.TaskInfo.State.error:
                raise Exception("Search task failed: {}".format(search_task_info.error.localizedMessage))
            time.sleep(1)

        if search_result.state != vim.TaskInfo.State.success:
            raise Exception("File '{}' not found on datastore '{}'".format(file_path, datastore_path.split('/')[0]))

        # Get the file URL
        file_url = search_result.results[0].folderPath + '/' + file_path

        # Transfer the file to the VM
        vm_tools_status = vm.guest.toolsStatus
        if vm_tools_status != 'toolsOk':
            raise Exception("VM tools are not running properly")

        guest_auth = vim.vm.guest.NamePasswordAuthentication(username=user, password=password)
        guest_file_mgr = content.guestOperationsManager.fileManager
        url = service_instance.content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, guest_auth, destination_path)
        file_attribute = vim.vm.guest.FileManager.FileAttributes()
        file_attribute.accessTime = 0
        file_attribute.modificationTime = 0
        file_attribute.symlink = False
        file_attribute.digestEnabled = False
        guest_url = vim.vm.guest.FileManager.GuestUrl()
        guest_url.url = url
        guest_url.destinationDirectory = destination_path
        guest_url.attributes = file_attribute
        guest_file_mgr.TransferFileToGuest(guest_url, file_url, guest_auth, True)
        
        print("File transferred successfully to VM")

    except ssl.SSLError as e:
        print("SSL error occurred:", str(e))
        if hasattr(e, 'reason'):
            print("SSL Reason:", e.reason)
    except Exception as e:
        print("An error occurred:", str(e))
        if hasattr(e, 'faultMessage'):
            print("Fault Message:", e.faultMessage)
        if hasattr(e, 'msg'):
            print("Error Message:", e.msg)
    finally:
        if service_instance:
            connect.Disconnect(service_instance)

# Example usage:
host = '10.0.0.10'
user = 'Administrator@VSPHERE.LOCAL'
password = 'VMware123!'
vm_name = 'k3s-app-test-pool1-6f0e5c26-hdr4s'
datastore_path = '[DatastoreClusters] userfiles/testje.zip'
destination_path = '/home/user/testje.zip'

transfer_file_to_vm(host, user, password, vm_name, datastore_path, destination_path)
