'''
Example code to Mount/Unmount ISOs on VMware ESX/ESXi using pysphere
based on Sebastián Tello's code:
https://groups.google.com/d/msg/pysphere/f75KE4RZBzc/8qjNrC06CEQJ

pysphere: https://code.google.com/p/pysphere/

@kbandla
3/25/2013
'''
from pysphere import VIServer, VITask
from pysphere.resources import VimService_services as VI

server = VIServer()

def ReconfigureVM(vm, cdrom):
    # create a new VM Reconfigure Task
    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm._mor)
    _this.set_attribute_type(vm._mor.get_attribute_type())
    request.set_element__this(_this)

    # new device change spec
    spec = request.new_spec()
    dev_change = spec.new_deviceChange()
    dev_change.set_element_device(cdrom)
    dev_change.set_element_operation("edit")

    spec.set_element_deviceChange([dev_change])
    request.set_element_spec(spec)
    ret = server._proxy.ReconfigVM_Task(request)._returnval

    task = VITask(ret, server)
    status = task.wait_for_state([task.STATE_SUCCESS,task.STATE_ERROR])
    if status == task.STATE_SUCCESS:
        print "%s: successfully reconfigured" % vm.properties.name
        return True
    elif status == task.STATE_ERROR:
        print "%s: Error reconfiguring vm"% vm.properties.name
        return False

def mount_iso(vm_path, iso_path, connect=True):
    '''
    Connect an ISO to a VM 
        @vm_path    :   $str;   Path to the VM
                        Example: '[datastore1] YOUR_VM_PATH/YOUR_VM_IMAGE.vmx'
        @iso_path   :   $str;   Path to the ISO
                        Example: '[datastore1] ISO/cdrom.iso'

    returns a bool, indicating the success
    '''
    # get the VM object
    vm = server.get_vm_by_path(  vm_path )
    # get the cdrom
    cdrom = None
    for dev in vm.properties.config.hardware.device:
        if dev._type == "VirtualCdrom":
            cdrom = dev._obj
            # found cdrom
            break

    # mark as 'Connected'
    cdrom.Connectable.Connected = connect
    # mark as 'Connect at power on'
    cdrom.Connectable.StartConnected = connect

    if connect:
        # config
        iso = VI.ns0.VirtualCdromIsoBackingInfo_Def("iso").pyclass()
        iso.set_element_fileName(iso_path)
        cdrom.set_element_backing(iso)

    # reconfigure the VM
    return ReconfigureVM(vm, cdrom)

def unmount_iso( vm_path ):
    return mount_iso( vm_path, iso_path=None, connect=False)

# == Testing ==
def testMountISO(mount=True):
    server.connect(SERVER, USER, PASSWORD)
    vm_path = '[datastore1] YOUR_VM_PATH/YOUR_VM_IMAGE.vmx' 
    ISO_PATH ='[datastore1] ISO/cdrom.iso'
    if mount:
        mount_iso( vm_path, ISO_PATH)
    else:
        unmount_iso( vm_path )
    server.disconnect()

if __name__ == "__main__":
    testMountISO()
