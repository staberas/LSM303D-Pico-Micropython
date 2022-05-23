from machine import UART, Pin, I2C
import time
import sys
from math import atan2, pi

xMag = 0
yMag = 0
zMag = 0
heading=0

## SET I2C bus - using pico pins 1-2 | 1, scl=machine.Pin(3), sda=machine.Pin(2)
sda=machine.Pin(2)
scl=machine.Pin(3)
i2c=machine.I2C(1,sda=sda, scl=scl, freq=100000)

## Enable LSM303D accelerator at I2C addr 0x1D => 29
config=bytearray(1)
config[0]=39+8
## Reg Control1: (0x20) 50Hz+enable (0x57) + block update
i2c.writeto_mem(29, 32, config)

config=bytearray(1)   
config[0]=0
# LSM303D Mag address, 0x1D(29) or 0x1E(30) 
# Select MR register, 0x02(02)
# 0x00(00) Continous conversion mode
config[0]=0
i2c.writeto_mem(29, 34, config) 
config[0]=0
i2c.writeto_mem(29, 35, config) 
config[0]=100
i2c.writeto_mem(29, 36, config) 
config[0]=32
i2c.writeto_mem(29, 37, config)
config[0]=0
i2c.writeto_mem(29, 38, config) 


def get_axis(reg): ## 40 - X , 42 - Y , 44 - Z
    high=bytearray(1)
    low=bytearray(1)
    i2c.readfrom_mem_into(29, reg, low)
    i2c.readfrom_mem_into(29, reg+1, high)
    res = high[0] * 256 + low[0]
    if (res<16384):
        result = res/16384.0
    elif (res>=16384 & res<49152):
        result = (32768-res)/16384.0
    else: 
        result = (res-65536)/16384.0
    return result

def getMagX():
    high=bytearray(1)
    low=bytearray(1)
    # X-Axis Mag MSB, X-Axis Mag LSB
    i2c.readfrom_mem_into(29, 8, low)
    i2c.readfrom_mem_into(29, 9, high)

    # Convert the data
    xMag = high[0] * 256 + low[0]
    #xMag = data0 * 256 + data1
    if xMag > 32767 :
        xMag -= 65536
    return xMag


def getMagY():
    high=bytearray(1)
    low=bytearray(1)
    # Y-Axis Mag MSB, Y-Axis Mag LSB
    i2c.readfrom_mem_into(29, 10, low)
    i2c.readfrom_mem_into(29, 11, high)
    
    # Convert the data
    yMag = high[0] * 256 + low[0]
    if yMag > 32767 :
        yMag -= 65536
    return yMag


def getMagZ():
    high=bytearray(1)
    low=bytearray(1)
    # Z-Axis Mag MSB, Z-Axis Mag LSB
    i2c.readfrom_mem_into(29, 12, low)
    i2c.readfrom_mem_into(29, 13, high)

    # Convert the data
    zMag = high[0] * 256 + low[0]
    if zMag > 32767 :
        zMag -= 65536
    return zMag

while True:
    time.sleep(0.1) 
    xMag = getMagX()
    yMag = getMagY()
    zMag = getMagZ()
    x = ( get_axis(40) + 1)
    y = (-get_axis(42) + 1)
    z = (-get_axis(44) + 1)
    try:
        heading = 180*atan2(yMag,xMag)/pi #assume pitch, roll are 0  
        if(heading < 0):
            heading += 360
        print(" ",f'{x:.3f}',",",f'{y:.3f}',",",f'{z:.3f}',",",xMag,",",yMag,",",zMag,",",heading," ")
    except:
        print("fail")        


