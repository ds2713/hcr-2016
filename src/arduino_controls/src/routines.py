#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
import serial
import time

def the_routines():
    rospy.init_node('routines', anonymous=True)
    rospy.Subscriber("arduino_routines", Int16, callback)
    rospy.spin()

# 0 is no
# 1 is yes
# 2 is calibrate
# 3 is shake hands
# 4 is change idle
# 5 is play
# 6 is tone

def callback(data):
    PREFIXCALIBRATE = '123'
    PREFIXSHAKEHANDS = '111'
    PREFIXCHANGEIDLE = '420'
    PREFIXYES = '777'
    PREFIXNO = '888'
    PREFIXPLAY = '999'
    PREFIXTONE = '990'

    global ser
    case = data.data

    if case == 0:
        ser.write('{}{}{}'.format(PREFIXNO,',',str(0)))
        ser.read(1)

    elif case == 1:
        ser.write('{}{}{}'.format(PREFIXYES,',',str(0)))
        ser.read(1)

    elif case == 2:
        ser.write('{}{}{}'.format(PREFIXCALIBRATE,',',str(0)))
        ser.read(1)

    elif case == 3:
        ser.write('{}{}{}'.format(PREFIXSHAKEHANDS,',',str(0)))
        ser.read(1)

    elif case == 4:
        ser.write('{}{}{}'.format(PREFIXCHANGEIDLE,',',str(0)))
        ser.read(1)

    elif case == 5:
        ser.write('{}{}{}'.format(PREFIXPLAY,',',str(0)))
        ser.read(1)

    elif case == 6:
        ser.write('{}{}{}'.format(PREFIXTONE,',',str(0)))
        ser.read(1)

    else:
        pass

if __name__ == '__main__':
    global ser
    ser = serial.Serial('/dev/ttyACM0', timeout=10.0)

    try:
        the_routines()
    except rospy.ROSInterruptException:
        pass
