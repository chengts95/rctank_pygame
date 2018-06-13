import numpy as np
import PyCRC.CRC16 as CRC16
import struct
def toBytes(i,l=1):
    return struct.pack('l',i)[:l]

header=b"$M<"

crc=CRC16.CRC16(True)

def speed_cmd(lspeed, rspeed):

    func_code=0x55
    left_speed=toBytes(lspeed,2)
    right_speed=toBytes(rspeed,2)

    cmd=header+toBytes(5)+toBytes(func_code)+left_speed+right_speed
    chkcrc=crc.calculate(cmd[3:]).to_bytes(2, byteorder='little')
    cmd+=chkcrc
    return cmd
