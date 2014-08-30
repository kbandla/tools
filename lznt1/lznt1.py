import sys
from ctypes import *
from pdb import set_trace

def decompress(data):
    '''
    '''
    data_len = len(data)
    data = create_string_buffer(data)
    print len(data)
    unpacked_data = create_string_buffer(len(data)*2)
    try:
        lznt1 = cdll.LoadLibrary('liblznt1.so')
        unpacked_len = lznt1.lznt1_decompress(data, len(data), unpacked_data)
        print unpacked_len
        print len(unpacked_data.raw)
        if unpacked_len == -1:
            print 'Error: Could not decompress data'
            return False
        return unpacked_data
    except Exception,e:
        print '%s'%e

if __name__ == "__main__":
    data = open(sys.argv[1]).read()
    unpacked = decompress(data)
