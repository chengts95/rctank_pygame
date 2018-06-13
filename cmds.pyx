
import numpy as np
import PyCRC.CRC16 as CRC16
ctypedef unsigned char uint8
ctypedef short int16
cdef toBytes(unsigned int i,uint8 l=1,byteorder='little'):
    return i.to_bytes(l, byteorder=byteorder)

header=b"$M<"

crc=CRC16.CRC16(True)


cpdef speed_cmd(int16 lspeed,int16 rspeed):

    func_code=0x55
    left_speed=toBytes(<unsigned short>lspeed,2)
    right_speed=toBytes(<unsigned short>rspeed,2)

    cmd=header+toBytes(5)+toBytes(func_code)+left_speed+right_speed
    chkcrc=crc.calculate(cmd[3:]).to_bytes(2, byteorder='little')
    cmd+=chkcrc
    return cmd
