'''
ctypes wrapper for aPlib
Kiran Bandla <kbandla@in2void.com>

ctypes wrapper to decompress aplib-compressed files
Tested against aPLib v1.01
'''

from ctypes import *
from hashlib import md5

def decompress( data ):
    '''Returns decompressed data
    On Windows, make sure you read the data with the 'rb' option
    Like so -> open('shellcode2.pak','rb').read()
    '''
    try:
        aplib = windll.LoadLibrary('aplib.dll') 
    except Exception,e:
        print 'Error loading dll : %s'%(e)
        return None
    unpacked_size = aplib._aPsafe_get_orig_size(data)
    print 'Unpacked size should be : ', unpacked_size
    unpacked_data =create_string_buffer(unpacked_size)
    try:
        unpacked_bytes = aplib._aPsafe_depack(data, len(data), unpacked_data, len(unpacked_data))
    except Exception,e:
        print 'Error unpacking data : %s'%(e)
    print 'Unpacked %s bytes [%s]'%(unpacked_bytes, md5(unpacked_data).hexdigest())
    return unpacked_data
